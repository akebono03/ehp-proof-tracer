"""Read-only diagnosis of R3-Q pi3^2 publication-order proof context."""
from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import ProofRule, Relation
from unified_statement_registry import AssertionOrigin


def contains_relation(value: object, target: Relation, seen: set[int] | None = None) -> bool:
    """Check a registered compound assertion without claiming proof availability."""
    if value == target and type(value) is type(target):
        return True
    if seen is None:
        seen = set()
    if id(value) in seen:
        return False
    seen.add(id(value))
    if is_dataclass(value) and not isinstance(value, type):
        return any(contains_relation(getattr(value, field.name), target, seen) for field in fields(value))
    if isinstance(value, (tuple, list)):
        return any(contains_relation(item, target, seen) for item in value)
    return False


def main() -> None:
    root = Path.cwd()
    if not (root / 'phase165_r55_nk_only_goal.py').is_file():
        raise SystemExit('Run from repository root.')
    bridge = build_shared_typed_bridge()
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    candidates = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if contains_relation(assertion.content, goal):
            reference = bridge.registry.reference(assertion.reference_id)
            candidates.append({
                'assertion_id': assertion.assertion_id,
                'reference_id': reference.reference_id,
                'locator': reference.locator,
                'publication_position': reference.publication_position,
                'component_position': assertion.component_position,
                'direct_content_match': type(assertion.content) is type(goal) and assertion.content == goal,
            })
    link_ids = {link.assertion_id for link in bridge.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN}
    ordered = []
    for entry in candidates:
        citing_id = entry['assertion_id']
        implicit = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=False,
        )
        explicit = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
        implicit_ids = {x.assertion_id for x in implicit.proof_links}
        explicit_ids = {x.assertion_id for x in explicit.proof_links}
        filtered = sorted(implicit_ids - explicit_ids)
        ordered.append({
            **entry,
            'implicit_given_count': len(implicit_ids),
            'ordered_given_count': len(explicit_ids),
            'excluded_previously_usable': [
                {
                    'assertion_id': aid,
                    'publication_position': bridge.registry.reference(bridge.registry.assertion(aid).reference_id).publication_position,
                    'component_position': bridge.registry.assertion(aid).component_position,
                    'was_linked': aid in link_ids,
                    'precedes': precedes_citing_assertion(bridge, aid, citing_id),
                }
                for aid in filtered
            ],
        })
    outcome = search_group_from_registered_goal(n=2, k=1, bridge=bridge)
    report = {
        'audit': 'phase166-r3q-reference-audit',
        'production_code_modified': False,
        'pi32_status': outcome.status.value,
        'pi32_diagnostics': list(outcome.diagnostics),
        'goal_matching_registered_assertions': ordered,
        'component_children_missing_position': sum(
            1 for a in bridge.registry._assertions.values()
            if ':component:' in a.assertion_id and a.component_position is None
        ),
        'full_pytest_run': False,
    }
    output = root / 'phase166_r3q_reference_audit_results'
    output.mkdir(exist_ok=True)
    result_path = output / 'audit.json'
    result_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=repr), encoding='utf-8')
    print(json.dumps({
        'audit': report['audit'],
        'production_code_modified': False,
        'pi32_status': report['pi32_status'],
        'matching_assertions': len(ordered),
        'unpositioned_component_children': report['component_children_missing_position'],
        'report': str(result_path),
        'full_pytest_run': False,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
