# Acceptance tests — the 5 Gherkin scenarios from acceptance.md, asserting against config truth.
import entitlements as E
from sub_repo import PLAN, TIER, FEATURE, PLAN_FEATURE

results = []
def case(rid, desc, fn):
    try: fn(); results.append((rid, desc, True, ""))
    except AssertionError as e: results.append((rid, desc, False, str(e)))

# R-SUB-PLAN-01 — subscribing grants the tier's quotas
def s1():
    q = E.quotas_for(2)
    assert q["seats"] == TIER[PLAN[2]["tier"]]["seats"] == 10
    assert q["projects"] == TIER[PLAN[2]["tier"]]["projects"] == 25
case("R-SUB-PLAN-01", "subscribe plan[2] -> quotas = planTier[2] (seats 10, projects 25)", s1)

# R-SUB-QUOTA-01 — action over the limit is rejected
def s2():
    r = E.check_quota(2, "seats", used=TIER[2]["seats"], delta=1)
    assert r["err"] == E.ERR_QUOTA_EXCEEDED and r["allowed"] is False
case("R-SUB-QUOTA-01", "usage == planTier[2].seats, +1 seat -> ERR_QUOTA_EXCEEDED", s2)

# R-SUB-QUOTA-02 — tier ladder is monotonic, row read directly
def s3():
    assert TIER[3]["seats"] >= TIER[2]["seats"] >= TIER[1]["seats"]
    assert E.quotas_for(3)["seats"] == TIER[3]["seats"] == 100
case("R-SUB-QUOTA-02", "ladder monotonic; planTier[3].seats = 100 (read row)", s3)

# R-SUB-CHANGE-02 — downgrade blocked when usage exceeds target
def s4():
    usage = {"projects": TIER[1]["projects"] + 1}      # over tier-1 project limit
    r = E.change_plan(current_pid=3, target_pid=1, usage=usage)
    assert r["err"] == E.ERR_USAGE_OVER_TARGET and r["plan"] == 3   # unchanged
case("R-SUB-CHANGE-02", "usage > planTier[1].projects -> ERR_USAGE_OVER_TARGET, unchanged", s4)

# R-SUB-FEAT-01 — feature gated by plan
def s5():
    assert E.feature_available(3, 201) is True         # planFeature[2] links plan3 -> feature201
    assert E.feature_available(1, 201) is False        # free plan: no SSO
case("R-SUB-FEAT-01", "feature[201] available to plan[3], not plan[1]", s5)

w = max(len(d) for _, d, _, _ in results)
for rid, desc, ok, err in results:
    print("%-16s %-*s  %s" % (rid, w, desc, "PASS" if ok else "FAIL " + err))
npass = sum(1 for r in results if r[2]); nfail = len(results) - npass
print()
print("%d passed, %d failed" % (npass, nfail))
