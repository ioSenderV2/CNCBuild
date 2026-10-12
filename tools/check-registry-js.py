#!/usr/bin/env python3
"""Does registry.html's own script actually filter and track?

🔴 WHY THIS EXISTS. The page's chips and search are the only way to find
anything in 515 symbols, and on 2026-10-11 he reported that none of the filter
buttons did anything. There is no browser here to check in, so a claim that it
works is worth nothing on its own - the page would be shipped broken twice.

So this lifts the script out of the GENERATED page and runs it under node
against a stub DOM built from that same page's real markup: real symbol ids,
real provenance values, real section ids. It then drives the page the way a
person does - click a chip, type in the box, jump to an anchor - and asserts
what should have happened.

It cannot prove the page LOOKS right. It can prove the logic is sound and the
handlers are wired, which is the half that was in doubt.

    python tools/check-registry-js.py

Exit 0 if every check passes, 1 if any fails, 2 if node or the page is missing.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# The failure lines carry emoji markers and reach stdout. On a default Windows
# console that is cp1252 and the print RAISES - so the ONE thing this tool
# exists to show, a failure, is the thing that kills it. Same trap and same fix
# as tools/dims.py.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = ROOT / "dimensions" / "registry.html"

HARNESS = r"""
const html = DATA.html, script = DATA.script;

function el(cls, data, id) {
  const c = new Set(String(cls || '').split(/\s+/).filter(Boolean));
  return {
    id: id || '', dataset: data || {}, children: [], parentElement: null,
    scrollTop: 0, textContent: '', _top: 0,
    classList: {
      add: x => c.add(x), remove: x => c.delete(x),
      contains: x => c.has(x),
      toggle: (x, on) => { on === undefined ? (c.has(x) ? c.delete(x) : c.add(x))
                                            : (on ? c.add(x) : c.delete(x)); },
    },
    has: x => c.has(x),
    getBoundingClientRect() { return { top: this._top, bottom: this._top + 20,
                                       height: 20 }; },
    getAttribute(n) { return this._attrs ? this._attrs[n] : undefined; },
    closest(sel) { return sel === 'section' ? this.parentElement : null; },
    scrollIntoView() { this._scrolled = true; },
    offsetWidth: 0, offsetHeight: 0, innerHTML: '', hidden: false,
    style: {},
    addEventListener(t, fn) { (this._h = this._h || {})[t] = fn; },
  };
}

// --- build the stub from the page's real markup -----------------------
const cards = [], sections = [];
let cur = null;
const re = /<section id="([a-z0-9-]+)"|<div class="sym (p-[A-Za-z]+)(?: retired)?" id="([A-Z0-9_]+)" data-sym="([^"]*)" data-prov="([^"]*)" data-retired="([^"]*)" data-note="([^"]*)"/g;
let m;
while ((m = re.exec(html))) {
  if (m[1]) {
    cur = el('', {}, m[1]);
    cur.syms = [];
    cur.querySelector = () => cur.syms.find(x => !x.has('hide')) || null;
    sections.push(cur);
    continue;
  }
  const e = el('sym ' + m[2], { sym: m[4], prov: m[5], retired: m[6],
                                note: m[7] }, m[3]);
  e.innerHTML = '<card>' + m[3] + '</card>';
  e.parentElement = cur;
  cards.push(e);
  if (cur) cur.syms.push(e);
}
sections.forEach((s, i) => { s._top = i * 400 - 2000; });

const navLinks = [...html.matchAll(/<a href="#([a-z0-9-]+)">/g)].map(x => {
  const a = el('', {}, '');
  a._attrs = { href: '#' + x[1] };
  return a;
});
const nav = el('');
nav._top = 0;
navLinks.forEach(a => { a.parentElement = nav; a._top = 0; });

const chips = [...html.matchAll(/<button type="button" class="chip" data-prov="([A-Za-z]+)">/g)]
  .map(x => el('chip', { prov: x[1] }));

const qEl = el(''); qEl.value = '';
const nEl = el('');
const peekEl = el(''); peekEl.hidden = true;
const byId = new Map([['q', qEl], ['n', nEl], ['peek', peekEl]]);
cards.forEach(c => byId.set(c.id, c));

const location = { hash: '' };
const winHandlers = {};
const retiredChip = el('chip', { retired: '1' });
const document = {
  getElementById: id => byId.get(id) || null,
  querySelector(sel) {
    if (sel === '.chip[data-retired]') return retiredChip;
    return null;
  },
  querySelectorAll(sel) {
    if (sel === '.sym') return cards;
    if (sel === 'section') return sections;
    if (sel === '.chip[data-prov]') return chips;
    if (sel === '.chip') return [...chips, retiredChip];
    if (sel === 'nav a') return navLinks;
    return [];
  },
};
function addEventListener(t, fn) { winHandlers[t] = fn; }

const innerWidth = 1400, innerHeight = 900;
const sandbox = { document, location, addEventListener, console,
                  innerWidth, innerHeight };
require('vm').runInNewContext(script, sandbox);

// --- drive it the way a person does -----------------------------------
const shown = () => cards.filter(c => !c.has('hide')).length;
const out = { total: cards.length, sections: sections.length,
              chips: chips.length, navLinks: navLinks.length,
              checks: [] };
const ok = (name, got, want) =>
  out.checks.push({ name, pass: JSON.stringify(got) === JSON.stringify(want),
                    got, want });

ok('every card visible at load', shown(), cards.length);
ok('counter set at load', nEl.textContent, cards.length + ' shown');

// one chip per provenance, and clicking one hides exactly that provenance
const provs = [...new Set(cards.map(c => c.dataset.prov))].sort();
ok('a chip for every provenance', chips.map(c => c.dataset.prov).sort(), provs);

// THE CHIPS SELECT RATHER THAN EXCLUDE - one click isolates a provenance,
// because that is how he uses the page.
for (const c of chips) {
  const p = c.dataset.prov;
  const n = cards.filter(x => x.dataset.prov === p).length;
  c._h.click();
  ok('clicking ' + p + ' shows only its ' + n, shown(), n);
  ok('and every one shown is ' + p,
     cards.filter(x => !x.has('hide')).every(x => x.dataset.prov === p), true);
  ok('counter says only ' + p, nEl.textContent.includes('only ' + p), true);
  ok(p + ' chip lit', c.has('on'), true);
  c._h.click();
  ok('clicking ' + p + ' again shows everything', shown(), cards.length);
  ok(p + ' chip unlit', c.has('on'), false);
}

// a second chip ADDS to the selection
chips[0]._h.click(); chips[1]._h.click();
const two = cards.filter(x => x.dataset.prov === chips[0].dataset.prov
                           || x.dataset.prov === chips[1].dataset.prov).length;
ok('two chips add up', shown(), two);
chips[0]._h.click();
ok('dropping one leaves the other',
   shown(), cards.filter(x => x.dataset.prov === chips[1].dataset.prov).length);
chips[1]._h.click();
ok('dropping the last shows everything', shown(), cards.length);

// the search box, on a name and on a note
qEl.value = 'acorn_nut';
qEl._h.input();
ok('name search finds the acorn symbols',
   cards.filter(c => !c.has('hide')).every(c => c.dataset.sym.includes('acorn_nut')),
   true);
qEl.value = 'caliper';
qEl._h.input();
const byNote = cards.filter(c => !c.has('hide'));
ok('note search matches notes, not just names', byNote.length > 0, true);
ok('and every hit really contains it',
   byNote.every(c => c.dataset.note.includes('caliper')), true);
qEl.value = 'zzzzzz';
qEl._h.input();
ok('a miss hides everything', shown(), 0);
ok('and hides every section', sections.every(s => s.has('hide')), true);
qEl.value = '';
qEl._h.input();
ok('clearing restores', shown(), cards.length);

// search AND chip together, which is the pair that actually gets used
chips[0]._h.click();
qEl.value = 'a';
qEl._h.input();
const both = cards.filter(x => !x.has('hide'));
ok('search and chip intersect',
   both.every(x => x.dataset.prov === chips[0].dataset.prov
                && (x.dataset.sym.includes('a') || x.dataset.note.includes('a'))),
   true);
chips[0]._h.click(); qEl.value = ''; qEl._h.input();

// the index follows the page
ok('a nav link for every section', navLinks.length, sections.length);
winHandlers.scroll();
const marked = () => navLinks.filter(a => a.has('cur')).map(a => a._attrs.href);
ok('exactly one section marked after a scroll', marked().length, 1);
ok('it is the last one passed', marked()[0], '#' + sections[5].id);
location.hash = '#' + cards[cards.length - 1].id;
winHandlers.hashchange();
ok('jumping to a symbol marks its section', marked().length, 1);
ok('and flashes the card it landed on',
   cards[cards.length - 1].has('flash'), true);

// 🔴 A LINK TO SOMETHING FILTERED OUT. Isolate one provenance, then follow a
// link to a symbol of another - the jump used to land on a display:none card
// and nothing moved at all.
const pA = chips[0].dataset.prov;
const other = cards.find(c => c.dataset.prov !== pA);
chips[0]._h.click();
ok('target is hidden while a chip is lit', other.has('hide'), true);
location.hash = '#' + other.id;
winHandlers.hashchange();
ok('following the link clears the filter', other.has('hide'), false);
ok('and scrolls to it', other._scrolled, true);
ok('and the chip goes out', chips[0].has('on'), false);
ok('and everything is back', shown(), cards.length);
ok('and it flashes', other.has('flash'), true);

// press and hold a symbol link: the card appears, release puts it away
const mkLink = t => {
  const a = { getAttribute: () => '#' + t.id };
  a.closest = sel => (sel === 'a[href^="#"]' ? a : null);
  return a;
};
const target = cards[7];
const anchor = mkLink(target);
winHandlers.pointerdown({ target: anchor, clientX: 100, clientY: 100 });
ok('holding a link shows the peek', peekEl.hidden, false);
ok('and it is the right symbol', peekEl.innerHTML, target.innerHTML);
ok('and it is placed on screen',
   typeof peekEl.style.left === 'string' && typeof peekEl.style.top === 'string',
   true);
winHandlers.pointerup();
ok('releasing hides it', peekEl.hidden, true);

// pressing somewhere that is not a symbol link does nothing
winHandlers.pointerdown({ target: { closest: () => null } });
ok('pressing elsewhere leaves it hidden', peekEl.hidden, true);

// 🔴 A PLAIN CLICK MUST NOT NAVIGATE - it peeked, and that is all it does
location.hash = '';
let prevented = false;
winHandlers.click({ target: anchor, preventDefault: () => { prevented = true; },
                    ctrlKey: false, metaKey: false });
ok('a plain click is prevented from following the link', prevented, true);
ok('and the hash does not move', location.hash, '');

// CTRL+CLICK IS THE ONE THAT GOES THERE, and it is prevented too so the
// browser does not open a new tab
prevented = false;
winHandlers.click({ target: anchor, preventDefault: () => { prevented = true; },
                    ctrlKey: true, metaKey: false });
ok('ctrl+click is prevented from opening a tab', prevented, true);
ok('and navigates itself', location.hash, '#' + target.id);

// ctrl held on PRESS does not peek - it is a navigation, not a look
peekEl.hidden = true;
winHandlers.pointerdown({ target: anchor, clientX: 10, clientY: 10,
                          ctrlKey: true });
ok('ctrl+press does not peek', peekEl.hidden, true);

// and a link that is NOT a symbol - the section index - is left alone
const navA = { getAttribute: () => '#the-extrusion' };
navA.closest = sel => (sel === 'a[href^="#"]' ? navA : null);
prevented = false;
winHandlers.click({ target: navA, preventDefault: () => { prevented = true; },
                    ctrlKey: false, metaKey: false });
ok('an index link is left to the browser', prevented, false);

// a hold on a link to a HIDDEN card still peeks - a filter is a view, and
// looking at something is not navigating to it
chips[0]._h.click();
const hiddenOne = cards.find(c => c.has('hide'));
const a2 = { getAttribute: () => '#' + hiddenOne.id,
             closest: sel => (sel === 'a[href^="#"]' ? a2 : null) };
winHandlers.pointerdown({ target: a2, clientX: 10, clientY: 10 });
ok('peeking at a filtered-out symbol still works', peekEl.hidden, false);
ok('and does NOT clear the filter', hiddenOne.has('hide'), true);
winHandlers.pointerup();
chips[0]._h.click();

// the retired chip is its own category, not a provenance
const nRet = cards.filter(c => c.dataset.retired === '1').length;
ok('some symbols are retired', nRet > 0, true);
retiredChip._h.click();
ok('the retired chip shows only those', shown(), nRet);
ok('counter says only retired', nEl.textContent.includes('only retired'), true);
retiredChip._h.click();
ok('and clicking it again restores', shown(), cards.length);

console.log(JSON.stringify(out));
"""


def main():
    if not PAGE.exists():
        print("registry.html is not built - run tools/dims.py html first",
              file=sys.stderr)
        return 2
    node = shutil.which("node")
    if not node:
        print("node is not on PATH, so the shipped script cannot be run."
              " THIS IS NOT A PASS.", file=sys.stderr)
        return 2

    html = PAGE.read_text(encoding="utf-8")
    script = html.split("<script>")[1].split("</script>")[0]
    data = json.dumps({"html": html, "script": script})

    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "h.js"
        f.write_text("const DATA=" + data + ";\n" + HARNESS, encoding="utf-8")
        r = subprocess.run([node, str(f)], capture_output=True,
                           encoding="utf-8", errors="replace")
    if r.returncode:
        print("node failed:\n" + (r.stderr or "")[:3000], file=sys.stderr)
        return 2

    res = json.loads(r.stdout.strip().splitlines()[-1])
    print(f"{res['total']} cards, {res['sections']} sections, "
          f"{res['chips']} chips, {res['navLinks']} index links\n")
    bad = 0
    for c in res["checks"]:
        if c["pass"]:
            print(f"  ok    {c['name']}")
        else:
            bad += 1
            print(f"  🔴 FAIL {c['name']}: got {c['got']!r}, want {c['want']!r}")
    print(f"\n{len(res['checks'])} check(s), {bad} failure(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
