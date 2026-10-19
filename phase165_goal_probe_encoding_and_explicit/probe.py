import json
import sys
import traceback
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from expression import GeneratorSymbol, HomotopyElement, Composition
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from proof import Relation
from phase165_r55_nk_only_goal import search_group_from_registered_goal

def eta(n):
    return HomotopyElement(
        name="η" + str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")),
        dimension=n, source=n+1, target=n,
        generator=GeneratorSymbol(family="η", index=n)
    )

def main():
    cases = ((2,1,None),(3,1,None),
             (3,2,Relation(TodaPrimaryGroup(5,3),
                           FiniteCyclicGroup(2, Composition(eta(3),eta(4))))))
    results = []
    for n,k,goal in cases:
        name = f"pi_{n+k}^{n}"
        try:
            result = search_group_from_registered_goal(n=n,k=k,goal=goal)
            record = {
                "group":name,
                "explicit_goal":goal is not None,
                "status":result.status.name,
                "proven_steps":len(result.proven_steps),
                "open_goals":len(result.open_goals),
                "conclusion":str(result.conclusion),
                "diagnostics":list(result.diagnostics),
                "proof_verified":False,
            }
        except Exception as exc:
            record = {"group":name,"explicit_goal":goal is not None,
                      "exception":repr(exc),"traceback":traceback.format_exc(),
                      "proof_verified":False}
        results.append(record)
        print(json.dumps(record,ensure_ascii=False),flush=True)
    target = root/"phase165_r6_audit_results"/"goal_probe_explicit"
    target.mkdir(parents=True,exist_ok=True)
    (target/"report.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
