# Trainer proposal brief and commercial inputs

This version needs no Adaptig account. To see what the trainer keeps at their price, use `pricing-explainer`; its seat fees are never a client price. It does not decide who may bind Adaptig: the trainer supplies the applicable authority and process.

## Brief card

Use only relevant rows. For every answer record **confirmed / proposed / unknown**, with a short source pointer such as supplied call notes, trainer response or approved product document. Do not copy the source record into the client document.

| Field | What to establish |
|---|---|
| Client and reader | Organisation, intended addressee, their role in the decision; no guessed contact details. |
| Situation | First contact, follow-up after discovery, revision before sending, or revision of a sent version. |
| Need | Specific problem, who experiences it, why it matters, desired observable change. |
| Participants | Roles, prior experience, confidence, number or supported capacity, accessibility and language needs. |
| Components | Each proposed workshop/coaching/follow-up component, quantity and relationship to the others. |
| Programme | Outcome, content areas, what participants practise/make, learning check and transfer activity. |
| Exercises | Representative scenario, difficulty paths, safe data, participant output and debrief; label new designs proposed. |
| Materials | What is included: participant sheet, slide content, trainer guide, templates or other specified items; format, owner, delivery and revisions. Do not assume recordings/certificates/platform access. |
| Delivery | On-site/online/hybrid, duration, dates or scheduling approach, venue, platform and time zone. |
| Tools/data | Approved accounts, who provides access, data restrictions and offline/no-access alternative. |
| Responsibilities | Trainer preparation and delivery; client sponsor, room/access, devices, participant briefing and example approval. |
| Pricing | Each line's quantity, unit, the trainer's unit price, currency and the date they gave it. One question when it is missing: "What is your fee for this, and in which currency?" |
| Terms | Sourced tax treatment, expenses, payment, validity, cancellation/rescheduling, content rights or other requested terms. Omit unknown terms from a scope draft rather than invent defaults. |
| Assumptions | Any condition that changes delivery work or price, including customisation and number of review rounds. |
| Output/review | Letter, email or slide outline; language; the version the trainer is reviewing. |
| Sender | The name that signs, role, contact details to show and the proposal date. Ask once when missing; never a placeholder. |

Ask first about audience/need, scope and delivery constraints, then about commercial inputs. At most three focused questions per round. Do not block useful scope work because a price or optional sender phone is unknown. If a draft contains assumptions, show them as proposals for review.

## The trainer's price

For each priced item, use this internal record:

```text
Line:
Quantity and unit:
Unit price and currency:
Includes / excludes:
Source and applicable date:
Given by the trainer on:
Tax treatment:
Discount or complimentary item, if the trainer offers one:
Status: given by the trainer / missing
```

The trainer is independent and sets their own price, so a fee the trainer gives is the price. Do not ask who approved it. Only a trainer who says their own organisation has a sign-off step gets that step recorded. Adaptig's fees, another trainer's fee and the price of a stage someone else delivers are never the trainer's to quote. Never consult private company systems for a price.

- Do not use a different client's amount, a public competitor price, an old offer or a proposed budget as an approved fee.
- Do not add a discount, a complimentary workshop or tax treatment because it sounds reasonable. Ask or omit it.
- An expired or scope-mismatched confirmation needs a current answer. Do not extend validity yourself.
- Inclusions and deliverable quantities must match the programme/materials scope.
- Price forms may be fixed workshop fee, per participant, per cohort or another supplied form. Explain any minimum or quantity assumption supplied with it.
- Alternative packages need separate approved lines and separate totals. Do not add option totals together as if the client buys all options.
- Keep prices in one investment section, with scope elsewhere; a cover email need not repeat them.

## Calculation record

Use `Decimal` or a trusted spreadsheet/calculator. Show quantities × units, approved discounts, tax basis/rate where supplied, expenses and totals as separate steps. Do not invent a rounding rule; ask if supplied values produce ambiguous currency rounding.

Example method only, not a price fixture:

```python
from decimal import Decimal
quantity = Decimal(quantity_text)
unit_price = Decimal(unit_price_text)
line_amount = quantity * unit_price
```

Read the result back against the draft after every changed quantity or price. If currencies differ, show separate currency totals and flag the need for an approved conversion or separate quotes. If no calculation tool is available, label arithmetic unverified and ask the trainer to check it; do not call the draft commercially checked.

## Review record and revisions

Keep this in the chat reply to the trainer, never in the client-facing text:

```text
Proposal / version:
Prepared from:
Status:
Scope confirmed by / still proposed:
Prices sourced from / open inputs:
Totals computed by:
Terms supplied / not included:
Materials and exercises promised:
Client responsibilities:
Brand/template used / layout review state:
Sign-off step, only if the trainer named one:
Name, role, contact and date in the signature:
Trainer's confirmation of this exact version, if given:
Open decisions and who can answer:
Changed since previous version:
```

An unpriced draft may be useful for a scope conversation, but it is not a price offer. Remove unfilled template slots from that copy and put missing decisions and unknown price lines in the review record in chat; an unknown amount never appears in the client document. A priced draft is still a draft until the trainer confirms it. A changed price or scope goes back to the trainer before the client sees it. Never overwrite the supplied sent record or claim it was sent merely because a file exists.
