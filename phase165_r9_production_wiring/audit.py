"""Live R9 wiring inspection, no proof-eligibility claims."""
import json
from pathlib import Path

from phase165_r9_production_wiring import discover_goal_search_inputs


def main():
    inputs = discover_goal_search_inputs()
    report = {
        "phase": "165 R9",
        "mode": "LIVE_GOAL_ENTRY_AND_RULE_PROVIDER_CONNECTED",
        "fixed_registry_assertions": len(inputs.bridge.registry._assertions),
        "discovered_rule_count": len(inputs.rule_report.rule_names),
        "patternless_rule_count": len(inputs.rule_report.skipped_rules),
        "verified_assertion_count": len(inputs.verified_assertion_ids),
        "goal_only_entry_auto_discovers_inputs": True,
        "group_structure_and_citing_context_auto_derived": False,
        "pi5_3_goal_only_proved": False,
        "remaining_blockers": [
            "NO_INDEPENDENTLY_VERIFIED_SEMANTIC_BINDINGS",
            "NO_APPROVED_CITATION_AVAILABILITY",
            "NO_VERIFIED_GOAL_STATEMENT_AND_CITING_CONTEXT",
            "NON_PATTERN_RULES_NOT_INVERTIBLE",
        ],
        "full_pytest_run": False,
    }
    folder=Path('phase165_r9_output')
    folder.mkdir(exist_ok=True)
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (folder/'report.md').write_text('# Phase 165 R9 — 本番 Goal-only 接続\n\n'+ '\n'.join(f'- {k}: {v}' for k,v in report.items())+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
