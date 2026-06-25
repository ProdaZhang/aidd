# App Example · Subscription Plans & Quotas (subscription-plans)

A **self-contained, runnable** AIDD handoff package for a **non-game** feature — SaaS subscription plans + quotas. It shows the methodology and the deterministic validators are **domain-general** (the same engine that gates a game system gates a billing feature). Entirely fictional, no specific project.

## Files (the six-piece set + spine)

| File | What it is |
|------|--------|
| [rules.md](rules.md) | Functional rules, each carrying `R-SUB-*`, prose with no bare numbers (only `<table>[<key>].<field>` references) |
| [subscription.xlsx](subscription.xlsx) | Config tables (4: `plan`/`planTier`/`feature`/`planFeature`), self-describing 4-row header |
| [config-spec.md](config-spec.md) | subscription.xlsx's field schema + foreign-key declarations |
| [subscription.proto](subscription.proto) | Interface contract (client = server, one and the same) |
| [acceptance.md](acceptance.md) | Gherkin, 5 scenarios, assertions reference config truth |
| [subscription.checks.json](subscription.checks.json) | Domain rules (tier-ladder coverage + monotonic) |
| [manifest.md](manifest.md) | Spine (2 systems: subscription + billing stub) |

## Run the validators (in this directory)

```bash
S=../../scripts

# 1) schema drift: config-spec <-> xlsx columns / types / table names
python $S/config_check.py config-spec.md subscription.xlsx

# 2) data integrity: broken foreign keys / dangling acceptance refs / coverage·monotonic rules
python $S/value_check.py config-spec.md . --acc acceptance.md --rules subscription.checks.json

# 3) spine self-consistency: module-code registration / dependency targets / status / cycle
python $S/manifest_check.py manifest.md

# 4) reference graph: dangling R-codes / table / proto across the package
python $S/ref_graph.py . --check
```

**Expected: all four clean (0 major).** Foreign keys checked: `plan.tier→planTier.tier`, `planFeature.plan→plan.id`, `planFeature.feature→feature.id`. External tables `plan.name`/`feature.name → text` are marked "(external)" → skipped.

## Reference implementation (proof another agent can build it)

[`_reference-impl/`](_reference-impl/) is a tiny entitlements service written **only from this package** (it reads `subscription.xlsx`, implements the `R-SUB-*` rules). Its tests are the 5 acceptance scenarios:

```bash
cd _reference-impl && python test_entitlements.py     # -> 5 passed, 0 failed
```

## Want to see a validator catch drift? Break one spot:

- Make a higher tier's limit smaller than a lower one in `planTier` (e.g. `planTier[2].seats` < `planTier[1].seats`) → `value_check` reports **RULE_MONOTONIC** (the classic "higher plan accidentally gives less" bug).
- Point a `plan.tier` at a nonexistent tier (e.g. `9`) → `value_check` reports **FK_BREAK**.
- Add a column to `subscription.xlsx` not recorded in the spec → `config_check` reports **UNDOC_COL**.
- Reference an `R-SUB-*` in `acceptance.md` that `rules.md` doesn't define → `ref_graph` reports **DANGLING_RULE**.

This is AIDD's core loop: **design → machine-check gating → only 0 major counts as ready for handoff** — same as the game examples, on an app feature.
