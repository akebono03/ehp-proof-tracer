"""Production R9/R10 readiness audit with no implied source certification."""
import json
from pathlib import Path
from phase165_r9_production_wiring import discover_goal_search_inputs
from unified_statement_registry import AssertionOrigin


def main():
    inputs = discover_goal_search_inputs()
    fixed = tuple(a for a in inputs.bridge.registry._assertions.values() if a.origin is AssertionOrigin.FIXED_STATEMENT)
    linked = tuple(link.assertion_id for link in inputs.bridge.proof_links)
    eligible = tuple(a.assertion_id for a in fixed if a.assertion_id in linked and a.assertion_id in inputs.verified_assertion_ids and a.available_after_position is not None)
    report = {
        "phase": "165 R10",
        "mode": "COMMON_GOAL_DIAGNOSTICS_NO_PROMOTION",
        "production_fixed_assertions": len(fixed),
        "rule_count": len(inputs.rule_report.rule_names),
        "patternless_rule_count": len(inputs.rule_report.skipped_rules),
        "verified_ids": len(inputs.verified_assertion_ids),
        "linked_fixed_steps": len(linked),
        "eligible_linked_fixed_steps": len(eligible),
        "diagnostic_provider_connected": True,
        "mathematical_goal_supplied": False,
        "pi5_3_proved": False,
        "full_pytest_run": False,
    }
    output = Path("phase165_r10_output")
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text("# Phase 165 R10 — 共通証明診断\n\n" + "\n".join(f"- {key}: {value}" for key, value in report.items()) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
