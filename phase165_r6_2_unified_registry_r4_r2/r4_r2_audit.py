"""Read-only attribution audit for R4 candidate expansions."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys


def fingerprint(expansion):
    """Comparison fingerprint for one goal-scoped proposal, not proof identity."""
    rule = getattr(expansion, "rule", None)
    return (getattr(rule, "name", type(rule).__name__), repr(getattr(expansion, "subgoals", None)))


def evaluate_labeled(provider_id, provider, goals):
    observed = []
    errors = Counter()
    for index, goal in enumerate(goals):
        try:
            proposals = provider(goal)
            if not isinstance(proposals, tuple):
                raise TypeError("provider output must be tuple")
            for expansion in proposals:
                observed.append({"goal_index": index, "rule_name": getattr(getattr(expansion, "rule", None), "name", None),
                                 "fingerprint": fingerprint(expansion)})
        except Exception as exc:
            errors[type(exc).__name__] += 1
    return {"provider_id": provider_id, "goals_proposed": len(set(x["goal_index"] for x in observed)),
            "expansions": len(observed), "errors": dict(errors), "observations": observed}


def overlap_by_goal(left, right):
    a = Counter((x["goal_index"], tuple(x["fingerprint"])) for x in left["observations"])
    b = Counter((x["goal_index"], tuple(x["fingerprint"])) for x in right["observations"])
    return sum((a & b).values())


def classify_rule(rule, proposals, goals):
    if proposals["expansions"]:
        return "APPLICABLE_CANDIDATE_ONLY"
    if getattr(rule, "conclusion_pattern", None) is None:
        return "INVERSE_UNAVAILABLE_NO_CONCLUSION_PATTERN"
    if not getattr(rule, "premise_patterns", None):
        return "INVERSE_UNAVAILABLE_NO_PREMISE_PATTERNS"
    return "NO_PROPOSAL_ON_SAMPLED_GOALS_UNRESOLVED"


def audit(root: Path, max_goals: int = 250):
    root = root.resolve()
    sys.path.insert(0, str(root))
    from phase165_r6_2_unified_registry_r4.r4_audit import audit as r4_audit, unique_goals
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
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

    baseline = r4_audit(root, max_goals)
    if baseline["status"] != "APPLICABILITY_AUDITED":
        return {"status": "BLOCKED_R4", "baseline": baseline, "proofs_verified": 0}
    bridge = build_shared_typed_bridge()
    goals = unique_goals(tuple(bridge.registry._assertions.values()), max_goals)
    allowed = tuple(link.step.conclusion for link in bridge.proof_links if link.step is not None
                    and link.step.rule is ProofRule.GIVEN
                    and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
                    and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content)
    registry, report = build_unified_backward_rule_registry()
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
    providers = [evaluate_labeled(e.provider_id, e.provider, goals) for e in fixed.entries() + context.entries()]
    generic = evaluate_labeled("R26_GENERIC", build_generic_backward_expansion_provider(rules), goals)
    per_rule = []
    for index, rule in enumerate(rules):
        item = evaluate_labeled("r1.rule.{}".format(index), build_generic_backward_expansion_provider((rule,)), goals)
        per_rule.append({"rule_index": index, "rule_name": rule.name,
                         "classification": classify_rule(rule, item, goals),
                         "expansions": item["expansions"], "goals_proposed": item["goals_proposed"],
                         "errors": item["errors"]})
    from phase165_r52_r9_shared_math import shared_expansion_provider
    shared = evaluate_labeled("SHARED", shared_expansion_provider(bridge), goals)
    for item in providers:
        item["overlap_with_shared"] = overlap_by_goal(item, shared)
        del item["observations"]
    return {"phase": "165 R6-2 R4-2", "status": "ATTRIBUTION_AUDITED",
            "goals_examined": len(goals), "rule_count": len(rules), "provider_count": len(providers),
            "generic_r26": {k: v for k, v in generic.items() if k != "observations"},
            "shared_provider": {k: v for k, v in shared.items() if k != "observations"},
            "generic_shared_overlap": overlap_by_goal(generic, shared),
            "providers": providers, "rules": per_rule,
            "proofs_verified": 0, "production_modified": False, "full_pytest_run": False,
            "limitations": ["Rule index and rule.name are provisional identifiers, not verified factory IDs.",
                            "Matching fingerprints indicate candidate equality, not proof equivalence.",
                            "Per-rule and per-provider probes are not necessarily additive.",
                            "Witness and seeded paths are not separately attributed.",
                            "An absent proposal on these Goals does not prove rule inapplicability.",
                            "WITNESS_REQUIRED and BINDING_REQUIRED cannot be certified by this audit."]}


def markdown(data):
    lines = ["# Phase 165 R6-2 R4-2 候補帰属監査", "", "- status: `" + data["status"] + "`",
             "- Goal: " + str(data.get("goals_examined", 0)),
             "- 証明検証件数: 0", "", "## Provider", "",
             "| Provider ID | 候補 | 共有経路と重複 | エラー |", "|---|---:|---:|---|"]
    for p in data.get("providers", []):
        lines.append("| {} | {} | {} | {} |".format(p["provider_id"], p["expansions"], p["overlap_with_shared"], p["errors"]))
    lines += ["", "## R26 個別規則", "", "| Index | Rule name | 候補 | 判定 |", "|---:|---|---:|---|"]
    for r in data.get("rules", []):
        lines.append("| {} | {} | {} | {} |".format(r["rule_index"], r["rule_name"], r["expansions"], r["classification"]))
    lines += ["", "## 制限", ""] + ["- " + s for s in data.get("limitations", [])]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-goals", type=int, default=250)
    args = parser.parse_args()
    data = audit(args.root, args.max_goals)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "attribution.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "attribution.md").write_text(markdown(data), encoding="utf-8")
    print(json.dumps({k: v for k, v in data.items() if k in ("status", "goals_examined", "rule_count", "provider_count", "generic_r26", "shared_provider", "generic_shared_overlap", "proofs_verified")}, ensure_ascii=False, indent=2))
    if data["status"] != "ATTRIBUTION_AUDITED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
