# Contributing guide (AIDD)

## Running tests

The checker / tool scripts have pure-stdlib tests (**not pytest**: each test file ships its own runner).

```bash
cd aidd/references/scripts
for t in tests/test_*.py; do python "$t"; done     # each prints N/N passed
pip install -r requirements.txt                     # only ui_palette/slice (Pillow) and gherkin (openpyxl) need it
```

Changing a script must keep everything green.

## Core principles (understand before changing)

1. **One skill, lean SKILL.md**: `aidd` reads the spine, judges progress, and **routes to a phase playbook in `references/`**. The detail lives in `references/` (methodology, phases, scripts), not inlined into `SKILL.md` — that keeps context lean without splitting into many skills.
2. **Scripts: argv-driven, zero project hardcoding, deterministic** (no `Date.now`/randomness). Reading xlsx always goes through `xlsx_dump` (sidesteps openpyxl's style errors on some exported tables); only **writing** xlsx uses openpyxl.
3. **Domain-neutral core**: examples / test fixtures use neutral illustrative names; **domain specifics live in packs** (`references/patterns/` + `references/examples/`) — the app pack ships the `subscription-plans` example; a game pack would add game patterns/examples. Don't bake one domain's vocabulary into the core.
4. **Checkers under-report rather than false-positive**: can't parse / can't find → flag explicitly (`*_SKIP` info), never silently drop, never fabricate.

## How to add things

- **A domain rule**: in some `<system>.checks.json`, per the rule schema at the top of `value_check.py` (`cardinality`/`coverage`/`monotonic`); sample in `aidd/references/scripts/checks/example.checks.json`.
- **A pattern**: `aidd/references/patterns/<…>/`, neutralized and portable.
- **A checker**: pure stdlib + argv + a matching `tests/test_*.py` (in-memory fixtures: "a planted error gets caught + a clean doc doesn't false-positive"); register the category / severity in `scripts/README.md`.
- **A phase playbook**: `aidd/references/phases/*.md`, and route to it from `SKILL.md`.

## Conventions

- Files are **UTF-8 without BOM**; use `/` paths cross-platform. Per-harness writing methods are in `aidd/references/harness-adapt.md`.
- In markdown table content columns, **don't use a bare `|`** (it breaks the table) — use `/` or `\|`.
- Make tool calls in the function-call format your harness requires, and **after sending, re-verify the artifact actually landed** (read the file / `ls`).
- Cross-harness: the single-skill format works across Claude Code / ZCode / Gemini / Codex (Copilot 1.0.63 has no skills mechanism — see `harness-adapt.md`).
