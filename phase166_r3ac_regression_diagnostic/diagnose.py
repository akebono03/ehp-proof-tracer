from __future__ import annotations
import json
from pathlib import Path
from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r57_r11_proof_order_gate import is_unordered_root_structure_specialization
from phase166_r3v_generator_transport import expand_generator_transport_normalization
from phase166_r3ac_stable_notation import expand_stable_eta_notation
from proof import Relation
from toda_rules import toda_eta_family_definition_statement


def main():
    base = toda_eta_family_definition_statement(3).element
    target = toda_eta_family_definition_statement(4).element
    source_group = TodaPrimaryGroup(4, 3)
    target_group = TodaPrimaryGroup(5, 4)
    transported = Relation(target_group, FiniteCyclicGroup(2, IteratedSuspension(base, 1)))
    named = Relation(target_group, FiniteCyclicGroup(2, target))
    witness = GeneratorSuspension(TodaSuspensionMap(source_group, target_group), base, target)
    bridge = build_shared_typed_bridge()
    target_id = 'shared:2:toda:adopted:prop5.1:higher_eta_group_relation'
    context = screen_shared_proof_context(bridge, goal=named, citing_assertion_id=target_id, explicit_publication_target=True)
    available = tuple(x.step.conclusion for x in context.proof_links if x.step is not None)
    old = expand_generator_transport_normalization(named, available)
    new = expand_stable_eta_notation(named, available)
    final = shared_expansion_provider(context, proof_target=named)(named)
    expected = (transported, witness)
    report = {
        'phase': '166 R3-AC regression diagnostic',
        'production_modified': False,
        'expected_old_subgoals': [repr(x) for x in expected],
        'earlier_pi43': [repr(x) for x in available if isinstance(x, Relation) and x.lhs == source_group],
        'old_candidates': [{'rule':x.rule.name,'subgoals':[repr(s) for s in x.subgoals], 'matches_expected':x.subgoals == expected,'root_gate_rejects':is_unordered_root_structure_specialization(named,named,x)} for x in old],
        'new_candidates': [{'rule':x.rule.name,'subgoals':[repr(s) for s in x.subgoals]} for x in new],
        'final_candidates': [{'rule':x.rule.name,'subgoals':[repr(s) for s in x.subgoals],'matches_expected':x.subgoals==expected} for x in final],
        'old_expected_generated':any(x.subgoals == expected for x in old),
        'old_expected_survives':any(x.subgoals == expected for x in final),
    }
    output=Path(__file__).with_name('report.json')
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('old_expected_generated','old_expected_survives','old_candidates','new_candidates')},ensure_ascii=False,indent=2))
    print('REPORT:',output)

if __name__ == '__main__':
    main()
