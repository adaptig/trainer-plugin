#!/usr/bin/env python3
"""Render a page and put it where THIS user will find it.

Two shapes come out of the same publisher:

  * PDF  (default)  -- the A4 one-pager, gated on being exactly one page.
  * PNG  (--png)    -- a social post at exact pixel size, gated on the headline fitting.

Works from any folder and on any surface the skill ships to:

  * Claude Code / a real computer  -> the system Downloads folder (macOS, Windows, Linux)
  * Cowork (Linux VM)              -> the user's connected Downloads folder if they
                                      connected one, else their connected folder
  * Claude app / claude.ai sandbox -> /mnt/user-data/outputs, so the file is handed
                                      back in the conversation

The HTML may live anywhere. Links to the brand pack written as `../adaptig-brand/...`
(the template's form) are rewritten to the pack's real location before rendering, so
the agent never has to work inside the plugin folder.

Usage:
    publish.py --topic "AI Agents Explained" --labels sheet,card sheet.html card.html
    publish.py --topic "..." --out /some/folder sheet.html      # override the location
    publish.py --png --topic "AI for Surgeons" cover.html
    publish.py --png --carousel --topic "..." 1.html 2.html 3.html
    publish.py --png --size 1x1 --topic "..." cover.html        # square instead of 4:5

Rendering is headless: no window appears, and nothing is opened for the user afterwards.
Every line printed is for the agent to relay: SURFACE, FOLDER, SAVED <path>.

SAVED means rendered, gated and delivered — and only that. Where no browser could be
found, or none finished in time, nothing is rendered at all, so the HTML source is handed
over under a different token, FALLBACK <path>, which an agent must never report as a
finished file, followed by one MESSAGE line to pass to the trainer as written. That copy
carries the brand pack embedded inside it, so the user can open and print it anywhere
without hunting for a folder of assets — but it is still source, still ungated.

Both shapes are GATED, and a page that fails its gate reaches nobody. A PDF that is not
exactly one page, and a social page whose headline ran past the type floor, are both
REJECTED and kept beside the source HTML for inspection; the exit code is 3 and the
user's folder is untouched. A page that still carries a template slot ({{HEADLINE}}) or
review wording ("ready for your review", "draft material", "unconfirmed") is REJECTED
before any rendering: that belongs in the chat reply, never on the page.

Rendering fails fast. Each browser launch gets ATTEMPT_SECONDS and the whole run
TOTAL_SECONDS; a browser that hangs is skipped, the next one found is tried, and when
none works the HTML is handed over with a print-it-yourself MESSAGE (exit 2).
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import datetime as dt
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote

# The two shapes the user picks between: a compact information sheet, or a visually
# relaxed info card. The label goes in the filename so someone holding both can tell
# them apart without opening either.
VERSION_LABELS = {"sheet": "Sheet", "card": "Card"}

# Social sizes, in the words a person uses for them. 4:5 is the default everywhere;
# 1:1 exists only because someone asked for a square.
SIZES = {"4x5": (1080, 1350), "1x1": (1080, 1080)}

WINDOWS_DOWNLOADS_GUID = "{374DE290-123F-4565-9164-39C4925E467B}"

# The brand pack sits beside tools/ in both layouts we ship:
#   plugin:  <plugin>/tools/publish.py  +  <plugin>/adaptig-brand/
#   zip:     <skill>/tools/publish.py   +  <skill>/adaptig-brand/
BRAND_DIR = Path(__file__).resolve().parent.parent / "adaptig-brand"

BROWSERS = {
    "Darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ],
    "Windows": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        # Edge ships with Windows, so this path is the reason the skill works on a
        # machine where nothing has been installed.
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    ],
    "Linux": [],  # resolved from PATH below
}
LINUX_BROWSER_NAMES = ["google-chrome", "google-chrome-stable", "chromium",
                       "chromium-browser", "microsoft-edge", "brave-browser", "msedge"]

# A headless print of one A4 page takes a few seconds. Brave on macOS was seen sitting on
# one for six minutes (180 s x 2 attempts) and then failing with no file at all, so every
# launch is capped and the whole run has a budget well under a minute. A browser that
# hangs is not retried: the next browser found is tried instead, and when none works the
# HTML is handed over with a message telling the trainer how to print it themselves.
ATTEMPT_SECONDS = 20
TOTAL_SECONDS = 55
MIN_ATTEMPT_SECONDS = 4

# Left in a page, these reach the client. Slots and review status belong in the chat
# reply to the trainer.
_SLOT = re.compile(r"\{\{\s*[A-Za-z0-9_]+\s*\}\}")
_REVIEW_WORDING = re.compile(
    r"ready for your review|review before use|\bdraft material\b|"
    r"\b(?:priced|scope|unpriced) draft\b|not approved (?:adaptig )?curriculum|"
    r"lorem ipsum|\b(?:TBD|TODO)\b|"
    r"待確認|未確認|待定|供審閱|草稿版|待确认|未确认|供审阅", re.IGNORECASE)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_NON_TEXT = re.compile(r"<(script|style)\b.*?</\1\s*>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class BrowserFailed(RuntimeError):
    """No usable PDF or PNG came out of a browser in the time allowed."""


# ---- Where the file goes -------------------------------------------------------------

def downloads_dir() -> Path:
    """The system Downloads folder, honouring a relocated one where we can read it."""
    system = platform.system()

    if system == "Windows":
        try:
            import winreg  # type: ignore[import-not-found]  # Windows-only

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
            )
            raw, _ = winreg.QueryValueEx(key, WINDOWS_DOWNLOADS_GUID)
            # The registry value is stored unexpanded, e.g. %USERPROFILE%\Downloads.
            path = Path(os.path.expandvars(raw))
            if path.parent.exists():
                path.mkdir(parents=True, exist_ok=True)
                return path
        except Exception:
            pass  # relocated-folder lookup failed; fall through to the default

    elif system == "Linux":
        xdg = shutil.which("xdg-user-dir")
        if xdg:
            try:
                out = subprocess.run([xdg, "DOWNLOAD"], capture_output=True,
                                     text=True, timeout=10).stdout.strip()
                if out and out != str(Path.home()):
                    path = Path(out)
                    path.mkdir(parents=True, exist_ok=True)
                    return path
            except Exception:
                pass

    path = Path.home() / "Downloads"
    path.mkdir(parents=True, exist_ok=True)
    return path


def output_dir(explicit: str | None) -> tuple[Path, str]:
    """(folder, surface). The surface name is printed so the agent can describe the
    hand-off truthfully: 'in your Downloads folder' is a lie inside a sandbox."""
    if explicit:
        p = Path(explicit).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p, "explicit"

    env = os.environ.get("ADAPTIG_OUTPUT_DIR")
    if env:
        p = Path(env).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p, "explicit"

    # Claude app / claude.ai code-execution sandbox: files here are handed back to the
    # user as downloads in the conversation.
    sandbox_out = Path("/mnt/user-data/outputs")
    if sandbox_out.is_dir():
        return sandbox_out, "claude-app"

    # Cowork: the user's connected folders are mounted under /sessions/<name>/mnt/<Folder>.
    # Nothing outside those mounts is visible to the user, so ~/Downloads inside the VM
    # would vanish with the session.
    sessions = Path("/sessions")
    if sessions.is_dir():
        for mnt in sorted(sessions.glob("*/mnt")):
            downloads = mnt / "Downloads"
            if downloads.is_dir():
                return downloads, "cowork-downloads"
            mounts = [d for d in mnt.iterdir() if d.is_dir()]
            if mounts:
                return mounts[0], "cowork-folder"

    return downloads_dir(), "downloads"


# ---- Rendering -----------------------------------------------------------------------

def find_browsers() -> list[str]:
    """Every Chromium-family browser we can drive headless, in order of preference."""
    found: list[str] = []
    for candidate in BROWSERS.get(platform.system(), []):
        if Path(candidate).exists() and candidate not in found:
            found.append(candidate)
    for name in LINUX_BROWSER_NAMES + ["google-chrome", "chromium", "msedge"]:
        path = shutil.which(name)
        if path and path not in found:
            found.append(path)
    return found


def find_browser() -> str | None:
    """The preferred browser, or None."""
    browsers = find_browsers()
    return browsers[0] if browsers else None


def page_problems(html: Path) -> list[str]:
    """Template slots or review wording left in the page's visible text."""
    try:
        text = html.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    text = _COMMENT.sub(" ", text)
    found = [m.group(0) for m in _SLOT.finditer(text)]
    visible = _TAG.sub(" ", _NON_TEXT.sub(" ", text))
    found += [m.group(0) for m in _REVIEW_WORDING.finditer(visible)]
    return sorted(set(found))


def slug(text: str) -> str:
    """Filename-safe, human-readable, hyphen-separated. Keeps the words legible."""
    cleaned = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip()
    cleaned = re.sub(r"[\s_]+", "-", cleaned)
    return re.sub(r"-{2,}", "-", cleaned).strip("-") or "One-Pager"


def target_path(folder: Path, topic: str, label: str, stamp: str, suffix: str = ".pdf") -> Path:
    """<Topic>-<Sheet|Card>-<YYYYMMDD>.pdf, never silently overwriting.

    BOTH parts go through slug(). The label reaches this function from the model via
    --labels, so an unslugged one carries `/` and `..` straight into the path and the
    file lands outside the folder the user was told about.
    """
    base = f"{slug(topic)}-{slug(label)}-{stamp}"
    path = folder / f"{base}{suffix}"
    n = 2
    while path.exists():
        path = folder / f"{base}-{n}{suffix}"
        n += 1
    return path


_BRAND_REF = re.compile(r"""((?:href|src)\s*=\s*["'])(?:\.\.?/)*adaptig-brand/""", re.IGNORECASE)


@contextlib.contextmanager
def resolve_brand_refs(html: Path) -> Iterator[Path]:
    """Point every `../adaptig-brand/...` reference at the pack's real location.

    The rewritten copy is written NEXT TO the source file (not in a temp folder) so any
    other relative references the agent made — a downloaded logo, say — keep resolving.

    It is created by `mkstemp`, so the name is unique to this invocation and the file is
    opened O_EXCL: a file that was already there can never be opened, truncated, or
    deleted on the way out. The old fixed name `<source>.__publish__.html` did all three
    — it destroyed a user's file that happened to be called that, and two runs on the
    same source raced each other for it. This is a context manager rather than a
    returned path so that nothing outside here decides what gets unlinked; what this run
    made is what this run removes.
    """
    if not BRAND_DIR.is_dir():
        raise RuntimeError(f"brand pack not found at {BRAND_DIR} — the skill folder was "
                           f"re-packed incorrectly; adaptig-brand/ must sit beside tools/")
    text = html.read_text(encoding="utf-8")
    fixed = _BRAND_REF.sub(lambda m: m.group(1) + BRAND_DIR.as_uri() + "/", text)
    handle, name = tempfile.mkstemp(dir=html.parent, suffix=html.suffix,
                                    prefix=f"{html.stem}.__publish__-")
    tmp = Path(name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as out:
            out.write(fixed)
        yield tmp
    finally:
        tmp.unlink(missing_ok=True)


# ---- The no-browser hand-off ---------------------------------------------------------
#
# Rendering needs a browser. Where there is none the HTML itself is handed over, and it
# has to be a file the user can actually open, print or screenshot — on its own, wherever
# it lands. Copying the pack next to it does not achieve that: the templates link
# `../adaptig-brand/...`, so a pack sitting *beside* the HTML in Downloads is one folder
# off, and it would drop 5.9 MB — 4.9 MB of it shapes the page never uses — into the
# user's folder on every run. Rewriting the links to absolute `file://` paths is worse
# again: it works only on this machine and prints the home directory into a file the user
# may forward. So the assets the page actually references are embedded in it. A one-pager
# comes out around 700 KB and a social page around 500 KB — one file, no folder to keep
# it next to, and it survives being emailed.

_MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".avif": "image/avif",
    ".svg": "image/svg+xml", ".ico": "image/x-icon",
    ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf",
    ".otf": "font/otf", ".css": "text/css", ".js": "text/javascript",
}

# A guard, not a budget: every brand asset is well under this. It stops one oversized
# reference — a phone photo the agent copied in beside its HTML — from turning the
# hand-off into a file too big to mail.
INLINE_MAX_BYTES = 4 * 1024 * 1024

_SCHEME = re.compile(r"^(?:[a-zA-Z][\w+.\-]*:|//|#)")
_BRAND_SEGMENT = re.compile(r"^(?:\.\.?/)*adaptig-brand/")
_LINK_TAG = re.compile(r"""<link\b[^>]*\brel\s*=\s*["']?stylesheet["']?[^>]*>""",
                       re.IGNORECASE)
_SCRIPT_TAG = re.compile(
    r"""<script\b[^>]*\bsrc\s*=\s*["']([^"']+)["'][^>]*>\s*</script\s*>""",
    re.IGNORECASE)
_HREF_VALUE = re.compile(r"""\bhref\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
_ATTR_REF = re.compile(r"""((?:href|src)\s*=\s*["'])([^"']+)(["'])""", re.IGNORECASE)
_URL_REF = re.compile(r"""(url\(\s*["']?)([^"')]+)(["']?\s*\))""", re.IGNORECASE)
_CSS_IMPORT = re.compile(
    r"""@import\s+(?:url\(\s*)?["']?([^"')\s;]+)["']?\s*\)?\s*;""", re.IGNORECASE)


def _asset(ref: str, base: Path) -> Path | None:
    """The readable file a reference points at, or None.

    `../adaptig-brand/...` is resolved against the pack's real location, exactly as the
    render path resolves it — the pack is never next to the HTML. Anything else is
    resolved against the file that referenced it. Absolute URLs, `data:`, `file:` and
    bare fragments are left alone: they are already self-contained, or they point at
    something we have no business rewriting.
    """
    if _SCHEME.match(ref):
        return None
    clean = unquote(ref.split("#")[0].split("?")[0]).strip()
    if not clean:
        return None
    brand = _BRAND_SEGMENT.match(clean)
    path = BRAND_DIR / clean[brand.end():] if brand else base / clean
    try:
        resolved = path.resolve()
        return resolved if resolved.is_file() else None
    except OSError:
        return None


def _too_big(path: Path) -> bool:
    return path.stat().st_size > INLINE_MAX_BYTES


def _data_uri(path: Path) -> str:
    mime = _MIME.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def _inline_urls(text: str, base: Path) -> str:
    """Every `url(...)` in a stylesheet — or in the page's own <style> — as a data URI."""
    def one(match: re.Match[str]) -> str:
        target = _asset(match.group(2), base)
        if target is None or _too_big(target):
            return match.group(0)
        return f'url("{_data_uri(target)}")'
    return _URL_REF.sub(one, text)


def _inline_css(text: str, base: Path, depth: int = 0) -> str:
    def imported(match: re.Match[str]) -> str:
        target = _asset(match.group(1), base)
        if target is None or depth >= 4 or _too_big(target):
            return match.group(0)
        return _inline_css(target.read_text(encoding="utf-8", errors="replace"),
                           target.parent, depth + 1)
    return _inline_urls(_CSS_IMPORT.sub(imported, text), base)


def inline_pack(html: Path) -> str:
    """The page as ONE self-contained file: stylesheets, fonts, logo, shapes embedded.

    Anything that cannot be read, is not a file type we embed, or is over the size guard
    is left exactly as written — a page that is partly embedded is still better than one
    that is not, and nothing here is allowed to lose a reference.
    """
    if not BRAND_DIR.is_dir():
        raise RuntimeError(f"brand pack not found at {BRAND_DIR} — the skill folder was "
                           f"re-packed incorrectly; adaptig-brand/ must sit beside tools/")
    text = html.read_text(encoding="utf-8")
    base = html.parent

    def stylesheet(match: re.Match[str]) -> str:
        href = _HREF_VALUE.search(match.group(0))
        target = _asset(href.group(1), base) if href else None
        if target is None or target.suffix.lower() != ".css" or _too_big(target):
            return match.group(0)
        css = _inline_css(target.read_text(encoding="utf-8", errors="replace"),
                          target.parent)
        return f"<style>\n{css}\n</style>"

    def script(match: re.Match[str]) -> str:
        target = _asset(match.group(1), base)
        if target is None or target.suffix.lower() != ".js" or _too_big(target):
            return match.group(0)
        code = target.read_text(encoding="utf-8", errors="replace")
        # A literal </script> inside the code would close the tag being opened here.
        return "<script>\n" + code.replace("</script", "<\\/script") + "\n</script>"

    def attribute(match: re.Match[str]) -> str:
        target = _asset(match.group(2), base)
        # Only asset types, so a plain <a href="notes.html"> stays a link to a page and
        # does not become a data URI.
        if (target is None or target.suffix.lower() not in _MIME or _too_big(target)):
            return match.group(0)
        return match.group(1) + _data_uri(target) + match.group(3)

    text = _LINK_TAG.sub(stylesheet, text)
    text = _SCRIPT_TAG.sub(script, text)
    text = _ATTR_REF.sub(attribute, text)
    # Last, so the page's own <style> block is covered too. The stylesheets inlined above
    # already hold data: URIs, which _asset declines, so nothing is rewritten twice.
    return _inline_urls(text, base)


def write_new_text(folder: Path, topic: str, label: str, stamp: str,
                   suffix: str, text: str) -> Path:
    """Write `text` to a file this call creates, never to one that was already there.

    target_path picks a free name, but a name that is free when it is checked can be
    taken by the time it is written. Opening "x" is the check and the write in one step;
    a lost race just takes the next name.
    """
    for _ in range(5):
        dest = target_path(folder, topic, label, stamp, suffix=suffix)
        try:
            with open(dest, "x", encoding="utf-8") as out:
                out.write(text)
            return dest
        except FileExistsError:
            continue
    raise RuntimeError(f"could not find a free filename in {folder}")


def _sandbox_flags() -> list[str]:
    """--no-sandbox only where Chrome refuses to start without it.

    That is running as root, which happens in a container and essentially nowhere else.
    On a normal account the flag buys nothing and turns off the renderer sandbox while
    we point the browser at model-authored HTML.
    """
    euid = getattr(os, "geteuid", None)  # absent on Windows
    return ["--no-sandbox"] if euid is not None and euid() == 0 else []


def _stop(proc: subprocess.Popen) -> None:
    """Kill the browser and the helper processes it started (its own process group)."""
    if proc.poll() is None:
        try:
            if os.name == "posix":
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                proc.kill()
        except OSError:
            with contextlib.suppress(OSError):
                proc.kill()


def _pdf_finished(pdf: Path, last_size: list[int]) -> bool:
    """A complete PDF whose size has stopped changing: some builds write it and then
    never exit, and the file is all we asked for."""
    try:
        size = pdf.stat().st_size
        if size <= 0 or size != last_size[0]:
            last_size[0] = size
            return False
        with pdf.open("rb") as stream:
            stream.seek(max(0, size - 1024))
            return b"%%EOF" in stream.read()
    except OSError:
        return False


def _browser_run(browser: str, flags: list[str], timeout: float,
                 finished_pdf: Path | None = None) -> subprocess.CompletedProcess:
    """One headless launch, in a profile directory of its own, hard-capped at `timeout`.

    Chrome serialises on its default profile's SingletonLock, so a second launch that
    reuses that profile blocks until the first lets go — the documented macOS hang of
    1 Sep 2026 (180 s). A fresh --user-data-dir per invocation removes the contention
    outright; it is deleted when the run returns. The browser runs in its own process
    group so a hung run is killed with every helper it spawned.
    """
    with tempfile.TemporaryDirectory(prefix="adaptig-chrome-",
                                     ignore_cleanup_errors=True) as profile:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run",
               "--no-default-browser-check", *_sandbox_flags(),
               f"--user-data-dir={profile}", *flags]
        extra = {"start_new_session": True} if os.name == "posix" else {}
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, **extra)
        stop_at = time.monotonic() + timeout
        last_size = [-1]
        try:
            while True:
                try:
                    out, err = proc.communicate(timeout=0.25)
                    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)
                except subprocess.TimeoutExpired:
                    pass
                if finished_pdf is not None and _pdf_finished(finished_pdf, last_size):
                    _stop(proc)
                    return subprocess.CompletedProcess(cmd, 0, "", "")
                if time.monotonic() >= stop_at:
                    raise subprocess.TimeoutExpired(cmd, timeout)
        finally:
            if proc.returncode is None:
                _stop(proc)
                with contextlib.suppress(subprocess.TimeoutExpired, OSError, ValueError):
                    proc.communicate(timeout=3)


def _seconds_left(deadline: float) -> float:
    return deadline - time.monotonic()


def _launch(browser: str, flags: list[str], produces: Path, what: str, deadline: float,
            finished_pdf: Path | None = None) -> subprocess.CompletedProcess:
    """One capped attempt. A hang is not retried on the same browser: it hangs again.

    A hung run can leave a truncated file behind, so the artefact it was asked for is
    removed — otherwise the caller's `exists()` check passes on a half-written file.
    """
    budget = min(ATTEMPT_SECONDS, _seconds_left(deadline))
    if budget < MIN_ATTEMPT_SECONDS:
        raise BrowserFailed(f"no time left to try {Path(browser).name}")
    try:
        return _browser_run(browser, flags, budget, finished_pdf)
    except subprocess.TimeoutExpired:
        produces.unlink(missing_ok=True)
        raise BrowserFailed(f"{Path(browser).name} did not finish {what} "
                            f"within {budget:.0f} s") from None
    except OSError as error:
        produces.unlink(missing_ok=True)
        raise BrowserFailed(f"{Path(browser).name} could not start: {error}") from None


def render(browser: str, html: Path, pdf: Path, deadline: float | None = None) -> None:
    deadline = deadline if deadline is not None else time.monotonic() + TOTAL_SECONDS
    flags = ["--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.resolve().as_uri()]
    proc = _launch(browser, flags, pdf, "printing the PDF", deadline, finished_pdf=pdf)
    if not pdf.exists() and _seconds_left(deadline) >= MIN_ATTEMPT_SECONDS:
        # Older builds spell the header flag differently; retry once before failing.
        flags[flags.index("--no-pdf-header-footer")] = "--print-to-pdf-no-header"
        proc = _launch(browser, flags, pdf, "printing the PDF", deadline, finished_pdf=pdf)
    if not pdf.exists():
        raise BrowserFailed(f"{Path(browser).name} produced no PDF: "
                            f"{(proc.stderr or proc.stdout or '').strip()[:300]}")


def render_any(browsers: list[str], html: Path, pdf: Path, deadline: float) -> str:
    """Print with the first browser that works inside the budget; return which one."""
    reasons = []
    for browser in browsers:
        if _seconds_left(deadline) < MIN_ATTEMPT_SECONDS:
            reasons.append("the time budget ran out")
            break
        try:
            render(browser, html, pdf, deadline)
            return browser
        except BrowserFailed as error:
            pdf.unlink(missing_ok=True)
            reasons.append(str(error))
    raise BrowserFailed("; ".join(reasons) or "no browser to try")


def page_count(pdf: Path) -> int:
    """Read the page tree's /Count when it is visible; fall back to counting page objects."""
    data = pdf.read_bytes()
    counts = [int(c) for c in re.findall(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)", data)]
    counts += [int(c) for c in re.findall(rb"/Count\s+(\d+)[^>]*?/Type\s*/Pages\b", data)]
    if counts:
        return max(counts)
    return len(re.findall(rb"/Type\s*/Page(?![s\w])", data))


# ---- Screenshots ---------------------------------------------------------------------

def png_size(png: Path) -> tuple[int, int]:
    """(width, height) from the PNG header. No image library: the IHDR chunk puts both
    as big-endian 32-bit integers at bytes 16..24, and every PNG starts that way."""
    header = png.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError(f"{png.name} is not a PNG")
    return (int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big"))


def _shot_flags(width: int, height: int) -> list[str]:
    """The flags specific to a screenshot pass. The headless/sandbox/profile flags come
    from _browser_run, so the screenshot and the DOM dump are taken of the same page, at
    the same size, after the same settling time."""
    return [
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        # Long enough for the webfonts to load and fit.js to finish measuring.
        "--virtual-time-budget=3000",
    ]


def screenshot(browser: str, html: Path, png: Path, width: int, height: int,
               deadline: float | None = None) -> str:
    """Screenshot the page at exact size AND return its serialised DOM from the SAME
    browser run (--screenshot and --dump-dom together), so the marks fit.js leaves on
    <body> describe the very render that was captured. One run, not two, because the
    PNG-size assertion below is the load-bearing check and must apply to the DOM it is
    read alongside."""
    flags = [*_shot_flags(width, height), f"--screenshot={png}", "--dump-dom",
             html.resolve().as_uri()]
    deadline = deadline if deadline is not None else time.monotonic() + TOTAL_SECONDS
    proc = _launch(browser, flags, png, "taking the screenshot", deadline)
    dom = proc.stdout or ""
    if not png.exists():
        raise BrowserFailed(f"{Path(browser).name} produced no PNG: "
                           f"{(proc.stderr or proc.stdout or '').strip()[:400]}")
    got = png_size(png)
    if got != (width, height):
        raise RuntimeError(f"{html.name} rendered at {got[0]}x{got[1]}, not "
                           f"{width}x{height} — the template's page box was changed, or "
                           f"the browser ignored --window-size")
    return dom


_FIT_DONE = re.compile(r"""<body[^>]*\bdata-fit\s*=\s*["']done["']""", re.IGNORECASE)
_OVERFLOW = re.compile(r"""<body[^>]*\bdata-overflow\s*=\s*["']1["']""", re.IGNORECASE)


def fit_failure(dom: str, force: bool = False) -> str | None:
    """Why this page must not be delivered, or None if it may be.

    Two different failures, and telling them apart is the point. `data-fit="done"`
    missing means fit.js never ran at all — a fonts or script problem, and the headline
    was never measured. `data-overflow="1"` means it was measured and did not fit even
    at the type floor, which is a word count problem and nothing else.
    """
    if not _FIT_DONE.search(dom):
        return ("fit.js never ran, so the headline was never measured — check that the "
                "template's links to the brand pack are intact")
    if _OVERFLOW.search(dom) and not force:
        return ("headline did not fit — cut words, never the type, then run again")
    return None


def carousel_pdf(browser: str, pages: list[Path], pdf: Path,
                 width: int, height: int) -> None:
    """One PDF holding the rendered slides, one slide per page, at their own size.

    A LinkedIn carousel is a document post, so the slides have to arrive as pages of a
    PDF rather than as separate images. They are already rendered: this only stacks
    them, so nothing can differ between the PNG a trainer posts to Instagram and the
    page they upload to LinkedIn.
    """
    images = "\n".join(f'  <img src="{page.resolve().as_uri()}" alt="">'
                        for page in pages)
    # The wrapper is scaffolding, and it is built in scratch space, not in the folder
    # the finished PDF goes to: the user's Downloads must never see a `__carousel__.html`
    # appear, however briefly. The slides are referenced by absolute file:// URI, so
    # where the wrapper sits makes no difference to what renders.
    with tempfile.TemporaryDirectory(prefix="adaptig-carousel-") as scratch:
        wrapper = Path(scratch) / "__carousel__.html"
        wrapper.write_text(
            "<!doctype html><meta charset=\"utf-8\"><style>\n"
            f"@page {{ size: {width}px {height}px; margin: 0 }}\n"
            "html, body { margin: 0; padding: 0; background: #fff }\n"
            f"img {{ display: block; width: {width}px; height: {height}px;\n"
            "  page-break-after: always; break-after: page }\n"
            "img:last-child { page-break-after: auto; break-after: auto }\n"
            f"</style>\n{images}\n", encoding="utf-8")
        render(browser, wrapper, pdf, time.monotonic() + TOTAL_SECONDS)
        pages_out = page_count(pdf)
        if pages_out != len(pages):
            raise RuntimeError(f"the carousel PDF came out {pages_out} pages long for "
                               f"{len(pages)} slides — nothing was delivered")


# ---- Main ----------------------------------------------------------------------------

def hand_over_html(pairs: list[tuple[str, str]], args, folder: Path, stamp: str,
                   why: str) -> int:
    """No PDF or PNG could be made: leave the HTML where the user will find it, and say
    in one line what to do with it.

    No silent failure and no half-delivery. What is handed over is NOT a finished
    deliverable, so it does not get the SAVED token an agent reports as delivered.
    It is, however, a file the user can open and print themselves: the brand pack is
    embedded (see inline_pack), not linked.
    """
    if args.png:
        made, advice = "image", "Open it in your browser and take a screenshot at 1080 pixels wide."
    else:
        made, advice = "PDF", ("Open it in your browser and choose Print > Save as PDF "
                               "(A4, no headers and footers).")
    for html, label in pairs:
        source = Path(html)
        try:
            page = inline_pack(source)
            dest = write_new_text(folder, args.topic, label, stamp, ".html", page)
            note = ""
            if "file://" in page:
                # A photo the trainer gave us goes in as an absolute path to their own
                # disk: right here, wrong anywhere else.
                note = " One image still points at a file on this computer."
        except (OSError, RuntimeError, ValueError) as error:
            # Never lose the hand-off over a packaging problem: the source itself is
            # still better than nothing, as long as we say what is wrong with it.
            dest = target_path(folder, args.topic, label, stamp, suffix=".html")
            shutil.copy2(source, dest)
            note = (f" The brand files could not be embedded ({error}), so keep it next to "
                    f"the adaptig-brand folder.")
        print(f"FALLBACK {dest}  (HTML source, not a checked {made})")
        print(f"MESSAGE The {made} could not be made on this computer, so your page is saved "
              f"as {dest.name} in {dest.parent}. {advice}{note}")
    print(f"NO_BROWSER {why}")
    return 2


def deliver_pngs(args, browsers: list[str], folder: Path,
                 labels: list[str], stamp: str) -> int:
    """The --png half: screenshot, gate, then hand over. Mirrors the PDF half exactly —
    every page is rendered and checked in a scratch folder, and only pages that passed
    are copied into the user's own."""
    width, height = SIZES[args.size]

    with tempfile.TemporaryDirectory() as scratch_name:
        scratch = Path(scratch_name)
        passed: list[tuple[str, Path]] = []
        bad = 0

        deadline = time.monotonic() + TOTAL_SECONDS
        browser = browsers[0]
        for index, (html, label) in enumerate(zip(args.html, labels), start=1):
            shot = scratch / f"page-{index:02d}.png"
            reasons: list[str] = []
            dom = None
            for candidate in browsers:
                try:
                    with resolve_brand_refs(Path(html)) as src:
                        dom = screenshot(candidate, src, shot, width, height, deadline)
                    browser = candidate
                    break
                except BrowserFailed as error:
                    shot.unlink(missing_ok=True)
                    reasons.append(str(error))
                except RuntimeError as error:  # wrong size or missing pack: not a browser problem
                    print(f"error: {error}", file=sys.stderr)
                    return 1
            if dom is None:
                # A post or carousel is handed over whole: pages that already passed
                # are still only in scratch space.
                return hand_over_html(list(zip(args.html, labels)), args,
                                      folder, stamp, "; ".join(reasons))
            browsers = [browser] + [b for b in browsers if b != browser]

            reason = fit_failure(dom, force=args.force)
            if reason:
                bad += 1
                # Through target_path like every other file we write: a second run on
                # the same page used to overwrite the first render, which is exactly
                # the artefact someone is comparing against.
                source = Path(html).resolve()
                kept = target_path(source.parent, source.stem, label, stamp,
                                   suffix=".rejected.png")
                shutil.copy2(shot, kept)
                print(f"REJECTED {html}  ({reason}). Nothing was delivered; "
                      f"the render is at {kept}")
                continue
            passed.append((label, shot))

        for label, shot in passed:
            dest = target_path(folder, args.topic, label, stamp, suffix=".png")
            shutil.copy2(shot, dest)
            print(f"SAVED {dest}  ({width}x{height}, "
                  f"{dest.stat().st_size // 1024} KB)")

        if args.carousel:
            if bad:
                # A carousel with a hole in it is not a carousel. The PNGs that passed
                # are still worth having; the document post is not.
                print(f"SKIPPED the carousel PDF — {bad} of {len(args.html)} slides "
                      f"were rejected, and a document post cannot be missing a page")
            else:
                pdf = target_path(folder, args.topic, "Carousel", stamp, suffix=".pdf")
                try:
                    carousel_pdf(browser, [shot for _, shot in passed], pdf,
                                 width, height)
                except RuntimeError as error:
                    print(f"error: {error}", file=sys.stderr)
                    pdf.unlink(missing_ok=True)
                    return 1
                print(f"SAVED {pdf}  ({len(passed)}pp, "
                      f"{pdf.stat().st_size // 1024} KB)")

    print(f"BROWSER {Path(browser).name}")
    return 3 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", nargs="+", help="HTML files, in the order they come out")
    ap.add_argument("--topic", required=True, help="what the page is about")
    ap.add_argument("--date", help="YYYY-MM-DD; defaults to today")
    ap.add_argument("--labels",
                    help="comma-separated version keys matching the HTML files; "
                         "defaults to sheet,card for a PDF and Post for a social image")
    ap.add_argument("--out", help="folder to write into (overrides surface detection)")
    ap.add_argument("--force", action="store_true",
                    help="deliver a social image whose headline overflowed; --png only, "
                         "and never available for a one-pager")
    ap.add_argument("--png", action="store_true",
                    help="screenshot each page at exact pixel size instead of printing a PDF")
    ap.add_argument("--size", choices=sorted(SIZES), default="4x5",
                    help="social image size: 4x5 (1080x1350, the default) or 1x1 (1080x1080)")
    ap.add_argument("--carousel", action="store_true",
                    help="the pages are one carousel: number them and stack them into a PDF too")
    args = ap.parse_args()

    if args.carousel and not args.png:
        print("! --carousel only applies to --png", file=sys.stderr)
        return 1

    if args.force and not args.png:
        # The docstring has always said "never for a one-pager"; the flag did not.
        # A two-page one-pager is not a judgement call the caller gets to override.
        print("! --force only applies to --png. A PDF that is not exactly one page is "
              "not a one-pager: cut content, do not shrink the type, then run again",
              file=sys.stderr)
        return 1

    stamp = (dt.date.fromisoformat(args.date) if args.date
             else dt.date.today()).strftime("%Y%m%d")

    if args.labels:
        labels: list[str] = [
            VERSION_LABELS[k.strip().lower()] if k.strip().lower() in VERSION_LABELS
            else k.strip().title()
            for k in args.labels.split(",")
        ]
    elif args.carousel:
        # The slide number is part of the name, because a folder of social images is
        # sorted by name and the order is the whole point of a carousel.
        labels = [f"Carousel-{n}" for n in range(1, len(args.html) + 1)]
    elif args.png:
        labels = ["Post"] * len(args.html)
    else:
        labels = ["Sheet", "Card"]

    if len(labels) < len(args.html):
        print(f"! {len(args.html)} files but {len(labels)} labels — pass --labels",
              file=sys.stderr)
        return 1

    problems = {html: page_problems(Path(html)) for html in args.html}
    if any(problems.values()):
        for html, found in problems.items():
            if found:
                print(f"REJECTED {html}  (still carries {', '.join(found)} — fill or remove "
                      f"every slot, and keep review status and gaps for the chat reply; "
                      f"nothing was delivered)")
        return 3

    folder, surface = output_dir(args.out)
    browsers = find_browsers()
    print(f"SURFACE {surface}")
    print(f"FOLDER {folder}")

    if not browsers:
        return hand_over_html(list(zip(args.html, labels)), args, folder, stamp,
                              "no Chromium-family browser (Chrome, Edge, Brave or "
                              "Chromium) was found")

    if args.png:
        return deliver_pngs(args, browsers, folder, labels, stamp)

    # Render to a scratch file and GATE on the page count before anything reaches the
    # user's folder. A two-page "one-pager" must never land in Downloads, and the agent
    # must never have to delete a failed attempt out of the user's own files.
    bad = 0
    deadline = time.monotonic() + TOTAL_SECONDS
    pairs = list(zip(args.html, labels))
    for index, (html, label) in enumerate(pairs):
        failed = None
        with resolve_brand_refs(Path(html)) as src:
            with tempfile.TemporaryDirectory() as scratch:
                tmp_pdf = Path(scratch) / "render.pdf"
                # A browser that fails or hangs costs at most ATTEMPT_SECONDS; when none
                # works inside TOTAL_SECONDS the HTML is handed over instead.
                try:
                    used = render_any(browsers, src, tmp_pdf, deadline)
                    browsers = [used] + [b for b in browsers if b != used]
                except BrowserFailed as error:
                    failed = str(error)
                if failed is None:
                    pages = page_count(tmp_pdf)
                    if pages != 1:
                        bad += 1
                        source = Path(html).resolve()
                        kept = target_path(source.parent, source.stem, label, stamp,
                                           suffix=".rejected.pdf")
                        shutil.copy2(tmp_pdf, kept)
                        print(f"REJECTED {kept}  ({pages}pp, expected 1 — nothing was "
                              f"delivered; cut content, do not shrink the type, then run again)")
                        continue
                    pdf = target_path(folder, args.topic, label, stamp)
                    shutil.copy2(tmp_pdf, pdf)
        if failed is not None:
            return hand_over_html(pairs[index:], args, folder, stamp, failed)
        print(f"SAVED {pdf}  ({pages}pp, {pdf.stat().st_size // 1024} KB)")

    print(f"BROWSER {Path(browsers[0]).name}")
    return 3 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
