# Adaptig visual snapshot for trainer handouts

This pack uses Adaptig's brand assets and palette.

## Colour and type

The six source colours are defined in `tokens.css`: Paper Beige `#f9f5ea`, Charcoal
Black `#212124`, Orange Peel `#fa5929`, Aqua Blue `#0a66db`, Leaf Green `#30966b`, and
Sky Blue `#abc9f5`. Use one dominant background with deliberate accents. On charcoal,
text is paper beige. Do not sample replacement colours from screenshots.

The pack renders with Bricolage Grotesque for display and Figtree for body, existing open
font substitutes for portable collateral. Their SIL Open Font License notices ship in
`fonts/`. Proxima Nova is not bundled: this pack does not grant redistribution rights
for that commercial typeface. A supplied, licensed design may use it separately.

Use the type ladder in `tokens.css` and weight for emphasis. If content overflows, cut
content before changing size. CJK text falls through to the system fonts in the stack;
check missing glyphs before handing over a multilingual file.

## Logo and shapes

Use `logo/adaptig-wordmark.png` as supplied. Never redraw, stretch or recolour it. Keep
clearspace around the mark. The two light-blue shapes included here are real source
assets: `asterisk.png` and `quatrefoil.png`. Use at most one per page, behind the content,
cropped on a curved edge. Other shapes are not included in this starter pack.

For third-party marks, use the vendor's actual supplied/official file with appropriate
usage rights or set the name in text. A mark identifies a tool, not an endorsement.

## Page and delivery

Use `layout/template.html` and `layout/one-pager-a4.css`. All output must be one A4 page
with readable source notes. Keep the `../adaptig-brand/` paths when writing scratch HTML;
`tools/publish.py` rewrites them to this pack during rendering. Remove all unused slots.

The Python publisher uses a local Chromium-family browser, checks the PDF page count,
and preserves existing files. It gives each browser 20 seconds and the run under a
minute; when no browser works it returns embedded HTML and a one-line message telling the
trainer to open it and choose Print > Save as PDF. It rejects a page that still carries a
`{{SLOT}}` or review wording.
HTML is source, not a checked PDF. Inspect the rendered output for clipping and overlap;
a one-page PDF can still have a layout defect. Render headlessly and report where the file
was actually delivered.

Logos and shapes remain Adaptig brand assets. Their inclusion lets trainers prepare
Adaptig partner material; it is not a grant to register, resell or create a new
identity from the marks.
