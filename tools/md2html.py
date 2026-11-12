#!/usr/bin/env python3
"""Render the prose into printable HTML files - the input to tools/make-pdf.ps1.

    md2html.py                 write all four
    md2html.py --doc build     just build-document.html
    md2html.py --doc steel     just steel-prep.html
    md2html.py --doc wiring    just wiring-document.html
    md2html.py --check         render and report, write nothing

Each document names its source directory with "dir" in DOCS, defaulting to machine. The
wiring document was the first from a second directory, 2026-11-07, and adding it is what
took the hardcoded machine/ out of rebase() and the photograph scan.

THE FOURTH IS THE WIRING PROSE, and it exists for a plainer reason than the register split
below: a .md file is unreadable anywhere but an editor. His words, 2026-11-07 - "md files
are useless on their own outside of VS Code". It also carries the two {{SYMBOL}} values that
a browser markdown extension would show as their own names.

WHY THERE ARE THREE MACHINE DOCUMENTS
-------------------------------------
The first two are split by REGISTER, not by subject, and that split is the whole point:

  build-document.html   <- machine/assembly.md      WHAT GETS BUILT. Parts, hardware, what
                                                    bolts to what, in the order it is done.
  design-record.html    <- the thirteen machine/*.md WHY IT IS THAT SHAPE. The schemes that
                                                    were killed, the figures that moved.

The third is a single procedure on its own sheet, with no cover page and no contents:

  steel-prep.html       <- machine/steel-prep.md    Cleaning the steel and getting paint on it.
                                                    It is carried to the parts, not read at a desk.

One document carrying both could not be worked from. A page that says "bolt this here" and
then spends four paragraphs on what it nearly was instead is arguing with itself while
somebody is standing at the machine holding a drill. Keeping the reasoning is right -
it is genuinely useful - but not on the page the work is read from.

So BOTH are VIEWS, never sources. Nothing is specified in either for the first time and
nothing in the record is summarised - every heading and every line of body text comes
through verbatim. If one of these files and a `machine/*.md` file disagree, the `.md` file
wins, exactly as docs/drawings/README.md says of the drawings.

A new decision goes into a chapter, and then into assembly.md if it changes what gets built.
Writing the reasoning into assembly.md is the failure this split exists to prevent.

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

LINKS, AND WHY EVERY HREF IS WRITTEN FOR docs/
----------------------------------------------
Measured 2026-10-02 by printing a test page and reading the PDF's annotation dictionary:
headless Edge preserves `<a href>` as real PDF link annotations, resolving RELATIVE hrefs
against the HTML's own location at print time and writing the result in as an absolute
`file:///` URL. Internal `#anchor` links become named destinations and work as page jumps.

Two consequences:

  * the HTML lives in docs/ (his call, 2026-11-11 - every reader document in one folder),
    so every link in the source markdown is rebased for that home: repo files gain one
    `../`, and targets already inside docs/ become sibling references. rebase() is where
    that rule lives, and the photo cache sits at docs/build-photos so the embedded
    photographs stay sibling-relative too;
  * a `file:///` link only resolves on a machine holding this checkout. The internal jumps
    and the table of contents work anywhere; the links out to photos, datasheets and the
    shop pack do not work on paper. That is accepted, not overlooked.

Python 3.11+, plus `markdown`.
"""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import sys
from pathlib import Path

try:
    import markdown
except ModuleNotFoundError:
    sys.exit("ERROR: the markdown package is missing - run:  python -m pip install markdown")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import subst                                                  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PHOTO_CACHE = ROOT / "docs" / "build-photos"   # print-sized copies beside the documents
                                               # that embed them; gitignored, rebuilt on demand

# Long edge in pixels, and JPEG quality. See prepare_photos() for why these are enough.
PHOTO_MAX_PX = 1100
PHOTO_QUALITY = 82

# Reading order, which is NOT the directory listing order. The load case is the premise every
# deflection figure depends on, so it leads. The three cross-cutting files - tramming,
# machining, open items - come last because the others refer to them.
#
# FLAG: SIX FILES LEFT THIS LIST ON 2026-10-11, into machine/archive/. They were walkthroughs of
# dimension chains the registry now owns - torsion-box, lateral-stiffness, x-gantry-end-plates,
# z-carriage, y-beam-support, outboard-plate - and they kept going stale against it. The specific
# failure: a sole plate position was read out of x-gantry-end-plates.md as -182.5 when the
# registry had moved it to -175 the week before, and the prose audit cannot catch that class of
# drift because a 7.5 error reads as a different quantity, not a near miss.
#
# What was worth keeping came out as FOUR SMALL FILES, one argument each - the parts that do not
# reduce to symbols. They are comparisons and rejected options, so their numbers cannot go stale
# against the registry: nothing in them defines a part.
ORDER = [
    "loads-and-plate-thicknesses.md",
    "gantry-beam-joint.md",
    "box-stiffness.md",
    "three-point-mount.md",
    "egg-crate.md",
    "lateral-fix.md",
    "spindle-and-mount.md",
    "stepper-sizing.md",
    "spoilboard.md",
    "tramming.md",
    "machining.md",
    "open-items.md",
]

# TWO DOCUMENTS, from the same prose directory and the same CSS.
#
# The split is by REGISTER, not by subject. The build document says what gets built - parts,
# hardware, what bolts to what, in the order it is done. The design record says why, what was
# weighed and what a figure used to be. Mixing them is what made one document that could not be
# worked from: a page carrying both is arguing with itself while somebody holds a drill.
#
# Neither is authoritative. The .md files are, exactly as docs/drawings/README.md says of
# the drawings.
DOCS = {
    "build": {
        "out": "docs/build-document.html",
        "order": ["assembly.md"],
        "tab": "CNCBuild - build document",
        "h1": "CNCBuild",
        "sub": "Building the machine &mdash; what bolts to what, and in what order",
        "sheets": True,
        "note": (
            "<p><strong>This is the build document. It says what gets built and nothing"
            " else.</strong> The reasoning, the options that were weighed and what any figure"
            " used to be are in the <em>design record</em> &mdash; a separate printout of the"
            " thirteen <code>machine/*.md</code> chapters. <strong>Where this document and a"
            " chapter disagree, the chapter wins.</strong></p>"
            "<p><strong>Drilled hole coordinates are not here.</strong> They are on the sheets"
            " in the shop pack, one sheet per part, linked below. This document says which"
            " parts meet, with what hardware, and when.</p>"
            "<p><strong>An item marked &#9888; Open is not specified anywhere in this"
            " repo.</strong> It is not an omission from this document &mdash; do not fill one"
            " in from a catalogue or from inference.</p>"
            "<p><strong>Measured values live in <a href=\"../commissioning/\">commissioning/</a>"
            " and outrank every computed figure here.</strong></p>"
        ),
    },
    "record": {
        "out": "docs/design-record.html",
        "order": None,            # filled from ORDER below
        "tab": "CNCBuild - design record",
        "h1": "CNCBuild &mdash; design record",
        "sub": "Why the machine is the shape it is &mdash; the reasoning, kept",
        "sheets": False,
        "note": (
            "<p><strong>This is the design record, not the build document.</strong> It is the"
            " thirteen <code>machine/*.md</code> files concatenated verbatim, in reading order,"
            " so the reasoning behind every decision can be followed - including the schemes"
            " that were tried and killed, and the figures that moved. <strong>To build from,"
            " use <code>build-document.pdf</code> instead.</strong></p>"
            "<p>Nothing is specified here for the first time and nothing is summarised."
            " <strong>If this document and a <code>.md</code> file disagree, the"
            " <code>.md</code> file wins</strong> and this copy is stale.</p>"
            "<p>Ten of the thirteen chapters were one 2877-line file,"
            " <code>end-plates-risers-and-spindle.md</code>, until 2026-10-02. The split was"
            " verbatim; the per-file note recording it is omitted here rather than repeated"
            " ten times.</p>"
            "<p><strong>Measured values live in <a href=\"../commissioning/\">commissioning/</a>"
            " and outrank every computed figure in this document.</strong></p>"
        ),
    },
    # THE ONE SHEET WITH NO COVER AND NO CONTENTS, because it is read standing over the parts
    # with a rag in one hand. A cover page and a table of contents on a three-page procedure is
    # two sheets of paper that have to be turned past before the first instruction.
    # It is NOT at the repo root, and it is TRACKED, where the other two are neither. Both
    # follow from the same thing: the sheet carries no outbound links, so it has no reason to
    # sit where machine/photos/x.jpg resolves, and nothing in it can go stale against the
    # registry - it names no dimension. So it can be a file in the repo rather than something
    # regenerated before every print. Add a link to this sheet and it has to move to the root.
    "steel": {
        "out": "docs/steel-prep.html",
        "order": ["steel-prep.md"],
        "tab": "CNCBuild - steel prep",
        "h1": None,              # the chapter's own h1 is the page's heading
        "sub": None,
        "front": False,          # no cover, no contents
        "sheets": False,
        "note": None,
        # The other two go through headless Edge with its own page setup. This one is printed
        # from a browser on a home printer, which honours @page - and the shared rule is A4.
        "css": "@page { size:letter portrait; margin:14mm 0 14mm; }",
    },
    # THE WIRING PROSE, because a .md file is unreadable anywhere but an editor. His, 2026-11-07.
    # It reads wiring/ rather than machine/, which is what "dir" is for - this was the first
    # document from a second source directory and the reason the hardcoded machine/ came out
    # of rebase() and the photo scan.
    "wiring": {
        "out": "docs/wiring-document.html",
        "dir": "wiring",
        "order": [
            "README.md",
            "cabinet-power-and-grounding.md",
            "ig57-drives.md",
            "breakout-box.md",
            "db37-axis-interconnect.md",
        ],
        "tab": "CNCBuild - wiring",
        "h1": "CNCBuild &mdash; wiring",
        "sub": "Power in, what the E-stops kill, the drives, and the one bar every ground meets at",
        "sheets": False,
        "note": (
            "<p><strong>The five <code>wiring/*.md</code> files, verbatim and in reading"
            " order.</strong> Nothing is specified here for the first time and nothing is"
            " summarised. <strong>If this document and a <code>.md</code> file disagree, the"
            " <code>.md</code> file wins</strong> and this copy is stale - regenerate it with"
            " <code>tools/md2html.py --doc wiring</code>.</p>"
            "<p><strong>The drawing is <a href=\"panel-schematic.html\">"
            "panel-schematic.html</a>, which is not part of this document.</strong> Five sheets"
            " with wire colour and gauge on every run, maintained by hand - it is derived from"
            " the prose here, never the other way round.</p>"
            "<p><strong>An item marked OPEN is not settled anywhere in this repo.</strong> Do"
            " not fill one in from a catalogue or from inference. FLAG marks a statement this"
            " file used to make and no longer does, kept so it cannot be reinstated by"
            " accident.</p>"
            "<p><strong>Measured values live in <a href=\"../commissioning/\">commissioning/</a>"
            " and outrank every computed figure here.</strong></p>"
        ),
    },
}

# The shop pack's own sheets, by the id anchors added to docs/drawings/shop-pack.html.
SHEETS = [
    ("sheet-1", "Sheet 1 - Front Y end plate / Z riser"),
    ("sheet-2", "Sheet 2 - X gantry end plate"),
    ("sheet-3a", "Sheet 3a - X carriage plate"),
    ("sheet-3b", "Sheet 3b - Z spacer bar"),
    ("sheet-4", "Sheet 4 - Z plate"),
    ("sheet-5", "Sheet 5 - Y nut doubler block and sole bracket"),
    ("sheet-12", "Sheet 12 - Parallelism jig end plate (made at home)"),
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
        if not prefix:
            # A single-file document needs no disambiguation, and leaving the slug bare is
            # what makes an `#anchor` written in the markdown work BOTH here and in GitHub's
            # own rendering of that file. Prefixed, every in-page link in the source is dead.
            return v
        return f"{prefix}{separator}{v}" if v else prefix

    return slugify


def rebase(href: str, chapters: dict[str, str], src: str = "machine",
           slug: str = "") -> str:
    """Rewrite one href for an HTML file living in docs/.

    Links between the chapters become internal anchors; everything else is rebased from the
    source directory to the root so the relative path still points at a real file. `src` is
    the document's source directory - machine for the three machine documents, wiring for the
    wiring one.

    `slug` is the chapter being rendered, and it exists for ONE case: a bare `#anchor`
    written in the markdown. On a multi-chapter document every heading id is namespaced with
    its chapter slug - see slugger() - so a bare anchor that works in VS Code and on GitHub
    points at nothing here. An in-file anchor means "this file", so it gets this chapter's
    prefix. Without this, every hand-written in-page link in the source is dead in the
    printed document, silently: the link renders, it just goes nowhere.
    """
    if href.startswith("#"):
        return f"#{slug}-{href[1:]}" if slug and href != "#" else href
    if href.startswith(("http://", "https://", "mailto:")):
        return href
    if href in chapters:                 # chapter to chapter -> a page jump
        return "#" + chapters[href]
    if href == "README.md":              # the source directory's own index
        root_rel = f"{src}/README.md"
    elif href.startswith("../"):         # already relative to the root
        root_rel = href[3:]
    else:                                # anything else inside the source directory
        root_rel = f"{src}/{href}"
    # The documents live in docs/ since 2026-11-11, so a root-relative path gains
    # one ../ - except a path into docs/ itself, which becomes a sibling reference.
    if root_rel.startswith("docs/"):
        return root_rel[len("docs/"):]
    return "../" + root_rel


HREF_RE = re.compile(r'href="([^"]*)"')


def prepare_photos(photo_dir: Path, out_dir: Path, rebuild: bool = False) -> tuple[int, int]:
    """Write print-sized copies of the photographs into out_dir. Originals are never touched.

    The source photographs are ~2576 px on the long edge and ~1.4 MB each, and Edge embeds
    them essentially whole - the first PDF built this way came out at 22.9 MB. Printed two
    across on A4 inside 14 mm margins each figure is about 88 mm wide, so PHOTO_MAX_PX is
    still comfortably over 300 dpi at the size it is actually printed.

    EXIF orientation is baked in rather than carried: the tag is dropped on save, so a
    portrait photograph that relied on it would come out on its side. That is a silent
    failure - the image is there, just wrong - which is why it is done explicitly.

    Returns (source bytes, output bytes).
    """
    out_dir.mkdir(exist_ok=True)
    src_bytes = out_bytes = 0
    for src in sorted(photo_dir.glob("*.jpg")):
        dst = out_dir / src.name
        src_bytes += src.stat().st_size
        if rebuild or not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            from PIL import Image, ImageOps

            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im)
                im.thumbnail((PHOTO_MAX_PX, PHOTO_MAX_PX), Image.LANCZOS)
                im.convert("RGB").save(dst, "JPEG", quality=PHOTO_QUALITY, optimize=True)
        out_bytes += dst.stat().st_size
    return src_bytes, out_bytes


def load_captions(photos: Path) -> dict[str, str]:
    """Read the caption table out of machine/photos/README.md, rendered to inline HTML.

    A caption may carry a link, and the caption's own base is the photos folder - not the
    chapter directory rebase() serves. Found the hard way on 2026-11-11: a caption linking
    ../../linear-encoder/controller-board.md rendered verbatim into a document where that
    path pointed outside the repo, and a dead link renders exactly like a live one. So
    caption hrefs get resolved from the photos folder here, then shifted for docs/ the same
    way rebase() shifts everything else.
    """
    readme = photos / "README.md"
    if not readme.exists():
        sys.exit(f"ERROR: {readme} not found - the captions have no source")
    photos_rel = photos.resolve().relative_to(ROOT).as_posix()

    def fix_href(m: re.Match) -> str:
        href = m.group(1)
        if href.startswith("#") or href.startswith(("http://", "https://", "mailto:")):
            return m.group(0)
        root_rel = posixpath.normpath(posixpath.join(photos_rel, href))
        if root_rel.startswith("docs/"):
            return f'href="{root_rel[len("docs/"):]}"'
        return f'href="../{root_rel}"'

    inline = markdown.Markdown(extensions=["extra"])
    out: dict[str, str] = {}
    for name, caption in CAPTION_RE.findall(readme.read_text(encoding="utf-8")):
        inline.reset()
        rendered = inline.convert(caption).removeprefix("<p>").removesuffix("</p>")
        out[name] = HREF_RE.sub(fix_href, rendered)
    return out


def figures(names: list[str], captions: dict[str, str]) -> str:
    """One grid of figures. A photograph with no caption row is an error, not a blank."""
    cells = []
    for n in names:
        if n not in captions:
            sys.exit(f"ERROR: {n} has no row in machine/photos/README.md - add one, do not guess")
        cells.append(
            f'<figure><img src="{PHOTO_CACHE.name}/{n}" alt="{html.escape(n)}">'
            f'<figcaption><span class="fn">{html.escape(n)}</span>{captions[n]}</figcaption>'
            f"</figure>"
        )
    return f'<div class="figs">{"".join(cells)}</div>'


def render(key: str, md_dir: Path, captions: dict[str, str], on_disk: list[str],
           check: bool) -> tuple[str, Path, list[tuple[str, int, int]], list[str]]:
    """Build one document. Returns (html, output path, per-file stats, orphan photographs)."""
    spec = DOCS[key]
    order = spec["order"] or ORDER
    chapters: dict[str, str] = {name: Path(name).stem for name in order}

    # A document's source directory. The three machine documents share machine/; the wiring
    # one reads wiring/. md_dir arrives as the repo root's machine/ for backwards
    # compatibility, so the spec's own "dir" wins when it has one.
    src_name = spec.get("dir", "machine")
    md_dir = md_dir.parent / src_name

    # Which chapter cites which photograph. First citer wins, so a photo referenced twice is
    # printed once, with the chapter that leans on it hardest - the earlier one in reading
    # order. Anything no chapter cites goes to the appendix rather than being dropped.
    #
    # The photographs live in machine/photos/ and are cited by the machine prose. A document
    # from another directory places none, and that is not a finding - so it skips the scan
    # rather than reporting every photograph as an orphan.
    placed: dict[str, list[str]] = {name: [] for name in order}
    if src_name == "machine":
        for photo in on_disk:
            for name in order:
                if photo in (md_dir / name).read_text(encoding="utf-8"):
                    placed[name].append(photo)
                    break
        orphans = [p for p in on_disk if not any(p in v for v in placed.values())]
    else:
        orphans = []

    bodies: list[str] = []
    toc: list[str] = []
    stats: list[tuple[str, int, int]] = []

    for name in order:
        src = md_dir / name
        if not src.exists():
            sys.exit(f"ERROR: {src} not found - DOCS[{key!r}] is out of date")

        # subst.read, not read_text: {{SYMBOL}} resolves to the registry's
        # value here, so the printed document carries the number and the .md
        # carries only the name. An unknown symbol raises rather than printing.
        text = subst.read(src)
        text, dropped = PROVENANCE_RE.subn("", text, count=1)

        slug = chapters[name]
        md = markdown.Markdown(
            extensions=["extra", "toc", "sane_lists", "admonition"],
            extension_configs={
                "toc": {"slugify": slugger(slug if len(order) > 1 else ""), "separator": "-"},
            },
        )
        body = md.convert(text)
        # slug is passed only when the document namespaces its heading ids, which is what
        # len(order) > 1 decides in the slugger above. On a single-chapter document the ids
        # are bare and a bare anchor already matches.
        anchor_prefix = slug if len(order) > 1 else ""
        body = HREF_RE.sub(
            lambda m: f'href="{rebase(m.group(1), chapters, src_name, anchor_prefix)}"', body)
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

    # The appendix only belongs on the document that places photographs chapter by chapter.
    # On the build document every photograph would be an orphan, which is not a finding.
    if orphans and len(order) > 1:
        bodies.append(
            '<section class="plates" id="appendix-photographs">'
            "<h1>Appendix &mdash; further photographs</h1>"
            "<p>These are in machine/photos/ and no chapter above cites them. They are here "
            "because the pack is carried away from the checkout, and a photograph that shows "
            "something a drawing cannot is worth having even when no sentence points at it.</p>"
            f"{CAP_NOTE}{figures(orphans, captions)}</section>"
        )
        toc.append('<li><a href="#appendix-photographs">Appendix &mdash; further photographs</a></li>')

    sheet_block = ""
    if spec["sheets"]:
        sheets = "".join(
            f'<li><a href="drawings/shop-pack.html#{i}">{html.escape(t)}</a></li>'
            for i, t in SHEETS
        )
        sheet_block = f"""
<h2>Drawings &mdash; the shop pack</h2>
<p>The sheets are a separate file because they are hand-authored SVG and are regenerated on a
different cycle. These links open the pack at the named sheet. <strong>They resolve only on a
machine holding this checkout</strong> &mdash; on paper they are inert, and the table of
contents jumps are the ones that always work.</p>
<ol>{sheets}</ol>
<p><a href="drawings/README.md">The rules that folder follows</a> &mdash; derived never
authoritative, unknowns marked never invented, one datum per plate.</p>"""

    # A document with "front": False carries neither - see DOCS["steel"] for why.
    front_block = ""
    if spec.get("front", True):
        front_block = f"""
<header class="front">
<h1>{spec["h1"]}</h1>
<p class="sub">{spec["sub"]}</p>

<div class="note">
{spec["note"]}
</div>
{sheet_block}
</header>

<nav class="toc">
<h1>Contents</h1>
<ol>{"".join(toc)}</ol>
</nav>
"""

    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{spec["tab"]}</title>
<!-- GENERATED by tools/md2html.py - DO NOT EDIT. Regenerate: tools\\make-pdf.ps1 -->
<style>{CSS}{spec.get("css", "")}</style></head>
<body><div class="page">
{front_block}
{chr(10).join(bodies)}

</div></body></html>
"""
    return doc, ROOT / spec["out"], stats, orphans


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="render and report, write nothing")
    ap.add_argument("--rebuild-photos", action="store_true",
                    help="re-scale every photograph even if the cached copy looks current")
    ap.add_argument("--doc", choices=sorted(DOCS), action="append",
                    help="render only this document; repeatable. Default: both")
    args = ap.parse_args()

    md_dir = ROOT / "machine"
    photo_dir = md_dir / "photos"

    keys = args.doc or sorted(DOCS)
    wants_photos = any(DOCS[k].get("dir", "machine") == "machine" for k in keys)

    captions = load_captions(photo_dir)
    on_disk = sorted(p.name for p in photo_dir.glob("*.jpg"))
    # Scaling sixteen photographs takes a few seconds and writes 2.3 MB. Only the machine
    # documents embed any, so rendering the wiring one alone should not pay for it.
    if not args.check and wants_photos:
        src_b, out_b = prepare_photos(photo_dir, PHOTO_CACHE, args.rebuild_photos)
        print(f"photographs scaled to {PHOTO_MAX_PX}px: "
              f"{src_b/1048576:.1f} MB -> {out_b/1048576:.1f} MB in {PHOTO_CACHE.name}/")

    missing = [p for p in on_disk if p not in captions]
    unused_caps = [c for c in captions if c not in on_disk]
    if missing:
        print(f"  WARNING no caption row: {', '.join(missing)}")
    if unused_caps:
        print(f"  WARNING caption with no file: {', '.join(unused_caps)}")

    for key in keys:
        doc, out, stats, orphans = render(key, md_dir, captions, on_disk, args.check)
        print(f"\n== {key}: {out.name} ==")
        for name, n, dropped in stats:
            flag = "  (provenance note dropped)" if dropped else ""
            print(f"  {name:34} {n:5} lines{flag}")
        total = sum(n for _, n, _ in stats)
        print(f"  {len(stats)} source file(s), {total} lines -> {len(doc.splitlines())} HTML lines")
        # Only the machine documents place photographs. Reporting a count on a document that
        # never scanned for them reads as 16 placed when the answer is none.
        if len(stats) > 1 and DOCS[key].get("dir", "machine") == "machine":
            print(f"  photographs: {len(on_disk)} on disk, "
                  f"{len(on_disk) - len(orphans)} placed, {len(orphans)} in the appendix")
        if args.check:
            print("  --check: nothing written")
        else:
            out.write_text(doc, encoding="utf-8")
            print(f"  wrote {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
