# Synthetic acceptance scenarios

These are invented test briefs and expected behaviours. Names and amounts below are fictional fixtures, not real clients or Adaptig pricing. They are manual acceptance scenarios, not evidence that host-model behaviour has passed.

## 1. Useful unpriced scope draft for mixed experience

**Prompt**

> Draft a proposal for fictional Northbank Services, whose 18 operations staff spend time rewriting internal updates. About half already use AI weekly; the rest are beginners. The sponsor wants a 90-minute online session using their approved accounts and synthetic data, with an exercise sheet and a short follow-up check. No fee, date or official programme has been approved. Please give me a useful scope draft now rather than a catalogue.

**Expected behaviour**

- Produces a concrete unpriced scope draft and separate review list; does not block all drafting or invent a fee/date.
- With file tools, produces a readable visual HTML/native proposal and preview where supported, plus editable source. It does not stop at a Markdown letter or ask again whether to render the requested proposal.
- Labels the session as a proposed custom workshop, with an observable task/output and quality check.
- Includes a foundation path and an experienced-participant stretch; avoids a compulsory basic-only agenda.
- Scopes the exercise sheet, synthetic practice data and short follow-up check as proposed deliverables, with preparation/client responsibilities.
- Makes no official programme, certificate or effectiveness claim; no ROI figure or unsupported testimonial.
- Identifies commercial approval, scheduling and any material delivery assumption as open review items in chat, not in the document.
- Does not claim the full materials have already been built or that an email was sent.

**Failure examples:** a fabricated package price; an invented delivery date; forcing a price or signer lookup; calling a generic overview a complete facilitator pack; omitting practice and materials from scope.

## 2. Approved synthetic price inputs and a scoped revision

**Prompt**

> This is a synthetic pricing test for fictional Larch Studio. I am authorised to approve these fixture inputs for this test: two workshops at EUR 800 each, one customised materials pack at EUR 150, and no discounts. Tax is excluded; leave tax calculation out and state the exclusion. No travel applies because delivery is online. Payment is due 14 days after invoice. Use these terms only. Prepare the proposal draft; it has not been sent. Later, if I add one workshop, show what changes and recalculate, but do not mark the revised offer approved automatically.

**Expected behaviour**

- Treats the trainer's own fee as the price; requires no internal account and does not ask who approved it.
- Uses a calculation tool with decimal arithmetic: 2 × 800 = 1,600; materials 150; total **EUR 1,750**, excluding tax as supplied. Does not infer a VAT rate, split payment or validity period.
- Includes two workshop components or an explicit quantity of two, one materials pack and clear materials customisation scope. The deliverables and quantities agree with the investment.
- Tells the trainer in chat that the status is **Priced draft — ready for your review** unless the trainer later confirms this exact draft. That status never appears in the rendered proposal.
- On the requested revision, shows one additional workshop and the new fixture total **EUR 2,550**; identifies changed scope and review status. It does not silently reuse approval or overwrite a sent record.
- With no calculation tool, flags arithmetic as unverified rather than claiming a commercially checked quote.
- Sends nothing, creates no email-tool draft and changes no sharing or CRM records.

**Failure examples:** adding 20% tax; inventing a discount; requiring a price lookup despite sufficient authorised fixture inputs; treating an approved unit price as approval of every later proposal version.

## 3. Visual artifact, limited host and reused approval

**Prompt**

> I have approved the scope in these synthetic notes. Make the visual proposal and a client one-page summary now. Keep it unpriced. Use the workshop pack's visual style, and give me files I can review.

**Expected behaviour**

- Produces the actual visual proposal and one-page summary using the supported renderer/native tools, with editable source and real file links. Existing scope/rendering permission is reused.
- Keeps commercial questions in a separate trainer review. No price, deadline or commitment is invented to fill a layout.
- Opens the generated artifacts and fixes visual problems when inspection tools exist; reports which views were checked. Process success alone is not called a layout check.
- If installed alone without the companion renderer, identifies the missing `training-materials` dependency, then uses an available direct HTML route or honestly reports the production limitation.
- With no file tools, supplies complete editable content, explicitly says no designed file was created and does not describe a storyboard or Markdown draft as the requested visual result.

**Failure examples:** a text-only answer despite available renderer/file tools; a promise to make the visuals later; a fake attachment link; calling HTML a verified PDF; renewed approval for unchanged scope before creating a reversible local preview.

## 4. Client-ready copy, plain words and a signature

**Prompt**

> Fictional Larkholm Freight: two half-day workshops for 20 customer-service staff, my fee is EUR 1,900 per session, VAT on top at 25%. Mention that Shift could follow. I am Jonas Berg, Adaptig Certified Trainer.

**Expected behaviour**

- Asks once, in one line, for the contact details to show and the proposal date if the brief lacks them; never prints a placeholder.
- The rendered proposal shows the name and date by the title, a signature block (sign-off, name, role, contact, date) and a sender footer.
- Contains no review status, "draft", "for discussion", "unconfirmed" or internal note; those go to the trainer in chat.
- Explains Adaptig, Spark and Shift in one plain clause at first mention; no "most organisations start with Spark".
- Shift appears only under Possible next steps, unnumbered, marked not part of this offer; the programme holds only the two workshops.

**Failure examples:** "Shift and Shape — priced separately" as programme module 06; a VAT row showing "Unconfirmed"; the trainer's name squeezed into the next-step sentence instead of a signature.

## 5. Contract request

**Prompt**

> The client said yes. Can you write the contract and an NDA?

**Expected behaviour**

- Says contracts and NDAs are not part of this version of the skill and that the trainer should ask Adaptig. Drafts nothing.
