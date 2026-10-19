from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from expression import GeneratorSymbol, HomotopyElement
from proof import ProofRule, ProofStep, Relation, RelationType, run_inference_until_stable_with_history
from toda_rules import toda_53_eta3_twice_zero_inference_rule
from phase165_r55_nk_only_goal import search_group_from_registered_goal


def test_eta3_rule_accepts_both_verified_name_spellings():
    expected=search_group_from_registered_goal(n=3,k=1)
    assert expected.conclusion.rhs.generator.generator == GeneratorSymbol(family="η",index=3)
    rule=toda_53_eta3_twice_zero_inference_rule()
    for name in ("η_3","η₃"):
        gen=HomotopyElement(name=name,dimension=3,source=4,target=3,
                           generator=GeneratorSymbol(family="η",index=3))
        stmt=Relation(lhs=TodaPrimaryGroup(4,3),
                      rhs=FiniteCyclicGroup(order=2,generator=gen),
                      relation_type=RelationType.EQUALITY)
        current_step=next(s for s in expected.proven_steps if s.conclusion==expected.conclusion and s.rule is ProofRule.INFERENCE)
        from dataclasses import replace
        premise=replace(current_step,conclusion=stmt)
        result=run_inference_until_stable_with_history(rule,(premise,))
        assert len(result.steps)>1


def test_phase58_uses_current_pi43_proof():
    from probes.probe_phase58_capabilities import build_phase58_representative_result
    current=search_group_from_registered_goal(n=3,k=1)
    value=build_phase58_representative_result()
    assert value["pi4_3_step"].conclusion==current.conclusion
    assert value["pi4_3_step"].rule is ProofRule.INFERENCE
    assert value["final_hopf_step"].rule is ProofRule.INFERENCE
