# manifest (spine) — Subscription Plans & Quotas (app example)

> Minimal spine: 2 systems (subscription/billing), real data pointing at this example's files.

## Status Enum (unified across all tables)
`Draft` → `Prototyping` → `Final` → `Recheck`. `Final*` = Final with a `[TBD]` backlog.

## A. System Inventory + Dependency Graph
| SystemID | Name | area-sub-system dir | Status | R-ModuleCode | Deps (upstream) | Depended-on-by (downstream) |
|--------|--------|----------------|------|----------|-----------|-------------|
| S01 | Subscription | examples/subscription-plans | Final* | R-SUB | Text`[external]`·Usage`[external]` | Billing |
| S02 | Billing | examples/billing | Draft | R-BILL | Subscription (reads plan/tier to charge) | (none) |

> Edges: Billing → Subscription (reads plan & tier for charging). Subscription only references external systems (text/usage/billing), forming no internal cycle.

## B. Range Allocation Registry
| ModuleCode | System | Protocol Range | Error-code Range | Notes |
|--------|------|----------|----------|------|
| R-SUB | Subscription | 2100–2199 `example` | 21000– `example` | `SubscriptionError` |
| R-BILL | Billing | 2200–2299 `example` | 22000– `example` | stub |

## C. Cross-layer Index (one block per system)

### S01 Subscription
- **Rules (-01)**: `rules.md` (R-SUB-PLAN/QUOTA/CHANGE/FEAT)
- **Config tables**: `subscription.xlsx` (4 tables) + `config-spec.md`
- **Contract (proto)**: `subscription.proto`
- **Acceptance**: `acceptance.md`
- **Domain rules**: `subscription.checks.json` (coverage/monotonic)
- **Reverse-provides**: plan/tier as the source of truth for entitlements

### S02 Billing  `(draft stub)`
- **Rules (-01)**: `(to be written)`
- **Referenced shared sources of truth**: subscription `plan.id` / `planTier.tier` (to charge & prorate)
- **The rest**: pending (stub)

## D. Freeze Ledger + Recheck
| System | Status | Final time | Occupied ranges | Recheck trigger |
|------|------|----------|----------|------------|
| S01 Subscription | Final* | 2026-06-24 | 2100– / 21000– | backlog: none |
| S02 Billing | Draft | — | — | subscription interface |

## E. Rollback Records
| Time | System | From status → To status | Reason | Affected downstream |
|------|------|-----------------|------|--------------|
| — | — | — | — | — |
