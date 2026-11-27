# Social layouts

Five templates, one CSS file and one fit script, for a LinkedIn or Instagram image.
Copy a template into a scratch folder, replace the `{{SLOTS}}`, leave the
`../adaptig-brand/...` links alone (the publisher rewrites them to this pack at render
time) and render with `tools/publish.py --png`.

| Template | Look | Use |
|---|---|---|
| `takeaways.html` | numbered rows on paper, one shape | **the default when there is no photo**: a single image with up to three points |
| `cover.html` | full-bleed photo, charcoal band | a single image with a photo the trainer may use; carousel cover |
| `framed.html` | paper frame, inset photo | quieter posts, portrait photos |
| `split.html` | photo beside a paper panel | posters and other material |
| `closing.html` | charcoal, wordmark | last slide of a carousel |

`cover`, `framed` and `split` need a photo. Without one, use `takeaways`.

Slots: `{{LANG}}` (`en`, `zh-Hant-HK`, `es`…), `{{TITLE}}`, `{{SIZE_CLASS}}` (empty for
4:5, `square` for 1:1), `{{PHOTO_SRC}}` (absolute `file:///…` path to the trainer's photo,
untouched), `{{FOCAL}}` (CSS background-position, e.g. `68% 50%`: the only edit the photo
ever gets), `{{KICKER}}`, `{{HEADLINE}}`, `{{SUBLINE}}`, `{{COUNTER}}` (`2 / 3`; delete
the element for a single image), `{{ITEM_1..3}}` (delete unused rows).

`fit.js` shrinks the headline to a floor of two-thirds its size and then marks the page
`data-overflow="1"`; the publisher refuses such a page. Cut words, never the floor.
