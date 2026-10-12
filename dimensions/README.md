# Dimensions

**A convention change, made deliberately on 2026-10-02, and a bigger one than the drawings folder.**

[`registry.toml`](registry.toml) is **authoritative for values.** The `machine/*.md` files stay
authoritative for **reasoning**. If a number here and a number in prose disagree, **this folder wins
and the prose is stale.**

That inverts the previous rule, under which the `.md` files were the source of truth for everything.
It is a narrower inversion than it sounds: the registry owns only *what a number is*, and prose keeps
owning *why* — what it trades against, what was rejected, what it would cost to change. Nothing about
how the files read has to change.

## Why

On 2026-10-02 a single session found **five wrong numbers** in the prose. They were two different
faults, and only one of them is fixed by writing numbers down in one place.

**Three were bad primitives carried as labels.** A "5/8in" spacer that measured **16.41**; a
"Φ80×200" spindle whose nameplate reads **213**; a "1/2in" plate whose stock is **10 mm**. In every
case the repo had recorded what the part was *sold as* and then used it as a dimension.

**Two were orphaned derivations**, and these are the dangerous class:

| | |
|---|---|
| The shelf's rear bolt | dimensioned from the **beam front**. The beam moved to flush; the hole did not, and it now lands at Y 0 — off the edge of the plate |
| "1.8 mm proud" | computed from an M8 column at **20**. The column was corrected to 35 elsewhere in the same file, and the consequence was left behind |

**A symbol would not have caught either.** A number in prose is just text; nothing checks it. What
catches them is the **reverse index** — change a primitive, and the tool lists every value that has
to be re-derived. That is what `expr` is for and why the registry is machine-readable rather than a
markdown table.

## Use

Run through [`../tools/dims.py`](../tools/dims.py). Stdlib only, Python 3.11+.

| Command | |
|---|---|
| `dims.py check` | evaluate everything; non-zero exit on any error. Also lists what is **not confirmed on the real part** |
| `dims.py deps SYM` | **what depends on SYM, transitively. Run this BEFORE changing a primitive** |
| `dims.py open` | every OPEN or nominal value, and what each feeds |
| `dims.py table` | every symbol, value, provenance |
| `dims.py fusion` | Fusion 360 parameters CSV |
| `dims.py md` | regenerate [`VALUES.md`](VALUES.md) |
| `check-registry-js.py` | run [`registry.html`](registry.html)&rsquo;s own script under node against a stub DOM and assert the chips, the search and the index tracking still work &mdash; there is no browser in the loop, so a claim that they do is worth nothing without it |
| `dims.py html` | regenerate [`registry.html`](registry.html) &mdash; the whole registry to browse: grouped by its own section headings, every symbol mentioned in an expression or a note is a link to that symbol, each card lists what USES it, and the search box matches notes as well as names |

## Provenance is not decoration

It is the repo's standing rule — *the machine is the authority, not the configuration* — made
machine-readable.

| | |
|---|---|
| `measured` | off the real machine or part, with an instrument |
| `part` | off a part's own geometry that is not in doubt |
| `vendor` | off a datasheet committed to `manufacturer-assets/` |
| `nominal` | OPEN: a catalogue figure **not yet confirmed on the part** — the class that produced three of this session's five errors |
| `derived` | computed here from other symbols, and it RE-DERIVES when they move |
| `alias` | another name for one other symbol &mdash; a rename, with no arithmetic to be wrong |
| `pinned` | NOTE: it came out of a calculation and was then FIXED. It does **not** follow its source: `XEP_W` is 154 from `BLOCK_BUTTED`&rsquo;s 154.18 rounded down, and stays 154. Re-check these by hand when the source moves |
| `OPEN` | FLAG: not established. **A placeholder. Must not be cut to.** |

Separately from provenance, a symbol may be **`retired = true`**: nothing uses it any more, and it is kept because it is the record of a reversal. `dims.py check` fails if anything still derives from one.

## Fusion

`dims.py fusion` writes [`fusion-parameters.csv`](fusion-parameters.csv) for **Modify → Change
Parameters → Import**.

OPEN: **Verify the first import rather than trusting it.** Fusion has shipped variations on whether it
wants a header row; `--header` adds one if yours does.

FLAG: **Every symbol exports as a plain number, never as its expression.** Fusion would accept the
expression, but then two systems would own the same derivation and they would drift — which is the
exact failure this registry exists to stop. **The registry derives; Fusion consumes.** Re-export and
re-import after any registry change, because Fusion holds a copy and a copy goes stale.

## What this does not do yet

OPEN: **Nothing enforces that a number quoted in prose matches the registry.** `deps` tells you what to
go and check; it does not check it for you. A prose checker — tagging quoted numbers so they can be
verified mechanically — is the obvious next step and is **not built**.

OPEN: **Only the ten plate files split out of `end-plates-risers-and-spindle.md` on 2026-10-02
have been mined for primitives** - see [`../machine/README.md`](../machine/README.md) for the list.
The other `machine/*.md` files have numbers that are not in here.
Key them in as they get touched rather than attempting a sweep, which is the version of this job that
gets abandoned half-done.
