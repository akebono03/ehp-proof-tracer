"""Read-only provenance comparison of three existing inverse rule pathways."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys


def fingerprint(expansion):
    """Equality key within one goal, not a proof or mathematical identity."""
    return (getattr(expansion.rule, "name", type(expansion.rule).__name__),
            repr(expansion.subgoals))


def cited_steps(bridge):
    """Use only matching typed, cited GIVEN links."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    output = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if link.step.conclusion != assertion.content:
            continue
        output.append((link.assertion_id, link.step))
    return tuple(output)


def enumerate_proposals(goals, paths, cited, rule_ids):
    """Compare outputs without assigning an unobserved source witness."""
    rows = []
    errors = Counter()
    for goal_index, goal in enumerate(goals):
        for provider_id, provider in paths:
            try:
                expansions = provider(goal)
                if not isinstance(expansions, tuple):
                    raise TypeError("provider output must be tuple")
                for expansion in expansions:
                    rule = expansion.rule
                    key = fingerprint(expansion)
                    matched = sorted({assertion_id for assertion_id, step in cited
                                      if any(step.conclusion == sub for sub in expansion.subgoals)})
                    rows.append({"goal_index": goal_index, "provider_id": provider_id,
                                 "rule_id": rule_ids.get(id(rule)),
                                 "rule_name": getattr(rule, "name", type(rule).__name__),
                                 "rule_id_status": "EXACT_OBJECT" if id(rule) in rule_ids else "UNRESOLVED",
                                 "goal_repr": repr(goal),
                                 "subgoal_reprs": [repr(x) for x in expansion.subgoals],
                                 "fingerprint": list(key),
                                 "matching_cited_premise_ids": matched,
                                 "witness_usage_status": ("POSSIBLE_PREMISE_MATCH_NOT_PROVEN_USED"
                                                          if matched else "UNRESOLVED")})
            except Exception as exc:
                errors[(provider_id, type(exc).__name__)] += 1
    groups = defaultdict(list)
    for index, row in enumerate(rows):
        groups[(row["goal_index"], tuple(row["fingerprint"]))].append(index)
    for indices in groups.values():
        for index in indices:
            rows[index]["overlap_providers"] = sorted({rows[other]["provider_id"] for other in indices if other != index})
    return rows, [{"provider_id": k[0], "error": k[1], "count": count}
                  for k, count in sorted(errors.items())]


def audit(root: Path, max_goals: int = 250):
    root = root.resolve()
    sys.path.insert(0, str(root))
    from phase165_r6_2_unified_registry_r4.r4_audit import check_adapter_removed, unique_goals
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import build_unified_backward_rule_registry
    from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
    from phase165_r6_2_r2_verified_inverse import reverse_rules_from_witnesses
    from phase165_r6_2_r4_seeded_goals import generate_seeded_backward_goals

    if not check_adapter_removed(root):
        return {"status": "BLOCKED_LEGACY_ADAPTER", "proofs_verified": 0}
    bridge = build_shared_typed_bridge()
    goals = unique_goals(tuple(bridge.registry._assertions.values()), max_goals)
    cited = cited_steps(bridge)
    steps = tuple(step for _, step in cited)
    registry, _ = build_unified_backward_rule_registry()
    rules = registry.rules()
    # Registry may expose rule ids on entries; object identity stays provisional
    # if its entries do not expose stable factory IDs.
    rule_ids = {}
    if hasattr(registry, "entries"):
        for entry in registry.entries():
            identifier = getattr(entry, "rule_id", None)
            rule = getattr(entry, "rule", None)
            if isinstance(identifier, str) and rule is not None:
                rule_ids[id(rule)] = identifier
    paths = (
        ("R26_GENERIC", build_generic_backward_expansion_provider(rules)),
        ("WITNESS_R2", lambda goal: reverse_rules_from_witnesses(goal, rules, steps, max_combinations=2048)),
        ("SEEDED_R4", lambda goal: generate_seeded_backward_goals(goal, rules, steps, max_candidates=2048)),
        ("SHARED", shared_expansion_provider(bridge)),
    )
    rows, errors = enumerate_proposals(goals, paths, cited, rule_ids)
    counts = Counter(row["provider_id"] for row in rows)
    overlap = Counter((row["provider_id"], other) for row in rows for other in row["overlap_providers"])
    return {"phase": "165 R6-2 R4-3", "status": "PROVENANCE_AUDITED",
            "goals_examined": len(goals), "registered_rules": len(rules),
            "cited_given_links": len(cited), "counts_by_provider": dict(sorted(counts.items())),
            "overlap_by_provider": [{"left": pair[0], "right": pair[1], "rows": n}
                                    for pair, n in sorted(overlap.items())],
            "errors": errors, "observations": rows,
            "proofs_verified": 0, "production_modified": False, "full_pytest_run": False,
            "limitations": [
                "An object rule ID is accepted only if exposed by the registry entry.",
                "Matching cited premise IDs do not prove which witness bound a variable.",
                "Witness/Seeded returns do not expose the witness-selection trace.",
                "Fingerprint overlap compares proposals, not proofs.",
                "SHARED may deduplicate and gate candidates, so totals need not add.",
                "This audit does not execute recursive proof reconstruction."]}


def markdown(data):
    lines = ["# Phase 165 R6-2 R4-3 候補生成根拠監査", "", "- 状態: `" + data["status"] + "`",
             "- 検査 Goal: " + str(data.get("goals_examined", 0)),
             "- 証明検証数: 0", "", "## 経路別の候補", "",
             "| Provider ID | 候補数 |", "|---|---:|"]
    for key, value in data.get("counts_by_provider", {}).items():
        lines.append("| {} | {} |".format(key, value))
    lines.extend(["", "## エラー", "", "```json", json.dumps(data.get("errors", []), ensure_ascii=False, indent=2), "```", "", "## 制約", ""])
    lines.extend("- " + s for s in data.get("limitations", []))
    lines.extend(["", "候補ごとの Rule ID、前提、重複、出典候補は JSON を参照。", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-goals", type=int, default=250)
    args = parser.parse_args()
    data = audit(args.root, args.max_goals)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "provenance.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "provenance.md").write_text(markdown(data), encoding="utf-8")
    print(json.dumps({k: v for k, v in data.items() if k != "observations"}, ensure_ascii=False, indent=2))
    if data["status"] != "PROVENANCE_AUDITED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
