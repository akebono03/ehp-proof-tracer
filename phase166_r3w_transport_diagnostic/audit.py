"""Phase 166 R3-W: read-only diagnosis of the actual screened pi_5^4 transport path."""
from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r57_r7_stable_expansion import expand_registered_toda45_finite_cyclic_goal
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase166_r3v_generator_transport import expand_generator_transport_normalization
from proof import ProofRule, Relation, RelationType
from toda_rules import Toda45IsomorphismStatement, toda_eta_family_definition_statement

TARGET_ID = 'shared:2:toda:adopted:prop5.1:higher_eta_group_relation'


def describe(obj):
    return repr(obj)


def inspect():
    eta4 = toda_eta_family_definition_statement(4).element
    goal = Relation(TodaPrimaryGroup(5, 4), FiniteCyclicGroup(2, eta4), RelationType.EQUALITY)
    bridge = build_shared_typed_bridge()
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=TARGET_ID,
        explicit_publication_target=True,
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    root_options = shared_expansion_provider(screened, proof_target=goal)(goal)
    normalizations = expand_generator_transport_normalization(goal)
    transported = normalizations[0].subgoals[0] if normalizations else None
    transport_options = (
        shared_expansion_provider(screened, proof_target=goal)(transported)
        if transported is not None else ()
    )
    bases = tuple(x for x in available if isinstance(x, Relation)
                  and isinstance(x.lhs, TodaPrimaryGroup)
                  and x.lhs == TodaPrimaryGroup(4, 3)
                  and isinstance(x.rhs, FiniteCyclicGroup))
    general_isos = tuple(x for x in available if isinstance(x, Toda45IsomorphismStatement))
    expected_iso = Toda45IsomorphismStatement(
        TodaIteratedSuspensionMap(1, TodaPrimaryGroup(4, 3), TodaPrimaryGroup(5, 4))
    )
    source_eta = toda_eta_family_definition_statement(3).element
    base_details = []
    for base in bases:
        expected_generator = IteratedSuspension(base.rhs.generator, 1)
        base_details.append({
            'base': describe(base),
            'base_generator_equal_eta3_definition': base.rhs.generator == source_eta,
            'base_generator_repr': describe(base.rhs.generator),
            'eta3_definition_repr': describe(source_eta),
            'iterated_from_base_matches_transport_goal': (
                transported is not None and expected_generator == transported.rhs.generator
            ),
            'iterated_from_base': describe(expected_generator),
        })
    iso_details = [{
        'statement': describe(iso),
        'exact_match': iso == expected_iso,
        'specialization_bindings': describe(specialize_typed_statement(iso, expected_iso)),
    } for iso in general_isos]
    direct_options = expand_registered_toda45_finite_cyclic_goal(transported, available) if transported else ()
    return {
        'phase': '166 R3-W', 'production_code_modified': False, 'full_pytest_run': False,
        'target_id': TARGET_ID,
        'screened_given_count': len(available),
        'base_pi43_count': len(bases),
        'bases': base_details,
        'toda45_screened_count': len(general_isos),
        'toda45_sources': iso_details,
        'named_goal': describe(goal),
        'normalization_option_count': len(normalizations),
        'transported_goal': describe(transported),
        'direct_transport_option_count': len(direct_options),
        'direct_transport_subgoals': [[describe(x) for x in option.subgoals] for option in direct_options],
        'common_root_rule_names': [x.rule.name for x in root_options],
        'common_transport_rule_names': [x.rule.name for x in transport_options],
        'common_transport_has_toda45': any('transport' in x.rule.name.lower() and len(x.subgoals) == 2 for x in transport_options),
        'root_has_normalization': any(x.subgoals == normalizations[0].subgoals for x in root_options) if normalizations else False,
    }


def main():
    report = inspect()
    output = Path(__file__).with_name('report.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('REPORT:', output)


if __name__ == '__main__':
    main()
