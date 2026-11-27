---
name: "linkedin-workshop-post"
description: "Create a finished LinkedIn workshop post and an image to upload with it, for an announcement, practical lesson, session recap or trainer perspective. Use real workshop facts, the trainer's voice and one clear action. Gives the paste-ready text first, then renders a branded PNG by default when file tools and a browser are available."
license: "MIT"
metadata:
  department: "marketing"
  author: "Adaptig"
  version: "0.7.0"
---

# LinkedIn workshop post

Help a trainer make their work visible and invite a useful next conversation. Produce one finished post: the paste-ready text in the chat first, then an image to upload with it (a PNG), by default, when file tools and a browser are available. Name what was actually created. Draft only; do not post, schedule, tag accounts through a tool, send messages or start an engagement campaign.

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

For the image, use the trainer's permitted photo or the photo-free layout below. Include alt text and check its actual exported dimensions and readability. Use current approved brand assets, never a fabricated client endorsement, audience photo or logo. A concise brief can guide the work but does not replace the requested graphic. Do not claim a PNG or carousel exists unless those files were generated and checked.

Apply `branding-guidelines` for colours, logo placement, type, shapes and the supplied
utility icons. The base plugin includes these files; another brand plugin is not required.

## Make the image

The image is made from the bundled social layouts in the sibling `explainer-one-pager`
skill: `../explainer-one-pager/adaptig-brand/layout/social/`. Read its `README.md` first.

1. **Pick the layout.** No photo, or no permission to use one: `takeaways.html`, with a
   kicker, a short headline and up to three points. A photo the trainer may use:
   `cover.html`. Size 4:5 (1080×1350) unless the trainer asks for a square.
2. **Fill it.** Copy the template into a scratch folder outside the plugin. Fill every
   slot: `{{LANG}}` with the post's language tag (`en`, `zh-Hant-HK`…), a headline of a
   few words taken from the post, the points from the post's real facts. Delete the
   counter element and any unused rows. Leave the `../adaptig-brand/...` links as they are.
3. **Render it** with the publisher:

   ```bash
   python3 "<this skill's folder>/../explainer-one-pager/tools/publish.py" --png --topic "<topic>" "<filled.html>"
   ```

   `SAVED <path>` is a checked PNG at the exact size. `REJECTED` means the headline did not
   fit: cut words, never the type, and run again. `FALLBACK` means no browser worked: pass
   on its `MESSAGE` line, which tells the trainer to open the HTML and take a screenshot.
4. **Look at it** before handing it over: no clipped words, the logo and shape in place,
   readable on a phone. A Chinese image on Linux needs the font check in
   [languages.md](../brand-voice/references/languages.md).

Show the PNG through the host's preview when there is one, with its path and alt text.
Never claim an image exists unless `SAVED` named it. A text preview of the post
(`linkedin.html` from the workshop pack renderer) is only for when the trainer asks for
the whole workshop pack.

## Deliver

Return one finished post: the paste-ready text, then the actual image, not an automatic menu of alternatives. Include the requested graphic only when it exists, with alt text and its actual file format. Below the artifact, list only unresolved facts/permissions and the inspection status. No placeholders in a post described as ready to publish. Complete requested visuals before suggesting another step.

## Failure and fallback

No image permissions: use the photo-free layout; do not block writing the post. No working browser: hand over the publisher's HTML and its message (open it, take a screenshot). No native preview: give the PNG's path and say the host could not display it inline. No file tools: deliver the complete post text, say no image could be made in this host, and give a one-line image idea the trainer can make themselves. An unresolved logistical detail becomes an interest-check draft rather than an invented announcement.

## Language

Answer the trainer in the language they write to you in. Write anything a client will read in the language the trainer names; when they name none, use the language of their brief or notes. [languages.md](../brand-voice/references/languages.md) says how to choose it, how to write Traditional Chinese (Hong Kong), and how to set the language of a file.


## Self-Improvement Loop

Suggest one change only when a real use reveals a reusable problem. Keep examples synthetic or anonymized. Do not silently edit installed files, file an issue or publish the post.
