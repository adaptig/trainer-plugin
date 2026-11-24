---
name: "pricing-explainer"
description: "Explain Adaptig pricing to a trainer and work out the numbers for one workshop. Use when: how does pricing work, what do I pay Adaptig, seat fees, how much is a seat, what should I charge, how much do I keep, what is my margin, price this workshop, Spark pricing, Shift fee, Shape fee, membership fee, free seats, is it worth it for 12 people. Answers in plain words with the trainer's own numbers: what the client pays the trainer, what the trainer pays Adaptig, and what is left."
license: "MIT"
metadata:
  department: "marketing"
  author: "Adaptig"
  version: "1.0.0"
  related: ["workshop-proposal", "warm-outreach"]
  source: "Trainer fees and guidance as told to trainers in the trainer agreement, trainer decks and trainer calls of 2026"
---

# Pricing explainer

Trainers find Adaptig's pricing hard to follow, because two kinds of money get mixed up:
the price a client pays the trainer, and the fee the trainer pays Adaptig. This skill
keeps them apart and does the sum for the trainer's own case. It needs no tools; the
answer is text in the chat.

Read [fees.md](references/fees.md) before answering. Every figure comes from that page.
It starts with Spark, then Shift and Shape; Show and the education workshops are marked
as not settled.

## What the trainer asks, and what to give

| They ask | Give |
|---|---|
| "How does pricing work?", "explain Spark pricing" | **The picture.** Three lines: the client pays you your price; you pay Adaptig a fee (a seat per participant for Spark, a fee per session for Shift and Shape); the difference is yours. Then one worked example with round numbers. |
| "What do I pay Adaptig for 18 people?" | **The fee.** The seat sum for that class, shown step by step, with the free seats they say they have. |
| "I'm charging 6,000 for 25 people, what do I keep?" | **The margin.** The table below, with their numbers. |
| "What should I charge?" | **The guidance, then a question.** Adaptig's guidance range and its date, then ask what the result is worth to this client. Never pick the price for them. |
| "Is it worth it for 8 people?", "small client" | **The break-even.** The fee for that size, what is left at their price, and the cheaper route when there is one (free seats, Spark split into sessions). |
| "What does it cost to be a trainer?" | **The fixed costs.** Membership and certification, and how many paid seats or workshops cover a month of membership at their price. |

## The margin table

Show the working, so the trainer can check it and reuse it.

```
Client pays you:        <their price and currency>
Seats:                  <n> participants
Adaptig seat fee:       <block by block, with the prices from fees.md, each step shown>
Monthly credit:         <minus the monthly credit from fees.md, if they still have this month's three free seats; otherwise none>
You pay Adaptig:        <the fee>
Left for you:           <price minus fee>, before your own costs and tax
```

- For Shift and Shape, replace the seat lines with the session fee: sessions × fee.
- Keep currencies apart. Fees are in US dollars; if the trainer charges in another
  currency, show the fee in dollars, ask once for the rate they want to use, and finish
  the last line when they give it. Do not supply a rate yourself.
- Membership is a monthly cost, not a cost of one workshop. Mention it once, on its own
  line, when the trainer asks what they really keep.
- End with the one line that matters: the platform shows the expected invoice when the
  course link is created, and that figure is the one they are billed.

## Rules

- **Every figure with what it is and its date.** Say "the seat fee you pay Adaptig" or
  "Adaptig's guidance to trainers, June 2026", never "the price".
- **Never invent, round or update a figure.** If it is not in `fees.md`, say it is not
  settled or not on the page, and that Adaptig HQ answers it.
- **A fee the trainer pays is never a client price.** Do not put a seat fee or a session
  fee into anything a client will read.
- **The trainer's price is the trainer's.** Give the guidance and the sum; do not choose.
  Suggest changing the scope before cutting the rate.
- **Adaptig's own price list and other clients' prices are not here** and are not the
  trainer's to quote. The guidance figures on the page help the trainer set their own
  price; give them with their date, as guidance.
- **Newer beats this page.** When the platform, the trainer's agreement or a newer
  message from Adaptig disagrees with `fees.md`, the newer source is right. Say so and
  suggest telling Adaptig through `trainer-feedback`, so the page gets fixed.
- **Arithmetic is checked.** Work each step in the open. With a calculation tool, use it;
  without one, show the steps and say the sum was done by hand.

## What happens next

Offer one next step, once, only when it fits and only when that skill is installed or
attached in this conversation; otherwise name it as another
skill in this plugin:

- They have settled a price for a real client: "Want the proposal drafted with that
  price?" (`workshop-proposal`)
- They are still looking for the client: "Want the message that gets you the meeting?"
  (`warm-outreach`)

Otherwise stop.

## Failure and fallback

No participant count or price: give the picture and the worked example, then ask for the
two numbers. A programme that is not settled (Show, the education workshops): say so and
do not estimate. A question about tax, invoicing rules or the trainer's own contract with
Adaptig: this skill explains fees, it does not interpret an agreement; point to Adaptig HQ.

## Language

Answer the trainer in the language they write to you in. Write anything a client will read in the language the trainer names; when they name none, use the language of their brief or notes.


## Self-Improvement Loop

Suggest one change only when a real run shows a repeatable gap that would change a future run: a figure trainers ask for that the page lacks, or an explanation that still confused a trainer. Never put a real client's price or a trainer's own fee into a suggestion. A changed figure is never taken from a conversation; it goes to Adaptig HQ to confirm and is then changed in `fees.md`.
