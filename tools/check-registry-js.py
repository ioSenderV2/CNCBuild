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
    addEventListener(t, fn) { (this._h = this._h || {})[t] = fn; },
  };
}

// --- build the stub from the page's real markup -----------------------
const cards = [], sections = [];
let cur = null;
const re = /<section id="([a-z0-9-]+)"|<div class="sym (p-[A-Za-z]+)" id="([A-Z0-9_]+)" data-sym="([^"]*)" data-prov="([^"]*)" data-note="([^"]*)"/g;
let m;
while ((m = re.exec(html))) {
  if (m[1]) {
    cur = el('', {}, m[1]);
    cur.syms = [];
    cur.querySelector = () => cur.syms.find(x => !x.has('hide')) || null;
    sections.push(cur);
    continue;
  }
  const e = el('sym ' + m[2], { sym: m[4], prov: m[5], note: m[6] }, m[3]);
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
const byId = new Map([['q', qEl], ['n', nEl]]);
cards.forEach(c => byId.set(c.id, c));

const location = { hash: '' };
const winHandlers = {};
const document = {
  getElementById: id => byId.get(id) || null,
  querySelectorAll(sel) {
    if (sel === '.sym') return cards;
    if (sel === 'section') return sections;
    if (sel === '.chip[data-prov]') return chips;
    if (sel === 'nav a') return navLinks;
    return [];
  },
};
function addEventListener(t, fn) { winHandlers[t] = fn; }

const sandbox = { document, location, addEventListener, console };
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
