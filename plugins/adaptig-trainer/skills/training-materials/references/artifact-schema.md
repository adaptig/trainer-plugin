# Visual workshop pack input

The renderer formats supplied, reviewed content. It makes no model calls, performs no
research and grants no company approval. Keep real client inputs in the trainer's private
work folder, never in the distributed skill.

```bash
python3 <skill-directory>/tools/render_pack.py --input content.json --output-dir artifacts
```

Python 3.10+ and its standard library are sufficient. It creates `index.html` plus
`workshop.html`, `proposal.html`, `one-pager.html` and `linkedin.html` only for the
corresponding supplied and selected document sections. Tabs show
only supplied documents. All fonts,
styles and the genuine Adaptig wordmark are embedded; no online assets or runtime APIs
are required. The folder must contain none of those filenames. Existing output is never
overwritten; choose a new folder for a revision. Nothing opens automatically.

**Everything rendered is client-facing.** Review status, open questions, gaps and
unknown amounts go to the trainer in the chat reply, never into the JSON fields that are
shown. The renderer rejects text that carries review, gap or placeholder wording (such as
"ready for your review", "priced draft", "draft material", "not approved curriculum", a
field that is just "Unconfirmed", a trailing "— unconfirmed" or "(proposed)" tag, "TBD",
`{{SLOT}}` or `[CLIENT]`) and names the field; reword it or leave it out. The exercise's
invented scenario is exempt from the status and gap wording only.

Only `company` and `label` are required globally. Supply one or more complete
document sections; workshop fields are required only when `exercise`, `timeline` or
`learningOutcomes` is present. Every required text field must contain non-empty text.
Leave an unknown optional field out; for a required one, write what is known in the
client's terms ("About 12 people per group") and list the gap for the trainer in chat.
Do not invent an answer. An array must have at least one item.
Use `--documents proposal` or a comma-separated selection such as
`--documents workshop,one-pager` to output a subset of supplied documents. A proposal-only,
LinkedIn-only or one-pager-only input needs no dummy workshop. Each standalone document
embeds only its own section plus the shared header/metadata, never other documents or their
private commercial details. The multi-document index embeds its selected content.

No renderer validation can establish that input facts or commercial terms are correct.

## Required JSON fields

| Field | Shape / purpose |
|---|---|
| `company`, `label` | Text. The client organisation, and one client-facing context line shown under it, such as `Workshop proposal for Anna Example, Operations Director`. For a fictional demo, say so in `label`. Never a review status. |
| `status` | Optional text. The trainer's own review record. It is never rendered or embedded in any HTML; report the status to the trainer in chat. |
| `lang` | Optional. The language tag of the client-facing text: `en` (the default), `zh-Hant-HK`, `es`… It sets the page language, so the browser picks the right glyphs, and a `zh` tag also prints the pack's own headings ("Investment", "Prepared by"…) in Traditional Chinese. |
| `title`, `subtitle` | Workshop only. Text. Workshop title and reader-oriented explanation. |
| `audience`, `duration`, `participants` | Workshop only. Text, including units, written for the reader. For example `3 hours 30 minutes, including a break`, `About 12 people per group`. |
| `learningOutcomes` | Workshop only. Array of outcome strings. |
| `timeline` | Workshop only. Array of `{ "minutes": positive_integer, "title": text, "activity": text }`. This describes a proposed agenda; the visible total is computed from these items. |
| `exercise` | Workshop only. Object described below. |
| `proposal` | Optional object described below. |
| `linkedin` | Optional `{ "label": text, "post": text, "visualHeadline": text, "cta": text }`. The label must distinguish a proposed invitation from a delivered-workshop recap. No automatic posting. |
| `onePager` | Optional `{ "title": text, "subtitle": text, "points": [{ "title": text, "text": text }], "takeaway": text }`. |

### Exercise

Required text: `title`, `brief`, `task`, `prompt`, `modelAnswer`, `stretch`.
Required arrays: `inputs: [{ "label": text, "text": text }]` and `checks: [text, ...]`.

`modelAnswer` is a **sample answer supplied by the author**, not an AI answer generated
by the renderer. Do not describe a worked example as evidence from an actual client.
Learner mode starts with the answer hidden. Facilitator mode and the explicit sample-answer
button reveal the sample answer and optional facilitator note. Success checks and the
stretch path remain visible to learners before reveal. If an answer is unknown, label it
as such. Answers are embedded in the HTML: this is a teaching reveal, **not access control**
or a secure facilitator file. For a participant export that must not contain an answer,
replace it in the supplied content with a truthful note such as `Held by the trainer`.

Optional: `facilitatorNote` (text), `supplierQuotes` (below), `seats`, `months`, `currency`.
The facilitator note holds coaching cues and answer notes. Rehearsal status, untested tool
steps and open checks go to the trainer in chat, not into the note.

```json
{
  "supplierQuotes": [
    { "id": "Fictional supplier A", "monthly": 20, "setup": 100, "support": null },
    { "id": "Fictional supplier B", "monthly": 18, "setup": 200, "support": 50 }
  ],
  "seats": 10,
  "months": 12,
  "currency": "fictional cost units"
}
```

This optional table is an illustrative calculator. `monthly` is cost **per seat per
month**; `setup` is a one-off cost; `support` is a single cost for the entire comparison
period. Values must be finite, non-negative JSON numbers. `support: null` explicitly
means unknown, not zero. `seats` and `months` must be positive integers when supplied.
Missing counts start blank; the calculator requests them rather than assuming one.
Unknown support produces a **known subtotal**, never a complete-cost claim or a supplier
recommendation. Taxes, currency conversion, discounts and other costs are not invented.
`currency` defaults to the honest label `cost units` if absent.

### Proposal

Required text: `title`, `subtitle`, `problem`, `nextStep`.
Required string arrays: `objectives`, `deliverables`, `clientInputs`.
Required `programme`: array of `{ "title": text, "duration": text, "output": text }`.
Only what this offer delivers goes in `programme`; it is numbered as the client's programme.
Required metadata: top-level `preparedBy` and `date` (below). The renderer refuses a
proposal without them, so ask the trainer once in chat rather than invent them.

Optional:

- `eyebrow` (text): the small line above the title; defaults to `Workshop proposal`.
- `commercialNote` (text): client-facing price and terms wording beyond the table, such
  as `Fixed fee per session, excluding 25% VAT. Travel within Aarhus is included.` For an
  unpriced proposal, one plain sentence such as `I will send the price once we have agreed
  the scope.` Never a review status.
- `possibleNextSteps` (array of text): later stages that are not part of this offer,
  shown unnumbered under "Possible next steps" after the programme and price, such as
  `Shift, where a small group of champions from your own team build real use cases and
  spread them through the business. Not part of this offer; priced separately if you want it.`
  Give each Adaptig term its plain explanation the first time it appears.
- `signOff` (text): the closing line above the signature, in the client's language, such
  as `Kind regards`. Do not repeat the sender's name in `nextStep`; the signature carries it.

The renderer never calculates a workshop price from exercise data.

### Optional structured commercial table

`proposal.commercial` needs `currency` (text) and `rows`, and may contain `label`
(defaults to `Investment`), `terms` and `validUntil` (text). Each row has `item` (text) and
`total` (a finite non-negative number), plus optional `quantity` and `unitPrice` (numbers,
or null where they do not apply, such as a VAT line; those cells stay blank). A line whose
amount is not known yet does not go in the client document: leave the row out and list it
for the trainer in chat. The renderer rejects a row without a `total`. `total` is a
supplied, checked line total; the renderer does not infer tax, calculate a binding fee or
correct commercial arithmetic. Verify totals before supplying them. `terms` and
`validUntil`, when supplied, are shown in full. Put no approval notes in displayed content.

## Optional metadata

- `preparedBy` (the name that signs), `role` (such as `Adaptig Certified Trainer`),
  `contact` (email and phone as the trainer gave them, for example
  `lena@example.com · +45 00 00 00 00`) and `date`: non-empty text if supplied. The
  date shows in the header; the sender line (name, role, contact, date) shows in the
  footer of every document. A proposal also shows the name and date beside the title and
  a signature block (sign-off, name, role, contact, date) under `nextStep`. Omit what the
  trainer has not given; never print a placeholder.
- `sourceNote`, `brandNote`: client-facing footer text if supplied, such as
  `Built from our call on 17 November 2026`. Nothing appears when they are absent.
- `sources`: non-empty array of `{ "title": text, "url": "https://..." }`. URLs are
  validated as http(s) and appear as source links; no page is fetched by the renderer.
- Unrecognized fields at every object level are rejected. Remove private notes, secrets,
  contact lists and unsupported keys before rendering. Shared metadata appears in every
  selected document; keep it suitable for each one's audience.

The existing brand snapshot uses Paper Beige, Charcoal Black, Orange Peel and Aqua Blue.
Open-font substitutes Bricolage Grotesque and Figtree ship under their bundled OFL notices.
The commercial Proxima Nova font is not included. Dark mode follows the viewer's system;
print uses the light paper palette and the currently selected document. Long content may
need editing before export. HTML output is not a page-count-validated PDF.

The template root is `adaptig-workshop-pack`. Its UI styles are scoped to that root;
custom font-face names avoid collisions when it is embedded. The script locates this root
by ID, reads the inert JSON payload beneath it and uses DOM `textContent` for content.
Use one instance per containing document, or isolate instances in separate frames.
