#!/usr/bin/env python3
"""Render a reviewed workshop brief into five portable, offline HTML documents.

Python 3.10+, standard library only. No model/API calls, network or automatic opening.
The renderer formats supplied content. It does not research, approve or invent it.
Everything it embeds is client-facing: review status, open questions and gaps belong in
the chat reply to the trainer, so `status` is never rendered and review or placeholder
wording in rendered text is rejected.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import math
from pathlib import Path
import re
import sys
from typing import Any


SKILL_DIR = Path(__file__).resolve().parent.parent
OUTPUTS = {
    "index.html": ("workshop", False),
    "workshop.html": ("workshop", True),
    "proposal.html": ("proposal", True),
    "one-pager.html": ("one-pager", True),
    "linkedin.html": ("linkedin", True),
}
MAX_INPUT_BYTES = 2 * 1024 * 1024
# The language of the client-facing text, as a BCP 47 tag. It sets <html lang>, which
# makes the browser pick the right glyphs (zh-Hant-HK gets Hong Kong forms, not Japanese
# or Simplified ones), and a zh tag switches the pack's own labels to Traditional Chinese.
LANG_TAG = re.compile(r"[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8}){0,3}")
DOC_NAMES = {"workshop": "Workshop", "proposal": "Proposal", "one-pager": "One-pager", "linkedin": "LinkedIn post"}

# Wording that belongs to the trainer's review, never to a document the client sees.
# Kept narrow so real content ("tools IT has not approved") passes. Slots are rejected
# everywhere; status wording and gap tags everywhere except the exercise, whose invented
# scenario may legitimately talk about an unconfirmed ETA.
STRUCTURAL_SLOTS = [
    re.compile(r"\{\{[^}]*\}\}"), re.compile(r"\[[A-Z][A-Z0-9 _/,.'&-]{2,}\]"),
    re.compile(r"\b(?:TBD|TBC|TODO)\b"), re.compile(r"lorem ipsum", re.IGNORECASE),
]
REVIEW_WORDING = [re.compile(p, re.IGNORECASE) for p in (
    r"ready for your review", r"review before use", r"\b(?:priced|scope|unpriced) draft\b",
    r"\bunpriced\b", r"\bdraft material\b", r"not approved (?:adaptig )?curriculum",
    r"brand snapshot",
    # the same review wording in Chinese (Traditional, then Simplified)
    r"待確認|未確認|待定|供審閱|草稿版|待确认|未确认|供审阅",
    # a gap tag: the whole field, or a trailing "— unconfirmed" / "(proposed)"
    r"^\s*(?:unconfirmed|not supplied|not confirmed|to be confirmed)\W*$",
    r"[—–(:]\s*(?:unconfirmed|not supplied|not confirmed|to be confirmed|proposed)\s*\)?\s*\.?$",
)]

class SchemaError(ValueError):
    """A supplied brief cannot be rendered without inventing required content."""


def _object(value: Any, path: str) -> dict:
    if not isinstance(value, dict):
        raise SchemaError(f"{path}: expected an object")
    return value


def _text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SchemaError(f"{path}: supply non-empty text; leave an unknown optional field out "
                          "and list the gap for the trainer in chat")
    if len(value) > 30_000:
        raise SchemaError(f"{path}: text exceeds 30,000 characters")
    return value


def _texts(value: Any, path: str, *, empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not empty):
        raise SchemaError(f"{path}: expected {'an' if empty else 'a non-empty'} array")
    if len(value) > 60:
        raise SchemaError(f"{path}: at most 60 entries")
    for index, item in enumerate(value):
        _text(item, f"{path}[{index}]")
    return value


def _number(value: Any, path: str, *, integer: bool = False, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SchemaError(f"{path}: expected {'an integer' if integer else 'a number'}")
    if not math.isfinite(value) or value < 0 or (positive and value <= 0):
        raise SchemaError(f"{path}: expected a finite {'positive' if positive else 'non-negative'} value")
    if integer and not isinstance(value, int):
        raise SchemaError(f"{path}: expected an integer")
    return value


def _records(value: Any, path: str, fields: tuple[str, ...]) -> list[dict]:
    if not isinstance(value, list) or not value or len(value) > 60:
        raise SchemaError(f"{path}: expected 1–60 objects")
    for index, item in enumerate(value):
        obj = _object(item, f"{path}[{index}]")
        for field in fields:
            _text(obj.get(field), f"{path}[{index}].{field}")
    return value


def _known(obj: dict, keys: set[str], path: str) -> None:
    extra = set(obj) - keys
    if extra:
        raise SchemaError(f"{path}: unrecognized fields: {', '.join(sorted(extra))}; remove private notes and unsupported fields")


def available_documents(data: dict) -> list[str]:
    docs = []
    if any(key in data for key in ("exercise", "timeline", "learningOutcomes")):
        docs.append("workshop")
    docs.extend(name for name, key in (("proposal", "proposal"), ("one-pager", "onePager"), ("linkedin", "linkedin")) if key in data)
    return docs


def validate(data: Any) -> dict:
    """Validate explicit sections; never fill an absent document with invented content."""
    data = _object(data, "brief")
    _known(data, {"company", "label", "status", "title", "subtitle", "audience", "duration", "participants", "learningOutcomes", "timeline", "exercise", "proposal", "linkedin", "onePager", "sourceNote", "brandNote", "preparedBy", "role", "contact", "date", "sources", "lang"}, "brief")
    for field in ("company", "label"):
        _text(data.get(field), field)
    if "lang" in data and not LANG_TAG.fullmatch(_text(data["lang"], "lang")):
        raise SchemaError("lang: use a language tag such as en, zh-Hant-HK or es")
    if "status" in data:  # the trainer's own record; never rendered or embedded
        _text(data["status"], "status")
    for field in ("title", "subtitle", "audience", "duration", "participants"):
        if field in data:
            _text(data[field], field)
    if "workshop" in available_documents(data):
        for field in ("title", "subtitle", "audience", "duration", "participants"):
            _text(data.get(field), field)
        _texts(data.get("learningOutcomes"), "learningOutcomes")
        timeline = _records(data.get("timeline"), "timeline", ("title", "activity"))
        for index, item in enumerate(timeline):
            _known(item, {"minutes", "title", "activity"}, f"timeline[{index}]")
            _number(item.get("minutes"), f"timeline[{index}].minutes", integer=True, positive=True)
        exercise = _object(data.get("exercise"), "exercise")
        _known(exercise, {"title", "brief", "task", "prompt", "modelAnswer", "stretch", "inputs", "checks", "facilitatorNote", "supplierQuotes", "seats", "months", "currency"}, "exercise")
        for field in ("title", "brief", "task", "prompt", "modelAnswer", "stretch"):
            _text(exercise.get(field), f"exercise.{field}")
        _records(exercise.get("inputs"), "exercise.inputs", ("label", "text"))
        for index, item in enumerate(exercise["inputs"]):
            _known(item, {"label", "text"}, f"exercise.inputs[{index}]")
        _texts(exercise.get("checks"), "exercise.checks")
        if "facilitatorNote" in exercise:
            _text(exercise["facilitatorNote"], "exercise.facilitatorNote")
        if "supplierQuotes" in exercise:
            quotes = _records(exercise["supplierQuotes"], "exercise.supplierQuotes", ("id",))
            seen: set[str] = set()
            for index, item in enumerate(quotes):
                _known(item, {"id", "monthly", "setup", "support"}, f"exercise.supplierQuotes[{index}]")
                if item["id"] in seen:
                    raise SchemaError("exercise.supplierQuotes: supplier ids must be unique")
                seen.add(item["id"])
                for field in ("monthly", "setup"):
                    _number(item.get(field), f"exercise.supplierQuotes[{index}].{field}")
                if "support" not in item:
                    raise SchemaError(f"exercise.supplierQuotes[{index}].support: supply a number or null for unknown")
                if item["support"] is not None:
                    _number(item["support"], f"exercise.supplierQuotes[{index}].support")
        for field in ("seats", "months"):
            if field in exercise and exercise[field] is not None:
                _number(exercise[field], f"exercise.{field}", integer=True, positive=True)
        if "currency" in exercise:
            _text(exercise["currency"], "exercise.currency")
    if "proposal" in data:
        proposal = _object(data["proposal"], "proposal")
        _known(proposal, {"eyebrow", "title", "subtitle", "problem", "commercialNote", "nextStep", "signOff", "objectives", "deliverables", "clientInputs", "programme", "possibleNextSteps", "commercial"}, "proposal")
        for field in ("title", "subtitle", "problem", "nextStep"):
            _text(proposal.get(field), f"proposal.{field}")
        for field in ("eyebrow", "commercialNote", "signOff"):
            if field in proposal:
                _text(proposal[field], f"proposal.{field}")
        for field in ("preparedBy", "date"):
            if field not in data:
                raise SchemaError(f"{field}: a proposal shows who sends it and when; ask the trainer "
                                  "once in chat for the name that signs and the date, never fill a placeholder")
        if "possibleNextSteps" in proposal:
            _texts(proposal["possibleNextSteps"], "proposal.possibleNextSteps")
        for field in ("objectives", "deliverables", "clientInputs"):
            _texts(proposal.get(field), f"proposal.{field}")
        _records(proposal.get("programme"), "proposal.programme", ("title", "duration", "output"))
        for index, item in enumerate(proposal["programme"]):
            _known(item, {"title", "duration", "output"}, f"proposal.programme[{index}]")
        if "commercial" in proposal:
            commercial = _object(proposal["commercial"], "proposal.commercial")
            _known(commercial, {"label", "currency", "rows", "terms", "validUntil"}, "proposal.commercial")
            _text(commercial.get("currency"), "proposal.commercial.currency")
            for field in ("label", "terms", "validUntil"):
                if field in commercial:
                    _text(commercial[field], f"proposal.commercial.{field}")
            _records(commercial.get("rows"), "proposal.commercial.rows", ("item",))
            for index, row in enumerate(commercial["rows"]):
                _known(row, {"item", "quantity", "unitPrice", "total"}, f"proposal.commercial.rows[{index}]")
                for field in ("quantity", "unitPrice"):
                    if field in row and row[field] is not None:
                        _number(row[field], f"proposal.commercial.rows[{index}].{field}")
                if row.get("total") is None:
                    raise SchemaError(f"proposal.commercial.rows[{index}].total: an unknown amount does not go "
                                      "in the client document; remove the row and list it for the trainer in chat")
                _number(row["total"], f"proposal.commercial.rows[{index}].total")
    if "linkedin" in data:
        linkedin = _object(data["linkedin"], "linkedin")
        _known(linkedin, {"label", "post", "visualHeadline", "cta"}, "linkedin")
        for field in ("label", "post", "visualHeadline", "cta"):
            _text(linkedin.get(field), f"linkedin.{field}")
    if "onePager" in data:
        one_pager = _object(data["onePager"], "onePager")
        _known(one_pager, {"title", "subtitle", "takeaway", "points"}, "onePager")
        for field in ("title", "subtitle", "takeaway"):
            _text(one_pager.get(field), f"onePager.{field}")
        _records(one_pager.get("points"), "onePager.points", ("title", "text"))
        for index, item in enumerate(one_pager["points"]):
            _known(item, {"title", "text"}, f"onePager.points[{index}]")
    for field in ("sourceNote", "brandNote", "preparedBy", "role", "contact", "date"):
        if field in data:
            _text(data[field], field)
    if "sources" in data:
        _records(data["sources"], "sources", ("title", "url"))
        for index, source in enumerate(data["sources"]):
            _known(source, {"title", "url", "checked"}, f"sources[{index}]")
            if "checked" in source:
                _text(source["checked"], f"sources[{index}].checked")
            if not re.match(r"^https?://[^\s]+$", source["url"], re.IGNORECASE):
                raise SchemaError(f"sources[{index}].url: expected an http(s) URL")
    if not available_documents(data):
        raise SchemaError("brief: supply at least one workshop, proposal, linkedin or onePager section")
    return data


def project_documents(data: dict, documents: list[str]) -> dict:
    """Only explicit shared headers and selected documents reach a standalone file.

    `status` is the trainer's review record and never leaves the JSON.
    """
    shared = {key: data[key] for key in ("company", "label", "sourceNote", "brandNote", "preparedBy", "role", "contact", "date", "sources", "lang") if key in data}
    for document in documents:
        if document == "workshop":
            for key in ("title", "subtitle", "audience", "duration", "participants", "learningOutcomes", "timeline", "exercise"):
                shared[key] = data[key]
        else:
            key = {"proposal": "proposal", "linkedin": "linkedin", "one-pager": "onePager"}[document]
            shared[key] = data[key]
    return shared


def review_wording(payload: Any, path: str = "", subject: bool = False) -> list[str]:
    """Paths and phrases in client-visible text that belong in the trainer's chat reply."""
    found: list[str] = []
    if isinstance(payload, str):
        for pattern in STRUCTURAL_SLOTS + ([] if subject else REVIEW_WORDING):
            match = pattern.search(payload)
            if match:
                found.append(f"{path} ({match.group(0)!r})")
    elif isinstance(payload, dict):
        for key, value in payload.items():
            if key != "url":
                found += review_wording(value, f"{path}.{key}" if path else key, subject or key == "exercise")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            found += review_wording(value, f"{path}[{index}]", subject)
    return found


def safe_json(data: dict) -> str:
    """Data in an inert JSON script may never terminate its containing HTML element."""
    serialized = json.dumps(data, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    for char, escaped in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"),
                          ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        serialized = serialized.replace(char, escaped)
    return serialized


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def brand_css() -> str:
    fonts = SKILL_DIR / "assets/brand/fonts"
    rules = []
    for family, prefix, weight in (("AdaptigPackDisplay", "bricolage-grotesque", "200 800"),
                                    ("AdaptigPackBody", "figtree", "300 900")):
        for subset in ("latin-ext", "latin"):
            uri = data_uri(fonts / f"{prefix}-var-normal-{subset}.woff2", "font/woff2")
            # Extended subset applies outside basic Latin/Latin-1; the Latin file covers
            # the common Western European characters, including Danish æ/ø/å.
            unicode_range = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+2020,U+20A0-20AB,U+2113,U+2C60-2C7F,U+A720-A7FF"
                             if subset == "latin-ext" else
                             "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
            rules.append(f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};font-display:swap;src:url('{uri}') format('woff2');unicode-range:{unicode_range};}}")
    return "\n".join(rules)


def render(data: dict, *, document: str | None = None, single: bool = False,
           documents: list[str] | None = None) -> str:
    validate(data)
    available = available_documents(data)
    selected = available if documents is None else documents
    if not selected or any(name not in available for name in selected):
        raise SchemaError("requested document is absent from the supplied content")
    document = document or selected[0]
    if document not in selected:
        raise SchemaError(f"unknown or absent document {document!r}")
    payload = project_documents(data, [document] if single else selected)
    problems = review_wording(payload)
    if problems:
        raise SchemaError("client-facing text carries review, gap or placeholder wording: "
                          + "; ".join(problems) + ". Review status, open questions and gaps go to "
                          "the trainer in the chat reply, never into the document; reword it or leave it out")
    template = (SKILL_DIR / "assets/workshop-pack.html").read_text(encoding="utf-8")
    replacements = {
        "BRAND_STYLE": brand_css(),
        "WORDMARK_DATA": data_uri(SKILL_DIR / "assets/brand/wordmark.png", "image/png"),
        "PACK_DATA": safe_json(payload),
        "DEFAULT_DOC": document,
        "SINGLE_DOCUMENT": "true" if single else "false",
        "TITLE": html.escape(f"{data['company']} · {DOC_NAMES[document]}"),
        "LANG": data.get("lang", "en"),
    }
    return re.sub(r"@@(BRAND_STYLE|WORDMARK_DATA|PACK_DATA|DEFAULT_DOC|SINGLE_DOCUMENT|TITLE|LANG)@@",
                  lambda match: replacements[match.group(1)], template)


def write_pack(data: dict, output_dir: Path, documents: list[str] | None = None) -> list[Path]:
    """Create only new outputs; preflight every filename before writing any of them."""
    validate(data)
    available = available_documents(data)
    selected = available if documents is None else documents
    if not selected or len(set(selected)) != len(selected) or any(name not in available for name in selected):
        raise SchemaError("--documents must name distinct supplied sections: " + ",".join(available))
    output_dir = output_dir.expanduser().resolve()
    if output_dir == SKILL_DIR or SKILL_DIR in output_dir.parents:
        raise SchemaError("output must be outside the installed skill directory")
    if output_dir.exists() and not output_dir.is_dir():
        raise FileExistsError(f"output path is not a directory: {output_dir}")
    planned = {"index.html": (selected[0], False)}
    planned.update({("one-pager.html" if doc == "one-pager" else doc + ".html"): (doc, True) for doc in selected})
    existing = [str(output_dir / name) for name in planned if (output_dir / name).exists() or (output_dir / name).is_symlink()]
    if existing:
        raise FileExistsError("refusing to overwrite existing output: " + ", ".join(existing))
    rendered = [(output_dir / name, render(data, document=doc, single=single, documents=selected))
                for name, (doc, single) in planned.items()]
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for path, content in rendered:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(content)
        written.append(path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="reviewed JSON brief")
    parser.add_argument("--output-dir", "--out", "--outpath", required=True, type=Path,
                        help="new output directory, or an existing directory without output filenames")
    parser.add_argument("--documents", help="optional comma-separated supplied sections: workshop,proposal,one-pager,linkedin; default: all supplied")
    args = parser.parse_args(argv)
    try:
        if args.input.stat().st_size > MAX_INPUT_BYTES:
            raise SchemaError("input exceeds 2 MiB")
        data = json.loads(args.input.read_text(encoding="utf-8"))
        for path in write_pack(data, args.output_dir, args.documents.split(",") if args.documents else None):
            print(f"SAVED_HTML {path}")
        print("HTML_ONLY — supplied content formatted; no PDF or external publication implied. "
              "Tell the trainer about review status and open points in chat, not in the document.")
        return 0
    except (OSError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
