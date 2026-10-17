"""R7: read-only semantic collision review of active R8 inference rules."""
from __future__ import annotations

import inspect
import json
from pathlib import Path

from phase165_r8_rule_provider import discover_inference_rules

PAIRS = (
    ("Freudenthal boundary range implies suspension epimorphism", "Freudenthal stable range implies suspension isomorphism"),
    ("generalized Hopf invariant enables composition law", "generalized Hopf invariant to EHP H equality"),
    ("Even exponent evaluates minus-one power to one", "Even scalar implies congruence to zero modulo two"),
    ("Odd exponent evaluates minus-one power to minus one", "Odd scalar implies congruence to one modulo two"),
    ("zero composition equality implies zero", "zero equality implies zero"),
)


def callable_evidence(fn):
    if fn is None:
        return {"present": False}
    code = getattr(fn, "__code__", None)
    return {
        "present": True,
        "module": getattr(fn, "__module__", None),
        "qualname": getattr(fn, "__qualname__", None),
        "code_names": list(code.co_names) if code else [],
        "code_constants": [repr(c) for c in code.co_consts if not inspect.iscode(c)] if code else [],
        "code_bytes_hex": code.co_code.hex() if code else None,
    }


def rule_evidence(rule):
    return {
        "name": rule.name,
        "description": rule.description,
        "conclusion_pattern": repr(rule.conclusion_pattern),
        "premise_patterns": [repr(p) for p in rule.premise_patterns],
        "guard": callable_evidence(getattr(rule, "guard", None)),
        "build_conclusion": callable_evidence(getattr(rule, "build_conclusion", None)),
    }


def classify_pair(left, right):
    a, b = rule_evidence(left), rule_evidence(right)
    if a["conclusion_pattern"] == "None" and b["conclusion_pattern"] == "None":
        return "NO_CONCLUSION_PATTERN__NOT_A_DUPLICATE_PROOF"
    if a["premise_patterns"] != b["premise_patterns"] or a["conclusion_pattern"] != b["conclusion_pattern"]:
        return "DISTINCT_DISPLAYED_PATTERNS"
    if a["guard"] != b["guard"] or a["build_conclusion"] != b["build_conclusion"]:
        return "SAME_PATTERNS_DIFFERENT_IMPLEMENTATION__MANUAL_REVIEW"
    return "MATCHING_OBSERVED_IMPLEMENTATION__MANUAL_REVIEW"


def main():
    rules, report = discover_inference_rules()
    by_name = {}
    for rule in rules:
        by_name.setdefault(rule.name, []).append(rule)
    pairs = []
    for left_name, right_name in PAIRS:
        ls, rs = by_name.get(left_name, []), by_name.get(right_name, [])
        if len(ls) != 1 or len(rs) != 1:
            raise RuntimeError(f"Expected exactly one active R8 rule per name: {left_name!r} / {right_name!r}")
        a, b = ls[0], rs[0]
        pairs.append({"left": rule_evidence(a), "right": rule_evidence(b), "classification": classify_pair(a, b)})
    data = {
        "phase": "165 R7 rule identity review",
        "mode": "READ_ONLY_R8_RULES",
        "active_rules": len(rules),
        "pairs_reviewed": len(pairs),
        "pairs": pairs,
        "identity_conclusion": "This audit does not establish semantic equivalence; do not merge or delete rules automatically.",
        "rule_id_status": "R8 is a factory discovery route; this audit cannot certify stable Rule IDs across all registries.",
        "retired_catalog_called": False,
        "production_modified": False,
        "full_pytest_run": False,
    }
    path = Path(__file__).resolve().parent / "audit_result.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "phase": data["phase"],
        "active_rules": data["active_rules"],
        "pairs_reviewed": data["pairs_reviewed"],
        "classifications": [p["classification"] for p in pairs],
        "production_modified": False,
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2))
    print("Audit saved:", path)
    return data


if __name__ == "__main__":
    main()
