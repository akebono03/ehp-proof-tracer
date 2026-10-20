"""Read-only inventory of the two Hopf image representations and consumers."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r14_r33_final_group import hopf_eta2_image_step
from proof import ProofRule

OUT = Path('phase166_r3q_hopf_single_source_audit_results')


def main() -> None:
    bridge = build_shared_typed_bridge()
    names = (
        'shared:1:adopted:assertion:5',
        'shared:2:toda:adopted:prop5.1:eta2_hopf_relation',
        'shared:2:toda:adopted:prop5.1:finite_dimensional:component:eta2_hopf_relation',
    )
    items = []
    for name in names:
        statement = bridge.registry.assertion(name)
        reference = bridge.registry.reference(statement.reference_id)
        links = [link for link in bridge.proof_links if link.assertion_id == name]
        items.append({
            'assertion_id': name,
            'reference_id': statement.reference_id,
            'locator': reference.locator,
            'reference_position': reference.publication_position,
            'component_position': statement.component_position,
            'kind': statement.kind.value,
            'content_type': type(statement.content).__name__,
            'content_repr': repr(statement.content),
            'given_links': sum(link.step is not None and link.step.rule is ProofRule.GIVEN for link in links),
        })
    source = bridge.registry.assertion(names[0]).content
    relation = bridge.registry.assertion(names[1]).content
    image = hopf_eta2_image_step().conclusion
    info = {
        'audit': 'phase166-r3q-hopf-single-source',
        'production_code_modified': False,
        'full_pytest_run': False,
        'registered_claims': items,
        'generator_image_matches_source_factory': source == image,
        'relation_type': type(relation).__name__,
        'relation_left_type': type(relation.lhs).__name__,
        'relation_map_repr': repr(getattr(relation.lhs, 'map', None)),
        'generator_image_map_repr': repr(image.map),
        'relation_input_matches_image': getattr(relation.lhs, 'expression', None) == image.source_generator,
        'relation_output_matches_image': relation.rhs == image.target_generator,
        'consumers': [
            'phase165_r14_r7_map_discovery.py:inverse_free_cyclic_transport_rule',
            'phase165_r14_r33_final_group.py:reverse_free_cyclic_transport_rule',
        ],
    }
    OUT.mkdir(exist_ok=True)
    destination = OUT / 'audit.json'
    destination.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        'audit': info['audit'],
        'registered_claims': len(items),
        'source_factory_equal': info['generator_image_matches_source_factory'],
        'input_equal': info['relation_input_matches_image'],
        'output_equal': info['relation_output_matches_image'],
        'report': str(destination.resolve()),
        'production_code_modified': False,
        'full_pytest_run': False,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
