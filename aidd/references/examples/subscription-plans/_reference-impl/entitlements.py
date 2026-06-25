# Downstream implementation of the subscription rules — built only from the handoff package.
from sub_repo import PLAN, TIER, PLAN_FEATURE

ERR_OK, ERR_QUOTA_EXCEEDED, ERR_USAGE_OVER_TARGET = 0, 1, 2
RESOURCES = ("seats", "projects", "storageGb", "apiPerDay")

def quotas_for(pid):                                  # R-SUB-PLAN-01
    """Granted quotas = the plan's tier row (read directly)."""
    return dict(TIER[PLAN[pid]["tier"]])

def check_quota(pid, resource, used, delta=1):        # R-SUB-QUOTA-01 / -02
    """Allowed only while used + delta <= the tier limit; else ERR_QUOTA_EXCEEDED."""
    limit = TIER[PLAN[pid]["tier"]][resource]
    ok = used + delta <= limit
    return {"err": ERR_OK if ok else ERR_QUOTA_EXCEEDED, "limit": limit, "used": used, "allowed": ok}

def change_plan(current_pid, target_pid, usage):      # R-SUB-CHANGE-01 / -02
    """Downgrade guard: reject if any current usage exceeds the target tier's limit; plan unchanged."""
    target = TIER[PLAN[target_pid]["tier"]]
    for r in RESOURCES:
        if usage.get(r, 0) > target[r]:
            return {"err": ERR_USAGE_OVER_TARGET, "plan": current_pid}
    return {"err": ERR_OK, "plan": target_pid}

def feature_available(pid, fid):                      # R-SUB-FEAT-01
    return any(r["plan"] == pid and r["feature"] == fid for r in PLAN_FEATURE)
