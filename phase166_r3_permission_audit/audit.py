"""Phase 166 R3: read-only proof-permission and lookup-mode boundary audit."""
from __future__ import annotations

import ast
import json
from pathlib import Path

from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from phase165_r2_registry_lookup import find_eligible_goal_candidates
from phase165_r4_production_connection import discover_production_registry
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
TARGETS = (
    'boundary:Proposition 5.1:pi3_2_group_relation',
    'boundary:Proposition 5.1:higher_eta_group_relation',
    'boundary:Proposition 5.3:pi5_3_group_relation',
    'boundary:(5.3):nu_prime_double_relation',
)

def inspect_lookup_modes():
    source = (ROOT / 'phase165_r3_recursive_search.py').read_text(encoding='utf-8-sig')
    tree = ast.parse(source)
    function = next((node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'reconstruct_registered_goal'), None)
    if function is None:
        raise RuntimeError('canonical reconstruct_registered_goal missing')
    text = ast.get_source_segment(source, function) or ''
    return {
        'legacy_uses_eligibility_lookup': 'find_eligible_goal_candidates(' in text,
        'typed_reference_uses_direct_lookup': 'options = list(_typed_reference_steps(' in text,
        'ordered_mode_function_present': 'ordered_typed_reference_steps(' in text,
        'review_required_for_all_modes': False if 'options = list(_typed_reference_steps(' in text else None,
    }

def inspect():
    discovery = discover_production_registry()
    bridge = discovery.bridge
    available = tuple(bridge.registry._assertions.values())
    targets = []
    for assertion_id in TARGETS:
        assertion = bridge.registry.assertion(assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        migration = [record.status.value for record in bridge.records if record.assertion_id == assertion_id]
        target = {
            'assertion_id': assertion_id,
            'origin': assertion.origin.value,
            'content_type': type(assertion.content).__name__,
            'reference': reference.locator,
            'migration_statuses': migration,
            'proof_link_count': sum(link.assertion_id == assertion_id for link in bridge.proof_links),
            'grant_allowed': False,
        }
        targets.append(target)
    # A metadata-only item must be denied even if a caller supplies its ID as reviewed.
    cited = TARGETS[0]
    citing_candidates = [a.assertion_id for a in available if a.assertion_id != cited]
    if not citing_candidates:
        raise RuntimeError('no citing assertion for eligibility audit')
    citing = citing_candidates[0]
    decisions = {}
    for label, verified in (('no_review', ()), ('id_supplied_not_certification', (cited,))):
        decision = assess_phase164_r2_citation(bridge, cited, citing, verified_assertion_ids=verified)
        decisions[label] = {'status': decision.status.value, 'reason': decision.reason, 'usable': decision.usable}
        if decision.usable:
            raise RuntimeError('metadata-only entry unexpectedly eligible')
    eligibility_candidates = find_eligible_goal_candidates(bridge, bridge.registry.assertion(cited).content, citing)
    if any(item.assertion.assertion_id == cited for item in eligibility_candidates):
        raise RuntimeError('metadata-only assertion entered eligible lookup')
    modes = inspect_lookup_modes()
    result = {
        'phase': '166 R3 boundary audit',
        'read_only': True,
        'total_registry_assertions': len(available),
        'origin_counts': {origin.value:sum(x.origin is origin for x in available) for origin in AssertionOrigin},
        'target_records': targets,
        'citation_checks': decisions,
        'lookup_modes': modes,
        'proof_permission_granted': 0,
        'production_code_modified': False,
        'full_pytest_run': False,
        'status': 'AUDITED_WITH_LOOKUP_MODE_REVIEW_PENDING' if modes['typed_reference_uses_direct_lookup'] else 'AUDITED',
    }
    return result

def main():
    result = inspect()
    directory = Path(__file__).resolve().parent / 'results'
    directory.mkdir(exist_ok=True)
    (directory/'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print('R3 read-only boundary audit completed; full pytest NOT run.')

if __name__ == '__main__':
    main()
