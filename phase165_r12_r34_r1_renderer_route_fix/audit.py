from __future__ import annotations
from pathlib import Path
import json
from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

def main():
    result = search_group_from_registered_goal(n=3,k=1)
    narrative = render_partial_proof_markdown(result)
    view = build_partial_web_group_proof_view(result)
    report = {"phase":"165 R12-R34-R1", "search_status":result.status.value,
      "open_goal_count":len(result.open_goals),"provenance_key":view.key,
      "raw_quotient_rule_visible":"infinite cyclic quotient structure" in narrative,
      "first_isomorphism_explained":"第一同型定理" in narrative,
      "final_conclusion_count":narrative.count("以上より"),
      "has_proof_box":narrative.rstrip().endswith("□"),"full_pytest_run":False}
    root=Path(__file__).resolve().parent
    (root/"audit_result.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf8")
    (root/"public_narrative.md").write_text(narrative,encoding="utf8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if (report["search_status"]!="complete" or report["open_goal_count"] or report["raw_quotient_rule_visible"]
        or not report["first_isomorphism_explained"] or report["final_conclusion_count"]!=1 or not report["has_proof_box"]):
        raise SystemExit("R12-R34-R1 Narrative acceptance FAILED")
if __name__=="__main__":main()
