from __future__ import annotations

import json
from pathlib import Path

from phase165_r8_rule_provider import build_production_rule_provider
from phase165_r7_bulk_integration import build_bulk_integration
from standard_production_repository import build_standard_production_proof_repository


def main():
    provider, report = build_production_rule_provider()
    result = build_bulk_integration(proof_repository=build_standard_production_proof_repository())
    payload = {
        "phase": "165 R8",
        "mode": "GENERIC_INVERTIBLE_RULE_CATALOG_NO_SOURCE_PROMOTION",
        "source_assertions_scanned": result.source_count,
        "repository_roots_indexed": len(result.repository_roots),
        "factory_rules_discovered": len(report.rule_names),
        "noninvertible_without_pattern": len(report.skipped_rules),
        "skipped_factories": list(report.skipped_factories),
        "rules": list(report.rule_names),
        "rule_expansion_provider_constructed": callable(provider),
        "source_assertions_newly_eligible": 0,
        "goal_only_proof_completed": False,
        "remaining_blockers": [
            "SEMANTIC_BINDINGS_NOT_INDEPENDENTLY_VERIFIED",
            "NO_APPROVED_CITATION_AVAILABILITY",
            "PRODUCTION_GOAL_ENTRY_NOT_YET_WIRED_TO_PROVIDER",
            "NON_PATTERN_RULES_NOT_INVERTIBLE",
        ],
        "full_pytest_run": False,
    }
    out = Path('phase165_r8_output')
    out.mkdir(exist_ok=True)
    (out / 'report.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out / 'report.md').write_text('# Phase 165 R8 — 共通推論規則の収集\n\n' + '\n'.join(f'- {k}: {v}' for k,v in payload.items()) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
