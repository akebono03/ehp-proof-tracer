from __future__ import annotations
import json
from pathlib import Path
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view


def main():
    result = search_group_from_registered_goal(n=3,k=1)
    narrative = render_partial_proof_markdown(result)
    view = build_partial_web_group_proof_view(result)
    report = {
        "phase":"165 R12-R34", "search_status":result.status.value,
        "unresolved_count":len(result.open_goals),
        "provenance_key":view.key,
        "raw_quotient_rule_visible":"infinite cyclic quotient structure" in narrative,
        "first_isomorphism_explained":"第一同型定理" in narrative,
        "final_conclusion_count":narrative.count("以上より"),
        "has_proof_box":narrative.rstrip().endswith("□"),
        "full_pytest_run":False,
    }
    output=Path(__file__).resolve().parent
    (output/"audit_result.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
    (output/"public_narrative.md").write_text(narrative,encoding="utf8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if result.status is not ProofSearchStatus.COMPLETE:
        raise SystemExit("proof incomplete: see audit_result.json")


if __name__ == "__main__":
    main()
