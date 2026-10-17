"""Phase 165 R8: read-only comparison of the zero-equality rule pair."""
from __future__ import annotations

import json
from pathlib import Path

from relation_rules import (
    zero_composition_equality_implies_zero_inference_rule,
    zero_equality_implies_zero_inference_rule,
)


def classify_pair() -> dict[str, object]:
    general = zero_equality_implies_zero_inference_rule()
    composition_only = zero_composition_equality_implies_zero_inference_rule()
    same_premises = general.premise_patterns == composition_only.premise_patterns
    same_conclusion = general.conclusion_pattern == composition_only.conclusion_pattern
    general_guard = general.match_guard is not None
    composition_guard = composition_only.match_guard is not None
    return {
        "general_name": general.name,
        "composition_name": composition_only.name,
        "same_premises": same_premises,
        "same_conclusion": same_conclusion,
        "general_has_guard": general_guard,
        "composition_has_guard": composition_guard,
        "classification": (
            "SAME_PATTERNS_DIFFERENT_APPLICABILITY__KEEP_BOTH"
            if same_premises and same_conclusion and not general_guard and composition_guard
            else "REQUIRES_FURTHER_REVIEW"
        ),
        "removal_performed": False,
        "full_pytest_run": False,
    }


def main() -> None:
    result = {"phase": "165 R8 zero-relation identity review", **classify_pair()}
    output = Path(__file__).resolve().parent / "audit_result.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Audit saved:", output)


if __name__ == "__main__":
    main()
