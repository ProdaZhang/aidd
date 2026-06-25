# Subscription Plans & Quotas — Acceptance Cases (Gherkin, app example)

> Each carries an `R-SUB-*`; assertions reference config truth via `<table>[<key>].<field>`, which `value_check` parses one by one.

## Subscribe

```gherkin
Scenario: Subscribing grants the tier's quotas (R-SUB-PLAN-01)
  Given a tenant subscribes to plan[2]
  When the subscription is created
  Then the seat limit = planTier[2].seats and the project limit = planTier[2].projects
```

## Quota enforcement

```gherkin
Scenario: Action over the limit is rejected (R-SUB-QUOTA-01)
  Given seat usage on plan[2] equals planTier[2].seats
  When inviting one more seat
  Then return ERR_QUOTA_EXCEEDED and no seat is added

Scenario: The tier ladder is monotonic (R-SUB-QUOTA-02)
  When comparing tiers
  Then planTier[3].seats >= planTier[2].seats and planTier[2].seats >= planTier[1].seats
```

## Tier change

```gherkin
Scenario: Downgrade blocked when usage exceeds target (R-SUB-CHANGE-02)
  Given current project usage exceeds planTier[1].projects
  When downgrading to the tier of plan[1]
  Then return ERR_USAGE_OVER_TARGET and the plan is unchanged
```

## Features

```gherkin
Scenario: Feature gated by plan (R-SUB-FEAT-01)
  Given planFeature[2] links plan[3] to feature[201]
  When a tenant on plan[3] opens feature[201]
  Then the feature is available
```
