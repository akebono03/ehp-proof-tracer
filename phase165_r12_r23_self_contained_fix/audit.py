"""Read-only public Narrative audit, saving exactly the renderer output."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r12_r23_public_narrative import build_verified_pi43_narrative


def perform_audit() -> dict:
    report = {
        'phase': '165 R12-R23', 'r22_proof_reverified': False,
        'root_ancestry_preserved': False, 'shared_renderer_called': False,
        'narrative_nonempty': False, 'reference_locators': [],
        'proof_node_count': 0, 'pi43_public_narrative_certified': False,
        'status': 'UNRESOLVED', 'full_pytest_run': False,
    }
    try:
        result = build_verified_pi43_narrative()
        path = Path(__file__).with_name('public_narrative.md')
        path.write_text(result.markdown, encoding='utf-8')
        report.update(
            r22_proof_reverified=True, root_ancestry_preserved=True,
            shared_renderer_called=True, narrative_nonempty=bool(result.markdown.strip()),
            reference_locators=list(result.sources), proof_node_count=result.node_count,
            narrative_path=str(path),
        )
        report['pi43_public_narrative_certified'] = bool(result.markdown.strip()) and bool(result.sources)
        report['status'] = 'PUBLIC_NARRATIVE_GENERATED_REVIEW_PENDING' if result.markdown.strip() else 'EMPTY_RENDER'
        # Human review of citation placement, prose and exactness order is still needed.
    except Exception as exc:
        report['blocker'] = type(exc).__name__ + ': ' + str(exc)
    return report


def main() -> None:
    report = perform_audit()
    path = Path(__file__).with_name('audit_result.json')
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['shared_renderer_called']:
        raise SystemExit('Public Narrative has not been generated; see blocker')


if __name__ == '__main__':
    main()
