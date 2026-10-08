"""Diagnostic for Phase 162 R3-A bridge-goal mismatch. No proof is modified."""

import json
from dataclasses import fields, is_dataclass
from pathlib import Path

from audit_phase162_r3a_presentation import build_r2_fixture
from expression import Composition
from homotopy_groups import TodaSuspensionMap
from phase162_group_structure_backward import expand_group_structure_goal
from proof import ProofRule, ProofStep, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule
from toda_rules import toda_eta_family_definition_statement, toda_prop53_n3_eta_square_suspension_bridge_inference_rule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data


def _structure(value):
    if is_dataclass(value):
        return {"type":type(value).__name__, "fields":{f.name:_structure(getattr(value,f.name)) for f in fields(value)}}
    if isinstance(value, tuple):
        return [_structure(x) for x in value]
    if isinstance(value, (str,int,float,bool)) or value is None:
        return value
    if hasattr(value, 'value') and hasattr(value, 'name'):
        return {"enum":type(value).__name__,"name":value.name}
    return {"type":type(value).__name__, "repr":repr(value)}


def diagnose_bridge():
    source_data=build_phase59_2_data()
    ehp_data=build_phase59_3_data()
    source_step=source_data['result_steps'][0]
    eta3=toda_eta_family_definition_statement(3)
    eta4=toda_eta_family_definition_statement(4)
    eta_steps=(ProofStep(conclusion=eta3,premises=(),rule=ProofRule.GIVEN), ProofStep(conclusion=eta4,premises=(),rule=ProofRule.GIVEN))
    suspension_map=TodaSuspensionMap(source_group=source_step.conclusion.lhs,target_group=ehp_data['expected_suspension_isomorphism'].map.target_group)
    goal=Relation(lhs=suspension_map.target_group,rhs=type(source_step.conclusion.rhs)(order=2,generator=Composition(left=eta3.element,right=eta4.element)),relation_type=RelationType.EQUALITY)
    plan=expand_group_structure_goal(goal,suspension_map,source_step.conclusion.rhs.generator)
    rule=toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    matches=tuple(m for m in find_inference_matches_for_rule(rule,eta_steps) if len(m.premises)==len(eta_steps) and all(a is b for a,b in zip(m.premises,eta_steps)))
    report={'matching_bridge_rules':len(matches),'target_group':_structure(goal),'source_generator':_structure(source_step.conclusion.rhs.generator),'planned_bridge':_structure(plan.generator_image_goal),'eta_definitions':[_structure(x.conclusion) for x in eta_steps]}
    if len(matches)==1:
        actual=apply_inference_match(matches[0]).conclusion
        expected=plan.generator_image_goal
        report.update({'actual_bridge':_structure(actual),'bridge_equal':actual==expected,'lhs_equal':getattr(actual,'lhs',None)==getattr(expected,'lhs',None),'rhs_equal':getattr(actual,'rhs',None)==getattr(expected,'rhs',None),'lhs_actual_type':type(getattr(actual,'lhs',None)).__name__,'lhs_expected_type':type(getattr(expected,'lhs',None)).__name__})
    output=Path('phase162_r3a_bridge_diagnostic.json')
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2,default=str))
    print('Diagnostic:',output.resolve())
    return report


if __name__=='__main__':
    diagnose_bridge()
