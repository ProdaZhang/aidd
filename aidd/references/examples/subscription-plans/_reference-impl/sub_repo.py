# Downstream implementation — loads config straight from the handoff's subscription.xlsx.
# Self-contained within the aidd repo (relative paths to the shipped xlsx reader + xlsx).
import zipfile, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "scripts"))
sys.path.insert(0, SCRIPTS)
import xlsx_dump  # the package ships this portable xlsx reader

def _sheets():
    z = zipfile.ZipFile(os.path.normpath(os.path.join(HERE, "..", "subscription.xlsx")))
    shared = xlsx_dump.load_shared_strings(z)
    out = {n: xlsx_dump.read_rows(z, sp, shared) for n, sp in xlsx_dump.sheet_map(z)}
    z.close(); return out
_S = _sheets()
def _rows(n): return _S[n][4:]  # skip the 4 self-describing header rows

PLAN = {int(r[0]): {"name": int(r[1]), "tier": int(r[2]),
                    "priceMonthly": int(r[3]), "trialDays": int(r[4])} for r in _rows("plan")}
TIER = {int(r[0]): {"seats": int(r[1]), "projects": int(r[2]),
                    "storageGb": int(r[3]), "apiPerDay": int(r[4])} for r in _rows("planTier")}
FEATURE = {int(r[0]): {"name": int(r[1])} for r in _rows("feature")}
PLAN_FEATURE = [{"id": int(r[0]), "plan": int(r[1]), "feature": int(r[2])} for r in _rows("planFeature")]
