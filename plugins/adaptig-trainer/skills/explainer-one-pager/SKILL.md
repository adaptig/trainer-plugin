---
name: "explainer-one-pager"
description: "Make a finished visual one-page pre-workshop agenda, explainer, client leave-behind, workshop handout or info card. Research current claims, write for the reader, and deliver a checked A4 PDF with the independent publisher when available, or a matching editable HTML one-pager through the workshop pack renderer. Show the actual preview where supported. Use when: pre-workshop agenda, agenda for the client, one-pager, one page on, explainer, brief, handout, explain this to a client, summary sheet."
license: "MIT"
metadata:
  department: "content"
  author: "Adaptig"
  version: "0.7.0"
---

# Explainer one-pager

Explain one thing on one page so the reader can understand it and use it. Produce the
actual visual client leave-behind or workshop handout. Use the independent publisher for
a verified one-page A4 PDF, or the companion workshop-pack renderer for a matched HTML
collection. Commercial offers belong in the bundled `workshop-proposal` workflow and the
trainer's current approved commercial process; an explainer is not a price offer.

## Pre-workshop agenda

The page trainers use most is the agenda a client reads before the workshop (step 4 of
the trainer flow, `/adaptig-trainer:agenda`). It is built from the agreed proposal or a
timed plan, not from research: skip the evidence step below. Use the compact sheet with
these parts: title; date, time and place when given; who it is for; three to five things
participants will be able to do; the day at a glance (four to six blocks, each with its
time and one line); what to bring or set up beforehand; and the trainer's name and
contact details in the footer, from their saved details
([trainer-details.md](../brand-voice/references/trainer-details.md)). No prices.

## Intake

Use the context already given. Establish the topic, reader, language, what they should
understand by the end, and preferred layout. Ask for material gaps in one short question.

Choose the layout from the brief: a **compact information sheet** for reference, or a
**visually relaxed info card** with fewer points and a useful diagram. If the choice is
immaterial, use the compact sheet and state that assumption instead of stopping. Build
both only when requested, from one content spine so their facts agree. Reuse permission
already given to create this artifact and its local preview; do not ask again whether to
render it. New unsupported claims still need evidence or must be omitted.

## Evidence and copy

1. Research current claims from primary sources when browsing is available. Record the
   source URL and checked date for each price, version, figure and product claim.
2. Without browsing, use supplied materials. Attribute a claim to its source in the
   reader's terms ("as your IT provider reported"), omit unsupported figures and tell the
   trainer in chat what you could not check. Never invent a statistic or testimonial to
   fill a slot.
3. Write a plain title, a short explanation, three to five useful points and one concrete
   example or next action. Keep source notes readable at the bottom.
4. Use the companion `brand-voice` skill when available. Preserve the user's meaning and
   language. Keep company claims to supplied, approved material; this pack is not a live
   database of Adaptig facts, products or prices.

## What the reader sees

The page is for the client. Review status, open questions, unchecked points and gaps go to
the trainer in the chat reply, never onto the page: no "draft", "for review", "not
approved" or "unconfirmed" labels, and no unfilled `{{SLOT}}`. The publisher rejects a
page that still carries a slot or review wording.

The client may never have heard of Adaptig, and its logo is on the page. The first time
"Adaptig", "Spark", "Shift" or "Shape" appears in the text, give it one plain clause,
using only these meanings (`brand-voice/references/trainer-context.md`,
`warm-outreach/references/selling.md`):

- **Adaptig**: an AI-adoption training company; independent trainers deliver its approved workshops.
- **Spark**: hands-on workshops that give all staff practical AI skills.
- **Shift**: a small group of champions from the client's own team build real use cases and spread them through the business.
- **Shape**: the leadership team sets direction, priorities and the rules for AI.

No claims about how other organisations buy. Put the trainer's name, and contact details
only as the trainer gave them, in the footer; never a placeholder.

## Build with the bundled assets

Locate this skill directory from the installed copy. Its `adaptig-brand/` and `tools/`
are self-contained. Read `adaptig-brand/RULES.md` before using its template.
Use bundled `branding-guidelines` for the overall logo, colour, icon and co-branding
rules; its rules and this local renderer's asset snapshot should stay consistent.

Work in a writable scratch/output folder outside the installed skill. Copy
`adaptig-brand/layout/template.html`, fill its slots (including `{{LANG}}`, the page's
language tag such as `en` or `zh-Hant-HK`), and remove unused sections and
unfilled placeholders. Leave the template's `../adaptig-brand/...` references intact:
the publisher resolves them against the bundled pack at render time.

- Compact sheet: clear rows and labels. Info card: more space and one explanatory figure.
- Render diagrams from code, such as inline SVG. Use real bundled logo and shape files.
- Tool names may appear in type. A third-party logo requires the vendor's real asset and
  never implies a partnership.
- Exactly one A4 page. Cut content when it overflows; never shrink type below the template.
- This is a snapshot of the existing Adaptig visual system. If newer approved brand
  guidance is supplied, use it and tell the trainer in chat which assets still await an
  update.

## Match a workshop collection

When the request includes a workshop preview, proposal or social post and asks for a
matching one-pager, use the companion `training-materials` [artifact schema](../training-materials/references/artifact-schema.md)
and [renderer](../training-materials/tools/render_pack.py). Supply the supported `onePager`
content and shared audience-appropriate metadata. The renderer supports a one-pager on
its own or selected document combinations; use `--documents one-pager` for that artifact
alone. It produces `one-pager.html` with embedded fonts, logo and styles, plus the selected
collection's index. Keep the editable JSON and HTML, and show the actual artifact through
the host's preview surface when available.

Keep the one-pager concise, with a clear title, three to five useful points, one concrete
takeaway and readable source notes where needed. Do not invent other document content to
fill the collection. Standalone exports contain only their own content and approved shared
metadata; inspect the export before sending it to a different audience.

The matched HTML layout is not a page-count-verified A4 PDF. For a requested checked
one-page PDF, use this skill's independent publisher below, or export through a supported
tool and verify the page count and visible layout. The full plugin includes the sibling
renderer; this skill's individual ZIP keeps its own independent publisher and assets but
does not include `training-materials`. If the sibling is missing, use this local publisher
or identify the missing collection renderer. Do not claim an unavailable renderer ran.

## Render and check

With Python 3.10+ and a local Chromium-family browser available:

```bash
python3 <skill-directory>/tools/publish.py --topic "<topic>" --labels sheet --out "<output-folder>" "<sheet.html>"
```

For two versions, use `--labels sheet,card` followed by the two HTML paths. For an info
card alone use `--labels card`. Quote paths. Use `--out` to select a folder available to
the user; without it the publisher detects Downloads or the supported host's output folder.
The script uses Python's standard library and an existing browser; it installs nothing.
It fails fast: each browser launch gets 20 seconds and the whole run under a minute. A
browser that hangs is skipped, the next Chromium-family browser is tried, and when none
works the page is handed over as HTML.

Read the publisher's output:

| Result | Meaning and next action |
|---|---|
| `SAVED` | Rendered PDF passed the one-page check. Inspect it before delivery. |
| `REJECTED` | No deliverable was published. Cut content, or fill or remove the slot or review wording it names, and render again. |
| `FALLBACK` + `MESSAGE` / `NO_BROWSER` | No working browser (none found, or none finished in time). The HTML, with the brand embedded, is in the folder; it is not a checked PDF. Pass the `MESSAGE` line to the trainer as written: open the file in a browser and choose Print > Save as PDF. |

Check the final page visually where the host supports it: no clipped text, overlapping
logo, tiny sources, unresolved placeholders or misleading diagram. The page-count gate
alone does not detect content clipped inside a fixed-height box. Without a visual preview,
state that layout review remains pending. Do not claim that an HTML fallback is a finished PDF.

If Python/browser execution is unavailable but file writing works, create a complete
self-contained visual HTML one-pager with the supported tools and identify the actual
format. If file and rendering tools are both unavailable, return complete editable text
and explain that a designed file/PDF could not be created in this host. Do not describe
Markdown as a finished visual one-pager or claim a file was created or saved.

## Delivery and boundaries

Lead with the actual one-pager preview where the host supports it, then give its working
file link, actual format, editable source and inspection status. Rendering a local preview
is part of the requested creation, not an external publication. Preserve existing files;
the independent publisher adds a numeric suffix, and the workshop renderer requires a
new output folder. Do not launch an external desktop application automatically or delete
earlier attempts.

Client names, identifiable quotes and logos require the trainer's confirmed permission
for the intended audience. Reuse clearance already established; otherwise use anonymous
descriptions while preparing the draft. No pricing, contract promises or invented outcomes.
Never send, post or publish the result unless the user explicitly requests that action.

## Language

Answer the trainer in the language they write to you in. Write anything a client will read in the language the trainer names; when they name none, use the language of their brief or notes. [languages.md](../brand-voice/references/languages.md) says how to choose it, how to write Traditional Chinese (Hong Kong), and how to set the language of a file.


## Self-Improvement Loop

Propose a change only when a run reveals a repeatable problem that would change future
behaviour. Suggest it for the source repository; never silently edit an installed snapshot.
