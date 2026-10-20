"""Phase 166 R3-T: read-only production diagnostic for pi_5^4."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization
from proof import ProofRule
from toda_rules import Toda45IsomorphismStatement
from web_group_proof import build_standard_web_group_proof_view


def inspect() -> dict:
    bridge = build_shared_typed_bridge()
    given = tuple(link for link in bridge.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN)
    available = tuple(link.step.conclusion for link in given)
    goals = registered_group_goal_candidates(bridge, n=4, k=1)
    cases = []
    for goal in goals:
        provider = shared_expansion_provider(bridge, proof_target=goal)
        shared = provider(goal)
        direct = expand_registered_toda45_finite_cyclic_goal(goal, available)
        eta = expand_registered_eta_specialization(goal, available)
        cases.append({
            "goal": repr(goal),
            "shared_expansion_count": len(shared),
            "shared_expansion_rules": [str(getattr(x.rule, "name", None)) for x in shared],
            "direct_toda45_expansion_count": len(direct),
            "eta_specialization_count": len(eta),
            "given_exact_goal_count": sum(x == goal for x in available),
        })
    web = {}
    for n, k in ((3, 1), (4, 1)):
        try:
            view = build_standard_web_group_proof_view(n, k, 2, "narrative")
            body = "\n".join(line.prefix + " " + " ".join(seg.value for seg in line.segments) for line in view.rendered_lines)
            web[f"pi_{n+k}^{n}"] = {
                "line_count": len(view.rendered_lines),
                "has_goal": "証明対象" in body,
                "has_references": "使用する結果" in body,
                "has_proof": "証明" in body,
                "text": body,
            }
        except Exception as exc:
            web[f"pi_{n+k}^{n}"] = {"error": type(exc).__name__ + ": " + str(exc)}
    return {
        "phase": "166 R3-T", "mode": "read_only", "production_code_modified": False,
        "pi54_candidate_count": len(goals), "pi54_candidates": cases,
        "toda45_concrete_given_count": sum(isinstance(x, Toda45IsomorphismStatement) for x in available),
        "given_type_counts": {name: sum(type(x).__name__ == name for x in available) for name in sorted({type(x).__name__ for x in available})},
        "web_views": web, "full_pytest_run": False,
    }


def main() -> None:
    report = inspect()
    path = Path(__file__).with_name("r3t_audit.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps({key: val for key, val in report.items() if key != "web_views"}, ensure_ascii=False, indent=2, default=str))
    print("REPORT:", path)


if __name__ == "__main__":
    main()
