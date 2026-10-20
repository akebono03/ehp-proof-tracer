"""R3-T read-only audit: map pi_5^4 specialized goal to typed source assertions."""
from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation, specialize_eta_group_relation,
)
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import Relation
from unified_statement_registry import AssertionOrigin


def relations_inside(value):
    if isinstance(value, Relation):
        yield value
        return
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            yield from relations_inside(getattr(value, field.name))
    elif isinstance(value, (tuple, list)):
        for item in value:
            yield from relations_inside(item)


def run():
    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=4, k=1)
    bases = registered_group_goal_candidates(bridge, n=3, k=1)
    target = targets[0] if len(targets) == 1 else None
    base = bases[0] if len(bases) == 1 else None
    all_sources = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        relations = tuple(relations_inside(assertion.content))
        exact_target = target is not None and any(r == target for r in relations)
        specialized_target = target is not None and any(
            _is_generic_eta_group_relation(r)
            and specialize_eta_group_relation(r, 4) == target for r in relations
        )
        exact_base = base is not None and any(r == base for r in relations)
        if not (exact_target or specialized_target or exact_base):
            continue
        ref = bridge.registry.reference(assertion.reference_id)
        all_sources.append({
            'assertion_id': assertion.assertion_id,
            'reference_id': assertion.reference_id,
            'locator': ref.locator,
            'publication_position': getattr(ref, 'publication_position', None),
            'component_position': getattr(assertion, 'component_position', None),
            'exact_target': exact_target,
            'specialized_target': specialized_target,
            'exact_base': exact_base,
        })
    target_sources = [s for s in all_sources if s['exact_target'] or s['specialized_target']]
    screening = []
    if target is not None:
        for source in target_sources:
            try:
                selected = screen_shared_proof_context(
                    bridge, goal=target, citing_assertion_id=source['assertion_id'],
                    explicit_publication_target=True,
                )
                matched = [link.assertion_id for link in selected.proof_links
                           if link.step is not None and base is not None
                           and link.step.conclusion == base]
                screening.append({'citing_assertion_id': source['assertion_id'],
                                  'base_given_ids': matched,
                                  'accepted_count': len(selected.proof_links)})
            except Exception as exc:
                screening.append({'citing_assertion_id': source['assertion_id'],
                                  'error': type(exc).__name__ + ': ' + str(exc)})
    report = {
        'audit': 'phase166-r3t-specialized-goal-provenance',
        'production_modified': False,
        'pi54_candidates': len(targets),
        'pi43_candidates': len(bases),
        'source_assertions': all_sources,
        'screening_by_source': screening,
        'warning': 'Specialized target source is not automatically a valid citing assertion. Review statement/component ordering before any code modification.',
        'full_pytest_run': False,
    }
    dest = Path(__file__).with_name('audit_result.json')
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    print('REPORT:', dest)


if __name__ == '__main__':
    run()
