---
name: aidd
description: AIDD (AI-assisted Design→Dev) — turn a design discussion into a platform-agnostic handoff package another AI can build from, gated by deterministic checkers. Use for designing any config/rule/UI-heavy system from scratch — game systems, app & SaaS features (plans, quotas, permissions, feature flags, forms, onboarding), tools — or to advance / sync the project spine. One skill: it reads the spine, judges progress, and routes you to the right phase playbook in references/. Domain-neutral; ships with references/.
---

# AIDD · orchestrator (one skill)

AIDD = **AI-assisted Design→Dev**. Turn a **design discussion** into a **platform-agnostic handoff package** — rules / config / contract / acceptance / UI prototype / spine — that **another AI (or person) can develop directly from**, with **deterministic checkers** gating it to "0 major issues" before handoff. Domain-neutral: the same engine designs a game system or a SaaS billing feature. **Landing the implementation (picking a tech stack to write the client/server) is downstream, not in this package.**

> This is **one skill** covering the whole pipeline. The detailed playbook for each phase lives in `references/` and is read on demand — keeping context lean without splitting into many skills.

## Core model
- **Two layers**: ① the live **project spine** — `project-charter` (concept / platform / target users / domain / naming conventions) + `manifest` (system list + dependency graph + cross-layer index + number-range registry + freeze ledger), continuously revised; ② the **per-system production loop**.
- **Centralized source of truth**: enums / numbering / contracts / config tables live in the project layer; prose references them by name, **position-independent** (`table[key].field` / `screenID.elementID` / `R-code`) — never inline a bare number.
- **Every operation**: read the spine → do the work → write back to the spine.
- Canonical method: `references/methodology.md`. Pitfalls: `references/gotchas.md`. Per-harness specifics: `references/harness-adapt.md`.

## On entry — self-check, then route (proactively drive forward)
1. **Does the spine exist?** (`project-charter` + `manifest`) — No → start at the **concept** phase to build it. Yes → read both.
2. **Which systems are not yet `Final`?** List them; ask which to push this time.
3. **Any `Recheck` systems?** (a shared item changed) → resolve via the **finalize/sync** phase first.
4. **Number-range conflicts / dependency cycles?** Check and report.

## Phases (read the matching playbook, then do the work)
| What you want to do | Read |
|---|---|
| Concept: core loop / platform / users / split into systems / start the spine | [`references/phases/concept.md`](references/phases/concept.md) |
| Design a system: rules (R-codes) + config tables (test data) + UI prototype | [`references/methodology.md`](references/methodology.md) — Steps 0–5, **part A** |
| Iterate after a dry-run: tweak rules / config / prototype (cheap, repeatable) | [`references/methodology.md`](references/methodology.md) — re-run **part A** |
| Finalize & hand off: contract + acceptance + (as needed) backend + checklist; then sync the spine | [`references/methodology.md`](references/methodology.md) **part B** + [`references/handoff-checklist.md`](references/handoff-checklist.md) |
| UI screenshot → UI DSL (capture a reference screen into the knowledge base) | [`references/phases/ui-capture.md`](references/phases/ui-capture.md) |

> Typical path: concept (once) → per system { design → iterate… (repeat) → finalize & hand off } → sync (continuous). Ordering isn't enforced — route as the work needs. A re-split / bounce records a rollback-log entry in the manifest and marks finalized downstream systems `Recheck`.

## Deterministic checkers (the gate — run before handoff)
`references/scripts/` (pure-Python, mostly stdlib): `config_check` (config-spec ↔ xlsx drift) · `value_check` (broken FKs / coverage / monotonic) · `manifest_check` (spine self-consistency) · `ref_graph --check` (dangling R-codes / refs) · `gherkin_to_checklist` · `ui_render` (UI-DSL → wireframe). **0 major = handoffable.** Runnable example: [`references/examples/subscription-plans/`](references/examples/subscription-plans/).

## Boundary (what it is not)
- Manages **structure & consistency, not quality judgment**: the checkers catch broken links / coverage / monotonicity / schema drift; they **don't judge whether the design is good** (game balance, UX, business correctness) — that's for people / dedicated tools.
- The HTML prototype validates **information architecture & flow**, not feel / timing / networking. Good for UI-dense surfaces (inventory, shop, settings, dashboards, onboarding); leave real-time feel to an engineering prototype.
- **Doesn't decide your numbers / conventions**: anything undecided is tagged `[to confirm]` and handed to a person.
- Goes as far as a **handoff package**; tech-stack choice and client/server implementation = downstream.

## Package (one folder)
Install the single `aidd/` skill folder into the host's skills directory (e.g. Claude Code's `.claude/skills/`). Everything — methodology, checkers, templates, examples — ships under `aidd/references/`. Domain packs (app / game patterns + examples) drop into `references/patterns/` + `references/examples/`.

## Hard constraints (don't violate)
- Files are **UTF-8 without BOM**.
- Reference by name (position-independent); per-myriad uniformly `/10000` where used.
- **Centralized config**: tables pooled globally, no per-system private tables; a cross-system reference is an ordinary reference, not a dependency edge. Broadcast-type shared sources (id namespace / enum / text) are **append-only, never break**.
- **Tool calls must use your harness's function-call format** or they may silently fail — verify the artifact actually landed (read-file / `ls`). Per-harness specifics in `references/harness-adapt.md`.
- After each change, append to the project **change ledger** (`CHANGELOG.md`); init from `references/templates/CHANGELOG.tpl.md` if absent.
