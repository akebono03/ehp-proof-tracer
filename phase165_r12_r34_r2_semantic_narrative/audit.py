from __future__ import annotations
import json
from pathlib import Path
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

def main():
    result=search_group_from_registered_goal(n=3,k=1)
    narrative=render_partial_proof_markdown(result)
    view=build_partial_web_group_proof_view(result)
    raw=("infinite cyclic quotient structure", "KernelMultipleStatement（数式表示未対応）", "CyclicStructureStatement（数式表示未対応）", "第一同型定理と無限巡回群の商群構造より,\n")
    report={"phase":"165 R12-R34-R2","search_status":result.status.value,"open_goals":len(result.open_goals),"provenance":view.key,"raw_internal_visible":any(x in narrative for x in raw),"first_isomorphism_explained":"第一同型定理" in narrative,"kernel_shown":"\\ker E" in narrative,"source_issues":narrative.count("要出典確認"),"final_count":narrative.count("以上より"),"has_box":narrative.rstrip().endswith("□"),"full_pytest_run":False}
    here=Path(__file__).resolve().parent
    (here/"audit_result.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
    (here/"public_narrative.md").write_text(narrative,encoding="utf8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if report["search_status"]!="complete" or report["open_goals"] or report["raw_internal_visible"] or not report["first_isomorphism_explained"] or report["final_count"]!=1 or not report["has_box"]:
        raise SystemExit("R12-R34-R2 narrative acceptance FAILED")
if __name__=="__main__": main()
