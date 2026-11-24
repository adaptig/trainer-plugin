---
name: "linkedin-workshop-post"
description: "Create a finished LinkedIn workshop post draft and readable visual post preview for an announcement, practical lesson, session recap or trainer perspective. Use real workshop facts, the trainer's voice and one clear action; render a preview by default with file tools, and an accompanying graphic when requested and supported."
license: "MIT"
metadata:
  department: "marketing"
  author: "Adaptig"
  version: "0.6.0"
---

# LinkedIn workshop post

Help a trainer make their work visible and invite a useful next conversation. Produce one finished post draft plus a readable visual post preview by default when file tools are available. If an accompanying graphic is requested, make the graphic with supported tools instead of stopping at an image brief. A post preview and an uploadable graphic are different artifacts; name what was actually created. Draft only; do not post, schedule, tag accounts through a tool, send messages or start an engagement campaign.

## Collect the facts once

Use the supplied notes and approved offer. Identify the post's purpose: announce a workshop, teach one useful thing, share a real observation after delivery, or explain the trainer's own perspective. Ask in one batch only for missing facts that matter: audience, actual workshop details, booking route, language and the trainer's own sentence about why it matters.

For an announcement, distinguish a confirmed public date/venue from a proposed one. If not confirmed, write an interest-check post without inventing logistics. For a recap, use what actually happened. If the workshop has not run, do not write a past-tense success story.

## Write

1. Choose one shape from [post-templates.md](references/post-templates.md). One point, a concrete detail, one action.
2. Use `brand-voice` when available. Write as the individual trainer. Use "Adaptig Certified Trainer" only if their certification is confirmed; never speak as company leadership or imply that a new workshop is approved.
3. Start from their words. Ask for a short sample if they want close voice matching and none exists. Do not invent a personal anecdote, conviction, client result or participant reaction.
4. Use a specific task or practical example. The source trainer social templates favour useful demonstrations, workshop announcements and grounded recaps. Personalize any shared post-hub draft so trainers do not publish identical accounts of experiences they did not have.
5. Keep it readable on a phone: a direct opening, short paragraphs, one clear call to action, zero to three relevant hashtags only if useful. Avoid hype, hashtag piles and manufactured scarcity. Do not force the same formula onto every post.
6. Check claims. Prices, booking links, dates, remaining seats and certificates need current supplied facts and relevant authority. Do not quote company track-record numbers from memory. Omit an unsupported number rather than turn it into a confident claim.

## Photo, quote or certificate

Reuse permissions already established for this audience. If people in a photo or a named client are not cleared for public use, draft with a neutral description and propose a text-only visual. Do not require a photo to write the post. Use the trainer's real image; do not invent a workshop crowd or participant quote.

For a quote, use the person's actual words and the permitted attribution/channel. Anonymous evaluation feedback is not automatically a public testimonial. A separate permission-request draft can be offered; do not send it.

A certificate post may use an actual issued certificate after checking personal information is suitable to share. A request to add a trainer name to a certificate goes to the approved issuing process; this skill cannot issue, edit or validate credentials. A visual brief should not imply certification the trainer has not confirmed.

If image work is requested, use the supplied permitted photo or create a simple typographic graphic with supported design/image tools. Include alt text and check its actual exported dimensions and readability. Use current approved brand assets, never a fabricated client endorsement, audience photo or logo. A concise brief can guide the work but does not replace the requested graphic. Do not claim a PNG or carousel exists unless those files were generated and checked.

Apply `branding-guidelines` for colours, logo placement, type, shapes and the supplied
utility icons. The base plugin includes these files; another brand plugin is not required.

## Render the post preview

Use the companion [artifact schema](../training-materials/references/artifact-schema.md) and [pack renderer](../training-materials/tools/render_pack.py) to create `linkedin.html` from the supplied post content. Follow the schema's actual command, document-selection rules and fields. A post-only request needs a post preview; do not invent an unrelated workshop agenda or proposal to create additional artifacts. Supported native visual tools may replace this route when they produce the requested preview.

The preview should show the draft as readable post copy with its paragraph breaks and a clear draft label. Include an approved image and alt text with supported tools if requested; the base pack renderer is a text preview and does not generate an uploadable image. Never invent likes, comments, participant reactions or an account identity. It is a preview, not proof of a LinkedIn publication or pixel-exact LinkedIn rendering.

Show the artifact through the host's visual surface when available and supply the actual file link. Inspect phone-width reading, paragraph spacing, text wrapping, contrast and any image crop; fix problems before handover. Keep copy as selectable text, with a plain-text version the trainer can paste. Preserve the JSON/HTML source for revisions. Creating this local preview is included in the request; reuse existing approval and do not ask again whether to render it.

The renderer is bundled in the sibling `training-materials` skill in the full plugin. An individual LinkedIn skill ZIP does not contain that sibling. If it is missing, identify the dependency and use an approved sibling installation or write a self-contained HTML preview directly when file tools permit. Never claim unavailable image or renderer tools were used.

## Deliver

Return one finished draft with paste-ready text and the actual visual preview, not an automatic menu of alternatives. Include the requested graphic only when it exists, with alt text and its actual file format. Below the artifact, list only unresolved facts/permissions and the inspection status. No placeholders in a post described as ready to publish. Complete requested visuals before suggesting another step.

## Failure and fallback

No image permissions: use a text-only preview; do not block writing the post. No image-generation/export tools: provide the visual preview and clearly mark any requested graphic as not produced. No native preview: deliver the HTML file and state the host could not display it inline. No file tools: deliver complete post text, explain that no visual preview could be made and supply an image brief only as an explicitly unfinished production aid. An unresolved logistical detail becomes an interest-check draft rather than an invented announcement.

## Language

Answer the trainer in the language they write to you in. Write anything a client will read in the language the trainer names; when they name none, use the language of their brief or notes.


## Self-Improvement Loop

Suggest one change only when a real use reveals a reusable problem. Keep examples synthetic or anonymized. Do not silently edit installed files, file an issue or publish the post.
