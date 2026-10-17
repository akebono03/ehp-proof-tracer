"""Read-only applicability audit of the unified rule/provider connections."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys


def unique_goals(assertions, limit: int):
    if limit < 1:
        raise ValueError("limit must be positive")
    output = []
    for assertion in assertions:
        goal = getattr(assertion, "content", None)
        if goal is None or any(type(goal) is type(old) and goal == old for old in output):
            continue
        output.append(goal)
    return tuple(output[:limit])


def evaluate_provider(provider, goals):
    """Return proposal statistics without asserting proof success."""
    result = {"goals_proposed": 0, "expansions": 0, "errors": {}, "sample_errors": []}
    for i, goal in enumerate(goals):
        try:
            expansions = provider(goal)
            if not isinstance(expansions, tuple):
                raise TypeError("provider must return tuple")
            result["expansions"] += len(expansions)
            result["goals_proposed"] += bool(expansions)
        except Exception as exc:
            key = type(exc).__name__
            result["errors"][key] = result["errors"].get(key, 0) + 1
            if len(result["sample_errors"]) < 3:
                result["sample_errors"].append({"goal_index": i, "error": key, "detail": str(exc)[:160]})
    return result


def check_adapter_removed(root: Path):
    source = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    return "expand_existing_pi43_rules" not in source and "phase165_r52_r23_existing_rule_adapter" not in source


def audit(root: Path, max_goals=250):
    root = root.resolve()
    sys.path.insert(0, str(root))
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
    from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import build_unified_backward_rule_registry
    from phase165_r6_2_unified_registry_r3_r3.provider_registry import build_shared_expansion_provider_registry
    from phase165_r6_2_unified_registry_r3_r4.context_provider_registry import build_context_expansion_provider_registry
    from phase165_r14_r6_generic_iso import expand_generic_iso_goal
    from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
    from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
    from phase165_r14_r14_diagonal_and_prop42 import expand_diagonal_suspension
    from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
    from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization
    from phase165_r57_r19_delta_image_backward import expand_registered_delta_image_goal
    from phase165_r57_r20_general_specialization import expand_cited_general_specialization
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    if not check_adapter_removed(root):
        return {"status": "BLOCKED_LEGACY_ADAPTER", "proofs_verified": 0}
    bridge = build_shared_typed_bridge()
    raw = tuple(bridge.registry._assertions.values())
    goals = unique_goals(raw, max_goals)
    allowed = tuple(link.step.conclusion for link in bridge.proof_links if link.step is not None
                    and link.step.rule is ProofRule.GIVEN
                    and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                    and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content)
    registry, rule_report = build_unified_backward_rule_registry()
    rules = registry.rules()
    fixed = build_shared_expansion_provider_registry(
        expand_generic_iso_goal=expand_generic_iso_goal,
        expand_generic_ehp_hopf_goal=expand_generic_ehp_hopf_goal,
        expand_delta_zero_from_suspension_iso=expand_delta_zero_from_suspension_iso,
        expand_diagonal_suspension=expand_diagonal_suspension)
    context = build_context_expansion_provider_registry(
        available=allowed, prior_conclusions=(),
        expand_registered_toda45_finite_cyclic_goal=expand_registered_toda45_finite_cyclic_goal,
        expand_registered_eta_specialization=expand_registered_eta_specialization,
        expand_registered_delta_image_goal=expand_registered_delta_image_goal,
        expand_cited_general_specialization=expand_cited_general_specialization)
    details = []
    for entry in fixed.entries() + context.entries():
        row = {"provider_id": entry.provider_id, "origin": entry.origin, "registration_status": entry.status}
        row.update(evaluate_provider(entry.provider, goals))
        details.append(row)
    generic = evaluate_provider(build_generic_backward_expansion_provider(rules), goals)
    shared = evaluate_provider(shared_expansion_provider(bridge), goals)
    return {"phase": "165 R6-2 unified registry R4", "status": "APPLICABILITY_AUDITED",
            "adapter_removed": True, "registered_goal_count": len(raw), "goals_examined": len(goals),
            "r1_registered_rules": len(rules), "registered_providers": len(details),
            "provider_results": details, "generic_r26": generic, "shared_provider": shared,
            "proofs_verified": 0, "production_modified": False, "full_pytest_run": False,
            "limitations": ["Emitted GoalExpansion is not a verified proof.",
                            "Provider results are not additive: paths can overlap.",
                            "Runtime checks are limited to registered assertion-content Goals.",
                            "Witness and seeded paths are included in shared aggregate, not individually attributed.",
                            "R8 argument-required factories are not automatically instantiated."]}


def markdown(data):
    lines = ["# Phase 165 R6-2 R4：統一規則適用監査", "", "- status: `" + data["status"] + "`",
             "- 検査 Goal: " + str(data.get("goals_examined", 0)),
             "- 台帳規則: " + str(data.get("r1_registered_rules", 0)),
             "- 接続 Provider: " + str(data.get("registered_providers", 0)),
             "- 証明成立の検証: 0", "", "| Provider ID | 適用 Goal | 候補 | エラー |", "|---|---:|---:|---|"]
    for item in data.get("provider_results", []):
        lines.append("| {} | {} | {} | {} |".format(item["provider_id"], item["goals_proposed"], item["expansions"], str(item["errors"])))
    for key in ("generic_r26", "shared_provider"):
        item = data.get(key, {})
        lines.append("| {} | {} | {} | {} |".format(key, item.get("goals_proposed", 0), item.get("expansions", 0), item.get("errors", {})))
    lines += ["", "## 制約", ""] + ["- " + note for note in data.get("limitations", [])]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-goals", type=int, default=250)
    args = parser.parse_args()
    data = audit(args.root, args.max_goals)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "applicability.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "applicability.md").write_text(markdown(data), encoding="utf-8")
    print(json.dumps({k: v for k, v in data.items() if k in ("status", "adapter_removed", "goals_examined", "r1_registered_rules", "registered_providers", "generic_r26", "shared_provider", "proofs_verified", "full_pytest_run")}, ensure_ascii=False, indent=2))
    if data["status"] != "APPLICABILITY_AUDITED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
