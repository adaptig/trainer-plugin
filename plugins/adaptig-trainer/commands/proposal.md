---
description: Step 3 of 7. Write a workshop proposal. Turn your meeting notes or the client's brief into a proposal they can read and sign, at your own price.
argument-hint: "[your notes, the client's brief, or an earlier proposal to revise]"
---

The trainer wants a proposal. What they gave you: $ARGUMENTS

Use the `adaptig-trainer:workshop-proposal` skill to turn their notes into a finished proposal the client can read.

- **Text first.** Give the full proposal text in the chat before anything else.
- **One round of questions, at the end.** If the fee is missing, or the trainer's details are not saved yet (the `trainer-details.md` reference the skill links to), ask for all of it in one message at the end of that reply, never one question at a time. Saved details are used without asking.
- **Language.** Write in the client's language (the `languages.md` reference the skill links to). When it is unclear, offer "English or Traditional Chinese (Hong Kong)? Any other language works too." in that same question.
- **Price.** The price is the trainer's own; never invent one. If they want to know what they keep, use the `adaptig-trainer:pricing-explainer` skill; that fee never goes into the proposal.

If they give you an earlier proposal with changes, revise it and open with what changed.

When it is done, give the trainer the proposal, anything they still need to fill in, and the next step: "Once they say yes: step 4, the agenda they read before the day: `/adaptig-trainer:agenda`".

Contracts are not part of this version; if they ask for one, say so and suggest they ask Adaptig.
