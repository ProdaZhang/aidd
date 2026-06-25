# Phase · Concept — build the project spine

Goal: from an idea, agree the concept and decompose it into systems; create the **spine** (`project-charter` + `manifest`). This phase sets **structure and conventions**, not values.

## Steps
1. **Discuss, don't hand over a doc.** Talk through, agree, and mark `[to confirm]` for anything undecided:
   - the **core loop / experience** (what the user does minute-to-minute and per session);
   - **platform**, **target users**, **domain/genre** (game) or **product surface** (app: e.g. billing, permissions, onboarding);
   - **business model** (monetization for a game; pricing/plans for SaaS) — at the structural level only.
2. **Decompose into systems + a dependency graph.** One system = one cohesive feature. Draw the upstream/downstream edges; flag cycles.
3. **Assign module-codes.** Give each system a unique `R-<MODULE>` and register its protocol / error-code ranges (check the registry first, avoid collisions).
4. **Create the spine from templates** — `references/templates/project-charter.tpl.md` + `references/templates/manifest.tpl.md`. Fill in:
   - charter: directory layout · naming · units · enum/quality dimensions · art/brand source;
   - manifest: system inventory · dependency graph · number-range registry · cross-layer index (one block per system) · freeze ledger.
5. **Output**: `project-charter.md` + `manifest.md`. Then route to the **system** phase, one system at a time (see `methodology.md`).

## Boundary
- Don't decide numbers or undecided conventions — concept fixes the **skeleton**, the system phase fills the flesh, and a person confirms the `[to confirm]` items.
- Reuse existing enums / conventions; don't redefine. Centralized config (global pool, no per-system private tables) is a project-charter convention set here.
