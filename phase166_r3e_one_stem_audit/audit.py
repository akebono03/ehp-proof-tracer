"""Read-only Phase 166 R3-E: current production 1-stem outcomes."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from proof import ProofRule


def inspect_case(n: int, k: int) -> dict:
    result = search_group_from_registered_goal(n=n, k=k)
    view = build_group_proof_progress_view(n=n, k=k, max_depth=2)
    markdown = render_partial_proof_markdown(result)
    return {
        "n": n,
        "k": k,
        "status": result.status.value,
        "complete": result.status is ProofSearchStatus.COMPLETE,
        "view_key": view.key,
        "view_mode": view.mode,
        "view_partial": view.partial_result,
        "reference_labels": list(result.references),
        "proof_step_count": len(result.proven_steps),
        "given_step_count": sum(step.rule is ProofRule.GIVEN for step in result.proven_steps),
        "inference_step_count": sum(step.rule is ProofRule.INFERENCE for step in result.proven_steps),
        "conclusion": repr(result.conclusion),
        "open_goals": [repr(item) for item in result.open_goals],
        "diagnostics": list(result.diagnostics),
        "markdown": markdown,
    }


def main() -> None:
    output = Path(__file__).resolve().parent / "audit_result.json"
    cases = [inspect_case(3, 1), inspect_case(4, 1)]
    report = {"phase": "166 R3-E", "production_code_modified": False,
              "full_pytest_run": False, "cases": cases}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    for item in cases:
        print(json.dumps({key: value for key, value in item.items() if key != "markdown"}, ensure_ascii=False, indent=2))
    print("Full audit report:", output)


if __name__ == "__main__":
    main()
