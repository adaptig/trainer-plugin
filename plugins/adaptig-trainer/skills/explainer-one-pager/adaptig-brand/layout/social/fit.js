// Headline fit: shrink the display type until the HEADLINE fits the room left for it,
// down to a floor of two-thirds the starting size. Past the floor, the page is marked
// data-overflow="1" and the publisher refuses it — the fix is fewer words, never
// smaller type.
document.fonts.ready.then(function () {
  try {
    var h = document.querySelector('.h');
    if (!h) return;                       // no headline slot: nothing to measure
    var box = h.closest('.txt') || h.parentElement;

    function outer(el) {
      var cs = getComputedStyle(el);
      return el.offsetHeight + parseFloat(cs.marginTop) + parseFloat(cs.marginBottom);
    }

    // Measure only what this loop can change. The box also carries the kicker, the
    // subline and (on takeaways) three numbered rows; measuring the whole box let an
    // over-long list drive the headline down to the floor and then PASS, having shrunk
    // the one element that was never the problem. `room` is taken once, before any
    // shrinking, so it stays the headline's own share throughout.
    var room = box.clientHeight - (box.scrollHeight - outer(h));
    if (room <= 0) {
      // Everything but the headline already overruns the box. No headline size fixes
      // that, so the headline is left alone and the page is refused on its word count.
      document.body.setAttribute('data-overflow', '1');
      return;
    }

    function over() { return outer(h) > room || h.scrollWidth > h.clientWidth; }

    var s = parseFloat(getComputedStyle(h).fontSize), floor = s * 0.66;
    while (over() && s > floor) { s -= 2; h.style.fontSize = s + 'px'; }
    if (over()) document.body.setAttribute('data-overflow', '1');
  } catch (e) {
    // Measuring threw, so nothing was proved to fit. Refusing is the safe answer.
    document.body.setAttribute('data-overflow', '1');
  } finally {
    // Always mark the page measured, including on the early return above. A missing
    // mark means "fit.js never ran", and the publisher then blames the template's
    // brand-pack links for what is really an empty or unusual headline slot.
    document.body.setAttribute('data-fit', 'done');
  }
});
