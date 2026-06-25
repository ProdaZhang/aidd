# Subscription Plans & Quotas — Functional Rules (app example)

> Prose has no bare numbers: only formulas + `<table>[<key>].<field>` references; the numbers live in `subscription.xlsx`. Every procedural decision carries an `R-SUB-*`.
> Scope: plan subscription, quota enforcement, tier change, feature gating. Billing/proration, current-usage and display text go through external systems.

---

## I. Plans — R-SUB-PLAN

- **R-SUB-PLAN-01** (subscribe): a tenant subscribes to `plan[pid]` → set the tenant's plan = pid and grant the quotas of that plan's tier `planTier[plan[pid].tier]`.
- **R-SUB-PLAN-02** (trial): a new tenant gets `plan[pid].trialDays` trial days before the first charge (charge settled by the billing system [external]).

## II. Quota enforcement — R-SUB-QUOTA

- **R-SUB-QUOTA-01** (enforce): an action that consumes a resource is allowed only while current usage < the matching limit in `planTier[plan[pid].tier]` (e.g. `planTier[...].seats`); otherwise reject (`ERR_QUOTA_EXCEEDED`). Current usage comes from the usage system [external].
- **R-SUB-QUOTA-02** (ladder convention): limits are read from the tier row directly; the ladder is **monotonically non-decreasing** — a higher `planTier.tier` is ≥ a lower one on every resource.

## III. Tier change — R-SUB-CHANGE

- **R-SUB-CHANGE-01** (upgrade): switching to a higher tier raises limits immediately; the price delta is prorated by the billing system [external].
- **R-SUB-CHANGE-02** (downgrade guard): a downgrade is rejected if current usage of any resource exceeds the target tier's limit in `planTier[target tier]` (`ERR_USAGE_OVER_TARGET`); the plan is left unchanged.

## IV. Features — R-SUB-FEAT

- **R-SUB-FEAT-01** (feature gate): a feature `feature[fid]` is available to a tenant iff a `planFeature` row links the tenant's `plan[pid]` to fid.

---

## Error Codes

| Code | Meaning |
|----|------|
| `ERR_QUOTA_EXCEEDED` | Action would exceed the tier's resource limit |
| `ERR_USAGE_OVER_TARGET` | Downgrade target tier's limit is below current usage |

## External Dependencies

- **Billing system** [external]: proration, charging, trial-to-paid conversion.
- **Usage system** [external]: the tenant's current usage per resource.
- **Text system** [external]: the `plan.name` / `feature.name` text ids.
