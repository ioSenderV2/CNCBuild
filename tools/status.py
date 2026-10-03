#!/usr/bin/env python3
"""Harvest decision markers out of the prose and generate the index and open list.

    status.py check     parse everything, report counts, name the stale-list risks
    status.py open      every open item, grouped by file
    status.py index     regenerate INDEX.md
    status.py status    regenerate STATUS.md
    status.py all       both files

WHY THIS EXISTS
---------------
On 2026-10-02 two settled decisions were relitigated in one session, both for the same
reason: a HAND-MAINTAINED SUMMARY had drifted from the text it summarised.

  * an "Open items" entry said the three-point mount was "only in the project notes,
    not in this repo" - while torsion-box.md documented it in full, tenons, ledge
    depth, back-post shoulder and all;
  * another entry carried an M8 column of 20 after the body text had corrected it to
    35, and a consequence computed from the dead value went with it.

Merging the files would not have helped: the second failure happened INSIDE one
2877-line file, with the entry and its own correction a few hundred lines apart.

The disease is the hand-maintained pointer, and the cure is the same one the dimension
registry applies to numbers - the summary is GENERATED, so it cannot disagree with its
source. Mark the decision where the decision lives; let the list build itself.

THE CONVENTION IT HARVESTS
--------------------------
Already in use across the prose, several hundred times:

    OK  settled / decided          WARN  open, or a caution
    RED important, often open      NO    rejected, superseded, struck out

CLASSIFICATION IS A HEURISTIC, AND IS MEANT TO BE VISIBLE: an entry counts as OPEN if
it carries WARN or RED and does NOT also carry OK. That is right most of the time and
wrong sometimes - a RED on a settled decision reads as open. When it misreads, fix the
MARKERS IN THE PROSE rather than special-casing here; the markers are the interface.

Stdlib only, Python 3.11+.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories whose prose carries decisions.
#
# machine/drawings/README.md IS harvested, deliberately: that folder is derived by its
# own rule, but its STALE banner is a real open item about the pack itself and belongs
# in the list. Only .md is read, so the hand-drawn sheets never leak in.
SOURCE_DIRS = ["machine", "linear-encoder", "commissioning", "wiring"]

# Generated or index files - never harvested, or the output feeds itself.
GENERATED = {"STATUS.md", "INDEX.md", "VALUES.md"}

SETTLED, OPEN, FLAG, REJECTED, NOTE, PROC = "✅", "⚠️", "🔴", "❌", "📌", "📋"
MARKERS = [SETTLED, OPEN, FLAG, REJECTED, NOTE, PROC]
MARKER_RE = re.compile("|".join(re.escape(m) for m in MARKERS))

LABEL = {
    SETTLED: "settled",
    OPEN: "open",
    FLAG: "flagged",
    REJECTED: "rejected",
    NOTE: "note",
    PROC: "procedure",
}

# A hand-maintained list of open items is exactly the thing this tool replaces. Finding
# one still in the prose is a finding, not an error - it is a migration not yet done.
HANDLIST_RE = re.compile(r"^#{1,5}\s*.*\bopen items?\b", re.I)


@dataclass
class Entry:
    marker: str
    text: str
    file: str
    line: int
    heading: str
    anchor: str
    struck: bool = False

    @property
    def is_open(self) -> bool:
        """Open = asks for something and is not also marked settled."""
        return self.marker in (OPEN, FLAG) and SETTLED not in self.text and not self.struck


@dataclass
class Doc:
    path: Path
    rel: str
    headings: list[tuple[int, str, str, int]] = field(default_factory=list)  # level, text, anchor, line
    entries: list[Entry] = field(default_factory=list)
    handlists: list[tuple[int, str]] = field(default_factory=list)


def anchorise(text: str, seen: Counter) -> str:
    """GitHub's heading-anchor rules, near enough for links that have to work in a
    browser and in the VS Code preview."""
    a = MARKER_RE.sub("", text)
    a = re.sub(r"[`*_~\[\]()]", "", a).strip().lower()
    a = re.sub(r"[^\w\s-]", "", a)
    a = re.sub(r"\s+", "-", a)
    seen[a] += 1
    return a if seen[a] == 1 else f"{a}-{seen[a] - 1}"


def clean(text: str) -> str:
    """Strip markdown emphasis so a harvested line reads as a sentence."""
    t = MARKER_RE.sub("", text).strip()
    t = re.sub(r"^[-*]\s+", "", t)
    t = re.sub(r"~~(.+?)~~", r"\1", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def parse(path: Path) -> Doc:
    doc = Doc(path=path, rel=path.relative_to(ROOT).as_posix())
    seen: Counter = Counter()
    stack: list[str] = []
    in_fence = False

    lines = path.read_text(encoding="utf-8").split("\n")

    def continuation(start: int) -> str:
        """A marked entry is nearly always a wrapped paragraph. Harvesting only its
        first line cut sentences in half - 'Much of the analysis on' - so take the rest
        of the block, stopping at anything that starts something new."""
        parts = []
        for look in lines[start:]:
            t = look.strip()
            if not t or t.startswith(("#", "|", "```", ">")) or MARKER_RE.match(t):
                break
            if re.match(r"^([-*]|\d+\.)\s", t):
                break
            parts.append(t)
        return " ".join(parts)

    for n, raw in enumerate(lines, 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        h = re.match(r"^(#{1,6})\s+(.*)$", raw)
        if h:
            level, text = len(h.group(1)), h.group(2).strip()
            anchor = anchorise(text, seen)
            doc.headings.append((level, text, anchor, n))
            del stack[level - 1:]
            stack.append(clean(text))
            if HANDLIST_RE.match(raw):
                doc.handlists.append((n, clean(text)))

        if not MARKER_RE.search(raw):
            continue
        # Only lines that OPEN with a marker are decisions. A marker mid-sentence is
        # emphasis inside an argument, and harvesting those buries the real ones.
        body = re.sub(r"^[-*]\s+", "", raw.strip())
        if not MARKER_RE.match(body):
            continue
        marker = MARKER_RE.match(body).group(0)
        text = clean(body + " " + continuation(n))
        if not text:
            continue
        doc.entries.append(
            Entry(
                marker=marker,
                text=text,
                file=doc.rel,
                line=n,
                heading=" / ".join(stack[-2:]) if stack else "",
                anchor=doc.headings[-1][2] if doc.headings else "",
                struck=body.lstrip(marker).strip().startswith("~~"),
            )
        )
    return doc


def load() -> list[Doc]:
    docs = []
    for d in SOURCE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            if p.name in GENERATED:
                continue
            docs.append(parse(p))
    return docs


def trunc(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def cmd_check(_a) -> int:
    docs = load()
    counts: Counter = Counter()
    opens = 0
    for d in docs:
        for e in d.entries:
            counts[e.marker] += 1
            opens += e.is_open
    print(f"{len(docs)} files, {sum(counts.values())} marked decisions.\n")
    for m in MARKERS:
        if counts[m]:
            print(f"  {m}  {LABEL[m]:10} {counts[m]:4}")
    print(f"\n  OPEN (needs action): {opens}")

    hand = [(d.rel, n, t) for d in docs for n, t in d.handlists]
    if hand:
        print(f"\n{len(hand)} hand-maintained open-items section(s) still in the prose:")
        for rel, n, t in hand:
            print(f"  {rel}:{n}  {t}")
        print(
            "\n  These are what this tool replaces. Each one is a list that can drift\n"
            "  from the text it summarises - which is how two settled decisions got\n"
            "  relitigated on 2026-10-02. Migrate the entries to markers where the\n"
            "  decision lives, then delete the section and let STATUS.md carry it."
        )
    return 0


def cmd_open(_a) -> int:
    docs = load()
    total = 0
    for d in docs:
        rows = [e for e in d.entries if e.is_open]
        if not rows:
            continue
        print(f"\n{d.rel}  ({len(rows)})")
        print("-" * (len(d.rel) + 8))
        for e in rows:
            print(f"  {e.marker} L{e.line:<5} {trunc(e.text, 96)}")
            total += 1
    print(f"\n{total} open.")
    return 0


HEADER = """<!-- GENERATED by tools/{tool} - DO NOT EDIT -->
# {title}

**Generated.** Edit the prose, then run `tools/status.py {cmd}`.

{blurb}
"""

BLURB_STATUS = """Every open decision across the repo, harvested from the markers in the prose. The
`machine/*.md` files remain authoritative: this page is a view of them, not a second
copy, and it **cannot go stale** because it is rebuilt rather than maintained.

That property is the whole point. On 2026-10-02 two settled decisions were relitigated
because a **hand-written** open-items list had drifted from the text it summarised — one
entry claimed the three-point mount was undocumented while `torsion-box.md` described it
in full, and another carried a dimension the body text had already corrected.

⚠️ **Classification is a heuristic:** an item is open if it carries ⚠️ or 🔴 and is not
also marked ✅. When that reads wrong, **fix the markers in the prose** — they are the
interface, not this file."""

BLURB_INDEX = """Every heading in the repo's prose, so a topic can be found without knowing which file
it lives in. That was the real gap: on 2026-10-02 the torsion box's mounting was looked
for in the end-plate file and declared missing.

Numbers are not here — [`dimensions/VALUES.md`](dimensions/VALUES.md) is authoritative
for those. Drawings are not here either; `machine/drawings/` is derived by its own rule."""


def cmd_status(_a) -> int:
    docs = load()
    out = [HEADER.format(tool="status.py", title="Open items", cmd="status", blurb=BLURB_STATUS)]
    total = 0
    for d in docs:
        rows = [e for e in d.entries if e.is_open]
        if not rows:
            continue
        out.append(f"\n## [{d.rel}]({d.rel})  ({len(rows)})\n")
        for e in rows:
            link = f"{d.rel}#{e.anchor}" if e.anchor else d.rel
            where = f" — *{trunc(e.heading, 60)}*" if e.heading else ""
            out.append(f"- {e.marker} [L{e.line}]({link}){where}<br>{e.text}")
            total += 1
    out.append(f"\n---\n\n**{total} open** across {len(docs)} files.\n")
    p = ROOT / "STATUS.md"
    p.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {p}  ({total} open)")
    return 0


def cmd_index(_a) -> int:
    docs = load()
    out = [HEADER.format(tool="status.py", title="Index", cmd="index", blurb=BLURB_INDEX)]
    for d in docs:
        if not d.headings:
            continue
        out.append(f"\n## [{d.rel}]({d.rel})\n")
        for level, text, anchor, line in d.headings:
            if level == 1:
                continue
            out.append(f"{'  ' * (level - 2)}- [{clean(text)}]({d.rel}#{anchor})")
    p = ROOT / "INDEX.md"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    n = sum(len(d.headings) for d in docs)
    print(f"wrote {p}  ({n} headings)")
    return 0


def cmd_all(a) -> int:
    return cmd_status(a) or cmd_index(a)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn, help_ in [
        ("check", cmd_check, "counts, and name the stale-list risks"),
        ("open", cmd_open, "every open item, to the terminal"),
        ("status", cmd_status, "regenerate STATUS.md"),
        ("index", cmd_index, "regenerate INDEX.md"),
        ("all", cmd_all, "regenerate both"),
    ]:
        sub.add_parser(name, help=help_).set_defaults(fn=fn)
    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    # A Windows console defaults to cp1252, which cannot encode the very markers this
    # tool is built around. Without this it dies printing its own summary.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
