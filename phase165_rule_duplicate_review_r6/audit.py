"""Review the five signature collisions from R5 without invoking retired catalogs."""
from __future__ import annotations

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


def describe_rule(rule):
    """Return readable rule metadata; descriptions are not proof of equivalence."""
    return {
        "name": rule.name,
        "description": rule.description,
        "conclusion_type": type(rule.conclusion_pattern).__name__ if rule.conclusion_pattern is not None else None,
        "conclusion_pattern": repr(rule.conclusion_pattern),
        "premises": [
            {
                "statement_type": getattr(p.statement_type, "__name__", str(p.statement_type)),
                "relation_type": str(p.relation_type),
                "relation_pattern": repr(p.relation_pattern),
                "statement_pattern": repr(p.statement_pattern),
            }
            for p in rule.premise_patterns
        ],
        "guard_present": bool(getattr(rule, "guard", None)),
        "build_conclusion_present": bool(getattr(rule, "build_conclusion", None)),
    }


def classify_pair(a, b):
    """Distinguish a superficial collision from an unresolved equivalence check."""
    if a["conclusion_type"] is None and b["conclusion_type"] is None:
        return "NO_CONCLUSION_PATTERNS__NAME_AND_DESCRIPTION_REVIEW_REQUIRED"
    if a["conclusion_type"] != b["conclusion_type"] or a["conclusion_pattern"] != b["conclusion_pattern"]:
        return "DIFFERENT_CONCLUSION_PATTERNS"
    if a["premises"] != b["premises"]:
        return "DIFFERENT_PREMISE_PATTERNS"
    return "SAME_DISPLAYED_PATTERNS__SEMANTIC_REVIEW_REQUIRED"


def main():
    rules, _ = discover_inference_rules()
    by_name = {rule.name: rule for rule in rules}
    if len(by_name) != len(rules):
        raise RuntimeError("Unexpected duplicate rule names in R8 discovery")
    results = []
    for names in PAIRS:
        missing = [name for name in names if name not in by_name]
        if missing:
            raise RuntimeError("R5 candidate missing from active rule discovery: " + ", ".join(missing))
        first, second = (describe_rule(by_name[name]) for name in names)
        results.append({"pair": list(names), "classification": classify_pair(first, second), "first": first, "second": second})
    report = {
        "phase": "165 R6 signature collision review",
        "mode": "READ_ONLY_ACTIVE_R8_ONLY",
        "rule_count": len(rules),
        "pairs_reviewed": len(results),
        "review": results,
        "warning": "This report does not certify semantic equivalence or full unified registry uniqueness.",
        "retired_catalog_called": False,
        "full_pytest_run": False,
    }
    path = Path(__file__).with_name("audit_result.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"phase": report["phase"], "rule_count": report["rule_count"], "pairs_reviewed": report["pairs_reviewed"], "classifications": [x["classification"] for x in results], "full_pytest_run": False}, ensure_ascii=False, indent=2))
    print("Audit saved:", path)
    return report


if __name__ == "__main__":
    main()
