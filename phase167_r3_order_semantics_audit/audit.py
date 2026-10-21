from __future__ import annotations

import json
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = Path(__file__).resolve().parent / "r3_order_semantics_report.json"


def run_audit() -> dict:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r57_r10_step_narrative import ordered_proof_ancestry
    from phase166_r3c_publication_order import precedes_citing_assertion
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from proof import ProofRule, find_inference_matches_for_rule
    from phase165_r12_r2_quotient_rules import (
        first_isomorphism_quotient_inference_rule,
        infinite_cyclic_quotient_structure_inference_rule,
    )

    result = search_group_from_registered_goal(n=3, k=1)
    bridge = build_shared_typed_bridge()
    roots = [s for s in result.proven_steps if s.conclusion == result.conclusion
             and s.rule is ProofRule.INFERENCE]
    root = roots[0] if len(roots) == 1 else None
    steps = ordered_proof_ancestry(root) if root is not None else ()
    rule_factories = (
        first_isomorphism_quotient_inference_rule,
        infinite_cyclic_quotient_structure_inference_rule,
    )
    factory_rules = {r.name: r for r in (make() for make in rule_factories)}
    replay = []
    for i, step in enumerate(steps, 1):
        name = getattr(step.inference_rule, "name", None)
        if name not in factory_rules:
            continue
        matches = find_inference_matches_for_rule(factory_rules[name], tuple(step.premises))
        successful = [m for m in matches if m.inference_rule.conclusion_pattern is not None]
        # Match bindings are structurally checked; to validate the concrete
        # conclusion, reconstruct through the existing public application API.
        from proof import apply_inference_match
        reproduced = []
        errors = []
        for match in successful:
            try:
                reproduced.append(apply_inference_match(match).conclusion == step.conclusion)
            except Exception as exc:
                errors.append(type(exc).__name__ + ": " + str(exc))
        replay.append({
            "step": i, "rule": name, "premises": len(step.premises),
            "match_count": len(matches), "conclusion_reproduced": any(reproduced),
            "errors": errors,
        })

    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assertions = list(bridge.registry._assertions.values())
    given_checks = []
    for i, step in enumerate(steps, 1):
        if step.rule is not ProofRule.GIVEN:
            continue
        ref = getattr(step.inference_rule, "literature_reference", None)
        locator = getattr(ref, "locator", None)
        matches = []
        for assertion in assertions:
            if assertion.content != step.conclusion:
                continue
            source = bridge.registry.reference(assertion.reference_id)
            matches.append({
                "assertion_id": assertion.assertion_id,
                "reference_id": assertion.reference_id,
                "publication_position": source.publication_position,
                "component_position": assertion.component_position,
                "precedes_target": (
                    precedes_citing_assertion(bridge, assertion.assertion_id, citing_id)
                    if citing_id is not None else None
                ),
            })
        status = (
            "NO_CITING_ASSERTION" if citing_id is None else
            "NO_MATCHING_ASSERTION" if not matches else
            "VERIFIED" if any(m["precedes_target"] is True for m in matches) else
            "NOT_PRECEDING"
        )
        given_checks.append({
            "step": i, "locator": locator, "status": status,
            "matching_assertions": matches,
        })
    report = {
        "phase": "167 R3",
        "mode": "READ_ONLY_PUBLICATION_AND_FORWARD_REPLAY",
        "status": result.status.value,
        "step_count": len(steps),
        "citing_assertion_id": citing_id,
        "given_checks": given_checks,
        "selected_rule_replay": replay,
        "all_givens_verified": bool(given_checks) and all(g["status"] == "VERIFIED" for g in given_checks),
        "selected_rules_reproduced": len(replay) == 2 and all(r["conclusion_reproduced"] for r in replay),
        "scope_limitations": [
            "A reproduced rule application checks implementation consistency, not a formal mathematical proof.",
            "Only the two specified quotient inference rules are replayed.",
            "Publication checks use matching assertion content and actual registry ordering, never locator-only acceptance.",
            "Missing or ambiguous source mappings remain visible in the report.",
        ],
        "full_pytest_run": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    try:
        report = run_audit()
    except Exception:
        REPORT.write_text(json.dumps({"error": traceback.format_exc()},
                                     ensure_ascii=False, indent=2), encoding="utf-8")
        raise
    print(json.dumps({
        "status": report["status"],
        "step_count": report["step_count"],
        "citing_assertion_id": report["citing_assertion_id"],
        "given_checks": [{k: item[k] for k in ("step","locator","status")} for item in report["given_checks"]],
        "selected_rule_replay": report["selected_rule_replay"],
        "all_givens_verified": report["all_givens_verified"],
        "selected_rules_reproduced": report["selected_rules_reproduced"],
        "report": str(REPORT),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
