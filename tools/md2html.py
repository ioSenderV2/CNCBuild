#!/usr/bin/env python3
"""Render the machine prose into ONE printable HTML file - the input to tools/make-pdf.ps1.

    md2html.py            write build-document.html at the repo root
    md2html.py --check    render and report, write nothing

WHY THIS EXISTS
---------------
The reasoning is the artifact, and the reasoning is spread over twelve files. That is right
for editing and wrong for the one thing prose cannot do: be carried. A build document is
read at the machine, away from a checkout, and the mill trip is a single trip.

So this is a VIEW, never a source. Nothing is specified here for the first time and nothing
is summarised - every heading and every line of body text comes through verbatim. If this
file and a `machine/*.md` file disagree, the `.md` file wins, exactly as
machine/drawings/README.md says of the drawings.

WHAT IT DELIBERATELY DROPS
--------------------------
The three-line "Split out of end-plates-risers-and-spindle.md" blockquote at the top of the
ten plate files. It is true and it belongs in each file, but ten copies of it in one printed
document is noise. The fact is stated ONCE in the front matter instead.

WHY IT IS NOT STDLIB-ONLY
-------------------------
tools/status.py is stdlib-only on purpose: STATUS.md and INDEX.md gate correctness, so they
must regenerate on any machine with a bare Python. This script does not gate anything - if
the markdown package is missing you lose a printout, not a datum. The prose here uses pipe
tables, four heading levels, nested bullets, bold inside table cells and inline links, which
is precisely where a hand-rolled parser drops a table row silently.

    python -m pip install markdown

LINKS, AND WHY THE OUTPUT GOES AT THE REPO ROOT
-----------------------------------------------
Measured 2026-10-02 by printing a test page and reading the PDF's annotation dictionary:
headless Edge preserves `<a href>` as real PDF link annotations, resolving RELATIVE hrefs
against the HTML's own location at print time and writing the result in as an absolute
`file:///` URL. Internal `#anchor` links become named destinations and work as page jumps.

Two consequences:

  * the HTML must sit at the REPO ROOT, so that `machine/photos/x.jpg` resolves to the real
    file - every link in the source markdown is rebased accordingly;
  * a `file:///` link only resolves on a machine holding this checkout. The internal jumps
    and the table of contents work anywhere; the links out to photos, datasheets and the
    shop pack do not work on paper. That is accepted, not overlooked.

Python 3.11+, plus `markdown`.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

try:
    import markdown
except ModuleNotFoundError:
    sys.exit("ERROR: the markdown package is missing - run:  python -m pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build-document.html"

# Reading order, which is NOT the directory listing order. The load case is the premise every
# deflection figure depends on, so it leads. The beams come before what holds them up.
# outboard-plate sits immediately before torsion-box because torsion-box.md opens by telling
# you to read the outboard plate's "How it lands on the torsion box" first. The three
# cross-cutting files - tramming, machining, open items - come last because every plate
# section refers to them.
ORDER = [
    "loads-and-plate-thicknesses.md",
    "gantry-beam-joint.md",
    "y-beam-support.md",
    "lateral-stiffness.md",
    "outboard-plate.md",
    "torsion-box.md",
    "spindle-and-mount.md",
    "z-carriage.md",
    "x-gantry-end-plates.md",
    "tramming.md",
    "machining.md",
    "open-items.md",
]

# The shop pack's own sheets, by the id anchors added to machine/drawings/shop-pack.html.
SHEETS = [
    ("sheet-1", "Sheet 1 - Front Y end plate / Z riser"),
    ("sheet-2", "Sheet 2 - X gantry end plate"),
    ("sheet-3", "Sheet 3 - X carriage plate"),
    ("sheet-4", "Sheet 4 - Z plate"),
    ("sheet-5", "Sheet 5 - Y nut doubler block and sole bracket"),
    ("checklist", "Before the trip - checklist"),
]

PROVENANCE_RE = re.compile(
    r"\n> Split out of `end-plates-risers-and-spindle\.md`.*?\n\n---\n",
    re.DOTALL,
)

# A row of the caption table in machine/photos/README.md. The captions are used VERBATIM -
# they are the owner's own words about what each photograph is evidence of, and inventing a
# caption for a photograph of a real part is exactly the kind of thing this repo forbids.
CAPTION_RE = re.compile(r"^\|\s*`([a-z0-9-]+\.jpg)`\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)

# machine/photos/README.md states this rule; it is repeated on every photo page because the
# page is what gets carried to the machine, and the README is not.
CAP_NOTE = (
    '<p class="cap-note">Evidence, not dimensions. <strong>Nothing here should be scaled'
    " off</strong> &mdash; every number in the prose came from a caliper or a vendor drawing."
    " Captions are from machine/photos/README.md, verbatim.</p>"
)

CSS = """
:root { --ink:#111; --rule:#bbb; --soft:#666; --band:#f2f2f2; }
* { box-sizing:border-box; }
body { margin:0; color:var(--ink); background:#fff;
       font:11pt/1.5 "Segoe UI","Helvetica Neue",Arial,sans-serif; }
.page { max-width:none; padding:0 14mm; }

h1,h2,h3,h4,h5 { line-height:1.25; margin:1.1em 0 .45em; page-break-after:avoid; break-after:avoid; }
h1 { font-size:21pt; border-bottom:2.5pt solid var(--ink); padding-bottom:.25em; margin-top:0; }
h2 { font-size:15pt; border-bottom:.75pt solid var(--rule); padding-bottom:.15em; }
h3 { font-size:12.5pt; }
h4 { font-size:11pt; text-transform:none; color:#000; }
h5 { font-size:10.5pt; color:var(--soft); }

p, li { orphans:3; widows:3; }
a { color:#0b4f9e; text-decoration:none; border-bottom:.4pt dotted #0b4f9e; }
code { font:10pt/1.4 Consolas,"Courier New",monospace; background:var(--band);
       padding:.05em .3em; border-radius:2px; }
strong { font-weight:650; }
blockquote { margin:.8em 0; padding:.1em 0 .1em 1em; border-left:2.5pt solid var(--rule);
             color:#333; }
hr { border:0; border-top:.75pt solid var(--rule); margin:1.4em 0; }

table { border-collapse:collapse; width:100%; margin:.7em 0; font-size:9.5pt;
        page-break-inside:auto; break-inside:auto; }
thead { display:table-header-group; }
tr { page-break-inside:avoid; break-inside:avoid; }
th,td { border:.5pt solid var(--rule); padding:.3em .5em; text-align:left;
        vertical-align:top; }
th { background:var(--band); font-weight:650; }

ul,ol { padding-left:1.4em; margin:.5em 0; }
li { margin:.18em 0; }

/* Each file starts a fresh page - the whole point of the split survives into print. */
section.chapter { page-break-before:always; break-before:page; }
section.chapter:first-of-type { page-break-before:avoid; break-before:avoid; }

/* Front matter and contents */
.front { page-break-after:always; break-after:page; }
.front h1 { font-size:30pt; border:0; margin-bottom:.1em; }
.front .sub { font-size:13pt; color:var(--soft); margin:0 0 1.6em; }
.warn { border:1.5pt solid #a00; background:#fff4f4; padding:.7em 1em; margin:1.2em 0; }
.note { border-left:3pt solid var(--rule); padding:.2em 0 .2em 1em; color:#333; margin:1.2em 0; }

nav.toc { page-break-after:always; break-after:page; }
nav.toc ol { list-style:none; padding-left:0; counter-reset:ch; }
nav.toc > ol > li { counter-increment:ch; margin:.5em 0; font-weight:650; font-size:11.5pt; }
nav.toc > ol > li::before { content:counter(ch) ".  "; color:var(--soft); }
nav.toc ol ol { padding-left:2.1em; margin:.2em 0 .6em; }
nav.toc ol ol li { font-weight:400; font-size:10pt; margin:.1em 0; }
nav.toc a { border:0; }

/* Photographs. Two across, each with its caption from machine/photos/README.md. The
   figures sit at the end of the chapter that cites them rather than interrupting a table. */
section.plates { page-break-before:always; break-before:page; }
section.plates h2 { margin-top:0; }
.figs { display:grid; grid-template-columns:1fr 1fr; gap:6mm 5mm; }
figure { margin:0; page-break-inside:avoid; break-inside:avoid; }
figure img { width:100%; height:auto; border:.5pt solid var(--rule); display:block; }
figcaption { font-size:8.5pt; line-height:1.35; color:#222; margin-top:.35em; }
figcaption .fn { display:block; font:8pt Consolas,"Courier New",monospace; color:var(--soft);
                 margin-bottom:.15em; }

@page { size:A4; margin:16mm 0 16mm; }
@media print { a { color:#0b4f9e; } }
"""


def slugger(prefix: str):
    """Heading anchors, namespaced per chapter.

    "Open items" is a heading in three different files, and the emoji markers would
    otherwise collide too once stripped. Prefixing with the chapter slug keeps every
    internal link unambiguous.
    """

    def slugify(value: str, separator: str) -> str:
        v = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
        v = re.sub(r"[-\s]+", separator, v)
        return f"{prefix}{separator}{v}" if v else prefix

    return slugify


def rebase(href: str, chapters: dict[str, str]) -> str:
    """Rewrite one href for an HTML file living at the repo root.

    Links between the twelve chapters become internal anchors; everything else is rebased
    from machine/ to the root so the relative path still points at a real file.
    """
    if href.startswith(("#", "http://", "https://", "mailto:")):
        return href
    if href in chapters:                 # chapter to chapter -> a page jump
        return "#" + chapters[href]
    if href == "README.md":              # machine/README.md, the directory index
        return "machine/README.md"
    if href.startswith("../"):           # already relative to the root
        return href[3:]
    return "machine/" + href             # photos/, drawings/, anything else in machine/


HREF_RE = re.compile(r'href="([^"]*)"')


def load_captions(photos: Path) -> dict[str, str]:
    """Read the caption table out of machine/photos/README.md, rendered to inline HTML."""
    readme = photos / "README.md"
    if not readme.exists():
        sys.exit(f"ERROR: {readme} not found - the captions have no source")
    inline = markdown.Markdown(extensions=["extra"])
    out: dict[str, str] = {}
    for name, caption in CAPTION_RE.findall(readme.read_text(encoding="utf-8")):
        inline.reset()
        out[name] = inline.convert(caption).removeprefix("<p>").removesuffix("</p>")
    return out


def figures(names: list[str], captions: dict[str, str]) -> str:
    """One grid of figures. A photograph with no caption row is an error, not a blank."""
    cells = []
    for n in names:
        if n not in captions:
            sys.exit(f"ERROR: {n} has no row in machine/photos/README.md - add one, do not guess")
        cells.append(
            f'<figure><img src="machine/photos/{n}" alt="{html.escape(n)}">'
            f'<figcaption><span class="fn">{html.escape(n)}</span>{captions[n]}</figcaption>'
            f"</figure>"
        )
    return f'<div class="figs">{"".join(cells)}</div>'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="render and report, write nothing")
    args = ap.parse_args()

    md_dir = ROOT / "machine"
    photo_dir = md_dir / "photos"
    chapters: dict[str, str] = {name: Path(name).stem for name in ORDER}

    captions = load_captions(photo_dir)
    on_disk = sorted(p.name for p in photo_dir.glob("*.jpg"))

    # Which chapter cites which photograph. First citer wins, so a photo referenced twice is
    # printed once, with the chapter that leans on it hardest - the earlier one in reading
    # order. Anything no chapter cites goes to the appendix rather than being dropped.
    placed: dict[str, list[str]] = {name: [] for name in ORDER}
    for photo in on_disk:
        for name in ORDER:
            if photo in (md_dir / name).read_text(encoding="utf-8"):
                placed[name].append(photo)
                break
    orphans = [p for p in on_disk if not any(p in v for v in placed.values())]

    bodies: list[str] = []
    toc: list[str] = []
    stats: list[tuple[str, int, int]] = []

    for name in ORDER:
        src = md_dir / name
        if not src.exists():
            sys.exit(f"ERROR: {src} not found - ORDER is out of date")

        text = src.read_text(encoding="utf-8")
        text, dropped = PROVENANCE_RE.subn("", text, count=1)

        slug = chapters[name]
        md = markdown.Markdown(
            extensions=["extra", "toc", "sane_lists", "admonition"],
            extension_configs={"toc": {"slugify": slugger(slug), "separator": "-"}},
        )
        body = md.convert(text)
        body = HREF_RE.sub(lambda m: f'href="{rebase(m.group(1), chapters)}"', body)
        bodies.append(f'<section class="chapter" id="{slug}">\n{body}\n</section>')

        # Contents: the chapter, then its H2s. Deeper levels would run to three pages.
        tokens = md.toc_tokens
        top = tokens[0] if tokens else {"id": slug, "name": name}
        subs = [
            f'<li><a href="#{html.escape(c["id"])}">{html.escape(c["name"])}</a></li>'
            for t in tokens for c in t.get("children", [])
        ]

        if placed[name]:
            bodies.append(
                f'<section class="plates" id="{slug}-photographs">'
                f'<h2>Photographs &mdash; {html.escape(top["name"])}</h2>'
                f"{CAP_NOTE}{figures(placed[name], captions)}</section>"
            )
            subs.append(f'<li><a href="#{slug}-photographs">Photographs</a></li>')

        toc.append(
            f'<li><a href="#{html.escape(top["id"])}">{html.escape(top["name"])}</a>'
            + (f'<ol>{"".join(subs)}</ol>' if subs else "")
            + "</li>"
        )
        stats.append((name, len(text.splitlines()), dropped))

    if orphans:
        bodies.append(
            '<section class="plates" id="appendix-photographs">'
            "<h1>Appendix &mdash; further photographs</h1>"
            "<p>These are in machine/photos/ and no chapter above cites them. They are here "
            "because the pack is carried away from the checkout, and a photograph that shows "
            "something a drawing cannot is worth having even when no sentence points at it.</p>"
            f"{CAP_NOTE}{figures(orphans, captions)}</section>"
        )
        toc.append('<li><a href="#appendix-photographs">Appendix &mdash; further photographs</a></li>')

    sheets = "".join(
        f'<li><a href="machine/drawings/shop-pack.html#{i}">{html.escape(t)}</a></li>'
        for i, t in SHEETS
    )

    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>CNCBuild - the mechanical build document</title>
<!-- GENERATED by tools/md2html.py - DO NOT EDIT. Regenerate: tools\\make-pdf.ps1 -->
<style>{CSS}</style></head>
<body><div class="page">

<header class="front">
<h1>CNCBuild</h1>
<p class="sub">The mechanical build document &mdash; beams, plates, risers, spindle and Z</p>

<div class="note">
<p><strong>This document is derived, never authoritative.</strong> It is the twelve
<code>machine/*.md</code> files concatenated verbatim, in reading order, so that the reasoning
can be carried to the machine. Nothing is specified here for the first time and nothing is
summarised. <strong>If this document and a <code>.md</code> file disagree, the
<code>.md</code> file wins</strong> and this copy is stale.</p>
<p>Ten of the twelve chapters were one 2877-line file,
<code>end-plates-risers-and-spindle.md</code>, until 2026-10-02. The split was verbatim; the
per-file note recording it is omitted here rather than repeated ten times.</p>
<p><strong>Measured values live in <a href="commissioning/">commissioning/</a> and outrank
every computed figure in this document.</strong></p>
</div>

<div class="warn">
<p><strong>The shop pack is STALE as of 2026-10-02 and must not go to the mill.</strong> The Y
end design was reworked that day &mdash; cast stepper frames replaced BK12 and the M5
standoffs, the Y steppers moved to the front, all four as-built Y risers are scrapped, and the
two rear risers became one 1200&nbsp;mm steel plate. Every riser sheet is superseded. See
<a href="#open-items">Open items</a> before cutting anything.</p>
</div>

<h2>Drawings &mdash; the shop pack</h2>
<p>The sheets are a separate file because they are hand-authored SVG and are regenerated on a
different cycle. These links open the pack at the named sheet. <strong>They resolve only on a
machine holding this checkout</strong> &mdash; on paper they are inert, and the table of
contents jumps are the ones that always work.</p>
<ol>{sheets}</ol>
<p><a href="machine/drawings/README.md">The rules that folder follows</a> &mdash; derived never
authoritative, unknowns marked never invented, one datum per plate.</p>
</header>

<nav class="toc">
<h1>Contents</h1>
<ol>{"".join(toc)}</ol>
</nav>

{chr(10).join(bodies)}

</div></body></html>
"""

    total = sum(n for _, n, _ in stats)
    for name, n, dropped in stats:
        pics = f"  +{len(placed[name])} photo(s)" if placed[name] else ""
        flag = "  (provenance note dropped)" if dropped else ""
        print(f"  {name:34} {n:5} lines{flag}{pics}")
    print(f"\n{len(ORDER)} chapters, {total} source lines -> {len(doc.splitlines())} HTML lines")
    print(f"photographs: {len(on_disk)} on disk, {len(on_disk) - len(orphans)} placed in chapters, "
          f"{len(orphans)} in the appendix")
    missing = [p for p in on_disk if p not in captions]
    unused_caps = [c for c in captions if c not in on_disk]
    if missing:
        print(f"  WARNING no caption row: {', '.join(missing)}")
    if unused_caps:
        print(f"  WARNING caption with no file: {', '.join(unused_caps)}")

    if args.check:
        print("--check: nothing written")
        return 0

    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
