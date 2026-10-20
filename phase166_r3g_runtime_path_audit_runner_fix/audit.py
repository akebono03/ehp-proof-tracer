"""Read-only runtime audit of Toda (4.5) specialization and transport reachability."""
from __future__ import annotations
import json
from pathlib import Path
from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r57_r20_general_specialization import expand_cited_general_specialization
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from proof import Relation, RelationType
from toda_rules import Toda45IsomorphismStatement


def run():
    bridge = build_shared_typed_bridge()
    general = tuple(a for a in bridge.registry._assertions.values()
                    if isinstance(a.content, Toda45IsomorphismStatement)
                    and not isinstance(a.content.map.source_group.sphere_dimension, int))
    base_group = TodaPrimaryGroup(4, 3)
    target_group = TodaPrimaryGroup(5, 4)
    iso = Toda45IsomorphismStatement(TodaIteratedSuspensionMap(
        exponent=1, source_group=base_group, target_group=target_group))
    eta3 = HomotopyElement(name='η₃', dimension=3, source=4, target=3,
                           generator=GeneratorSymbol(family='η', index=3))
    eta4 = HomotopyElement(name='η₄', dimension=4, source=5, target=4,
                           generator=GeneratorSymbol(family='η', index=4))
    base = Relation(base_group, FiniteCyclicGroup(2, eta3), RelationType.EQUALITY)
    suspended = Relation(target_group, FiniteCyclicGroup(2, IteratedSuspension(eta3, 1)), RelationType.EQUALITY)
    displayed = Relation(target_group, FiniteCyclicGroup(2, eta4), RelationType.EQUALITY)
    available = tuple(link.step.conclusion for link in bridge.proof_links if link.step is not None)
    general_values = tuple(a.content for a in general)
    specialized = expand_cited_general_specialization(iso, general_values)
    direct_transport = expand_registered_toda45_finite_cyclic_goal(suspended, available)
    with_base = expand_registered_toda45_finite_cyclic_goal(suspended, available + (base,))
    with_both = expand_registered_toda45_finite_cyclic_goal(suspended, available + (base, iso))
    displayed_with_both = expand_registered_toda45_finite_cyclic_goal(displayed, available + (base, iso))
    provider = shared_expansion_provider(bridge, proof_target=displayed)
    iso_options = provider(iso)
    target_options = provider(displayed)
    report = {
        'audit': 'phase166-r3g-runtime-path',
        'production_modified': False,
        'typed_general_toda45_count': len(general),
        'general_locators': [bridge.registry.reference(a.reference_id).locator for a in general],
        'general_given_available': any(x in available for x in general_values),
        'concrete_iso_given_available': iso in available,
        'concrete_base_group_given_available': base in available,
        'specialization_proposals_for_concrete_iso': len(specialized),
        'shared_provider_concrete_iso_proposals': [getattr(x.rule, 'name', repr(x.rule)) for x in iso_options],
        'transport_proposals_as_is': len(direct_transport),
        'transport_proposals_base_supplied': len(with_base),
        'transport_proposals_base_and_iso_supplied': len(with_both),
        'transport_proposals_named_eta4_base_and_iso_supplied': len(displayed_with_both),
        'shared_provider_named_eta4_proposals': [getattr(x.rule, 'name', repr(x.rule)) for x in target_options],
        'full_pytest_run': False,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    output = Path('phase166_r3g_runtime_path_audit_results.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('AUDIT SAVED:', output.resolve())


if __name__ == '__main__':
    run()
