"""Phase 165 R12: read-only production rule inventory and pi43 proof gap audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r8_rule_provider import build_production_rule_provider
from phase165_r10_rule_registry import build_rule_registry
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES


def make_report() -> dict:
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    provider, provider_report = build_production_rule_provider()
    rules = registry.rules()
    keywords = ("quotient", "cyclic", "kernel", "exactness", "surject", "isomorph", "generator")
    matched = [
        {"rule_id": item.rule_id, "name": item.rule.name,
         "backward_pattern_candidate": item.backward_pattern_candidate}
        for item in registry.entries
        if any(word in (item.rule_id + " " + item.rule.name).lower() for word in keywords)
    ]
    return {
        "phase": "165 R12",
        "mode": "READ_ONLY_GAP_AUDIT_NOT_PROOF_GENERATION",
        "registered_rule_count": len(rules),
        "provider_rule_count": len(provider_report.rule_names),
        "inverse_pattern_candidates": sum(item.backward_pattern_candidate for item in registry.entries),
        "required_input_factories": [x for x in registry.skipped_factories if x.endswith(":requires-input")],
        "relevant_rules": matched,
        "next_required_check": "typed quotient/cyclic structure and verified pi43 premises",
        "proof_generated": False,
        "proofstep_verified": False,
        "full_pytest_run": False,
    }


def main() -> None:
    result = make_report()
    output = Path(__file__).resolve().parent / "report.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
