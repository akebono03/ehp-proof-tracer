from __future__ import annotations

import json
from pathlib import Path

from phase165_r7_bulk_integration import build_bulk_integration


def main():
    # The existing production proof repository is obtained through its public
    # factory. The audit does not turn its internal roots into citations.
    repository_error = None
    repository = None
    try:
        from standard_production_repository import build_standard_production_proof_repository
        repository = build_standard_production_proof_repository()
    except Exception as exc:
        repository_error = f'{type(exc).__name__}: {exc}'
    result = build_bulk_integration(proof_repository=repository)
    payload = {
        'phase': '165 R7',
        'mode': 'BULK_SOURCE_AND_PROOF_ASSET_INDEX_NON_PROMOTING',
        'source_assertions_scanned': result.source_count,
        'unique_locator_candidates': len(result.candidate_pairs),
        'ambiguous_source_assertions': len(result.ambiguous_ids),
        'unmatched_source_assertions': len(result.unmatched_ids),
        'repository_root_count': len(result.repository_roots),
        'repository_root_ids': result.repository_roots,
        'repository_root_conclusion_types': result.repository_root_conclusion_types,
        'repository_factory_error': repository_error,
        'verified_source_assertions': len(result.verified_source_ids),
        'proof_eligible_source_assertions': len(result.eligible_source_ids),
        'rule_expansion_provider_connected': result.rule_expansion_provider_connected,
        'goal_only_proof_completed': False,
        'remaining_blockers': [
            'SEMANTIC_BINDINGS_NOT_INDEPENDENTLY_VERIFIED',
            'NO_APPROVED_CITATION_AVAILABILITY',
            'NO_GLOBAL_GOAL_EXPANSION_PROVIDER',
        ],
        'full_pytest_run': False,
    }
    out = Path('phase165_r7_output')
    out.mkdir(exist_ok=True)
    (out / 'report.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out / 'report.md').write_text(
        '# Phase 165 R7 — 全件一括照合\n\n'
        + '\n'.join(f'- {key}: {value}' for key, value in payload.items()) + '\n', encoding='utf-8'
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
