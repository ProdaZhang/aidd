# Subscription Plans & Quotas — Config Spec (field schema for subscription.xlsx)

> Field annotations for the 4 tables in `subscription.xlsx`. Self-describing header: row1=table English name, row2=type, row3=field key, row4=description, row5+=data.
> The Ref column written as `table.field` (in backticks) = a foreign key; `config_check`/`value_check` machine-check it; external tables are marked "(external)" and not machine-checked.

---

## Config-table Overview

| Table | Primary key | Purpose |
|------|------|------|
| `plan` | id | Subscription plan (price + tier) |
| `planTier` | tier | Tier → per-resource quota ladder (monotonic) |
| `feature` | id | Feature catalog |
| `planFeature` | id | Which features each plan includes |

---

## 1. `plan` Plans (primary key id)

| Field | Type | Values/Enum | Range/Default | Ref | Description |
|------|------|----------|----------|------|------|
| id | int | — | — | — | Plan id |
| name | int | — | — | Text table (external) | Name text id |
| tier | int | — | 1~3 | `planTier.tier` | Quota tier |
| priceMonthly | int | cents | — | — | Monthly price in cents |
| trialDays | int | — | — | — | Trial days before first charge |

## 2. `planTier` Quota Ladder (primary key tier)

| Field | Type | Values/Enum | Range/Default | Ref | Description |
|------|------|----------|----------|------|------|
| tier | int | — | 1~3 | — | Tier |
| seats | int | monotonic | — | — | Seat limit (non-decreasing with tier) |
| projects | int | monotonic | — | — | Project limit |
| storageGb | int | monotonic | — | — | Storage limit (GB) |
| apiPerDay | int | monotonic | — | — | API calls per day |

## 3. `feature` Feature Catalog (primary key id)

| Field | Type | Values/Enum | Range/Default | Ref | Description |
|------|------|----------|----------|------|------|
| id | int | — | — | — | Feature id |
| name | int | — | — | Text table (external) | Name text id |

## 4. `planFeature` Plan → Feature (primary key id)

| Field | Type | Values/Enum | Range/Default | Ref | Description |
|------|------|----------|----------|------|------|
| id | int | — | — | — | Row id |
| plan | int | — | — | `plan.id` | Plan id |
| feature | int | — | — | `feature.id` | Feature id |

---

## Check Checklist (machine-checked)

- [ ] schema alignment: `config_check.py config-spec.md subscription.xlsx` → 0 major.
- [ ] foreign keys: `plan.tier→planTier.tier`, `planFeature.plan→plan.id`, `planFeature.feature→feature.id` with no broken links.
- [ ] ladder: `planTier.tier` covers 1~3; `seats`/`projects`/`storageGb`/`apiPerDay` monotonic non-decreasing (see `subscription.checks.json`).
