from dataclasses import replace
import re

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension, MapApplication, Suspension
from map_facts import EHP_DELTA_MAP
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, NarrativeCitation, root_ancestor_step_indices
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r3_unsigned_delta_composition_isolated.rule import RULE_NAME, unsigned_prop25_rule
from phase177_r4_general_iterated_suspension_audit.audit import image
from phase177_r5_general_suspension_equality_isolated.rule import expand_iterated_notation_equality, expand_suspension_image_equality
from phase177_r17r4r1_prop25_suspension_elision.projection import project_prop25_suspension_elision
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation, apply_inference_match, find_inference_matches_for_rule
from relation_rules import equality_preserved_under_left_composition_inference_rule, equality_transitivity_inference_rule, suspension_preserves_equality_inference_rule
from web_group_proof_common import _group_proof_statement_latex


def proved(rule, parents, goal):
    matches = [step for match in find_inference_matches_for_rule(rule, parents)
               for step in (apply_inference_match(match),)
               if step.conclusion == goal and step.premises == parents]
    result, = matches
    return result


def fixture(m):
    # Generic consecutive stable representatives; no target-specific formatter.
    i = 2*m+1
    from phase177_r4_general_iterated_suspension_audit.audit import family_member
    from phase169_r10b_registered_stable_family_binding.family_registry import registered_family_of
    # family_member supplies the repository's canonical names and symbols.
    from phase177_r4_general_iterated_suspension_audit.audit import cases
    family = registered_family_of(cases()['eta'][0])
    beta,y,z = (family_member(family,k) for k in (i-1,i,i+1))
    alpha = HomotopyElement('a',2*m+1,i+1,2*m+1)
    x = HomotopyElement('x',m,i-1,m)
    base_value = Relation(MapApplication(EHP_DELTA_MAP,alpha),x)
    reference = LiteratureReference(label='Toda Proposition 2.5',locator='Proposition 2.5')
    cite = ProofStep(CitedTodaProp25(),(),ProofRule.GIVEN)
    base = ProofStep(base_value,(),ProofRule.INFERENCE,inference_rule=InferenceRule('test-only base'))
    first, second = image(beta,y), image(y,z)
    first_step = proved(expand_defined_stable_element_image(first)[0].rule,(),first)
    second_step = proved(expand_defined_stable_element_image(second)[0].rule,(),second)
    r1,r2 = Relation(Suspension(beta),y),Relation(Suspension(y),z)
    e1 = proved(expand_suspension_image_equality(r1)[0].rule,(first_step,),r1)
    e2 = proved(expand_suspension_image_equality(r2)[0].rule,(second_step,),r2)
    nested = Suspension(Suspension(beta))
    lifted = Relation(nested,Suspension(y))
    lift = proved(suspension_preserves_equality_inference_rule(),(e1,),lifted)
    nested_eq = Relation(nested,z)
    trans = proved(equality_transitivity_inference_rule(),(lift,e2),nested_eq)
    notation = Relation(IteratedSuspension(beta,2),nested)
    note = proved(expand_iterated_notation_equality(notation)[0].rule,(),notation)
    double = Relation(notation.lhs,z)
    double_step = proved(equality_transitivity_inference_rule(),(note,trans),double)
    identity = Relation(Composition(alpha,double.lhs),Composition(alpha,z))
    comp = proved(equality_preserved_under_left_composition_inference_rule(alpha),(double_step,),identity)
    goal = Relation(MapApplication(EHP_DELTA_MAP,identity.rhs),Composition(x,beta))
    prop = proved(unsigned_prop25_rule(goal,base_value,identity),(cite,base,comp),goal)
    steps = (cite,base,first_step,e1,lift,second_step,e2,trans,note,double_step,comp,prop)
    model = ProofNarrativeModel(steps,(NarrativeCitation(1,reference,(0,11)),),
                                ((1,),)+ ((),)*10 + ((1,),),11,ProofSearchStatus.COMPLETE)
    return model


@pytest.mark.parametrize('m',[3,4,5])
def test_generic_elision(m):
    model = fixture(m)
    order = tuple(range(len(model.steps)))
    hidden = project_prop25_suspension_elision(model,order)
    assert hidden == frozenset(range(2,11))
    assert not project_prop25_suspension_elision(replace(model,status=ProofSearchStatus.PARTIAL),order)
    assert not project_prop25_suspension_elision(model,order,protected={9})
    assert not project_prop25_suspension_elision(model,order,suppressed={1})
    numbers = list(model.step_citation_numbers)
    numbers[9] = (1,)
    assert not project_prop25_suspension_elision(replace(model,step_citation_numbers=tuple(numbers)),order)
    # A branch witness is consumed by a different step: preserve all of it.
    extra = ProofStep(model.steps[9].conclusion,(model.steps[-1],model.steps[9]),ProofRule.INFERENCE)
    shared = replace(model,steps=model.steps+(extra,),step_citation_numbers=model.step_citation_numbers+((),),root_index=len(model.steps))
    assert not project_prop25_suspension_elision(shared,order+(len(model.steps),))


def key(value):
    return re.sub(r'\s+','',value.replace(r'\left','').replace(r'\right','').replace(r'\circ',''))


def test_actual_elision():
    invocation,result,calls,model,view = capture()
    assert result.status.value == 'complete' and not result.open_goals
    assert view.key == 'generic-complete-proof'
    assert len(result.proven_steps) == len(model.steps) == 43 and len(model.citations) == 8
    scope = root_ancestor_step_indices(model.steps,model.root_index)
    order = tuple(e.step_index for e in project_narrative_order(model) if e.step_index in scope)
    hidden = project_prop25_suspension_elision(model,order)
    assert hidden, [(i,s.inference_rule.name if s.inference_rule else None,repr(s.conclusion)) for i,s in enumerate(model.steps)]
    prop, = [s for s in model.steps if s.inference_rule is not None and s.inference_rule.name == RULE_NAME]
    assert len(prop.premises) == 3 and any(model.steps[i] is prop.premises[2] for i in hidden)
    markdown = render_model_backed_narrative_markdown(result,model)
    body = markdown.split('\n証明\n',1)[1]
    terms = {key(s) for s in re.findall(r'\$([^$]+)\$',body)}
    unwanted = (r'EE\eta_{8}=E^{2}\eta_{8}',r'E(\eta_{8})=\eta_{9}',r'E\eta_{8}=\eta_{9}',
                r'E\eta_{9}=EE\eta_{8}',r'E(\eta_{9})=\eta_{10}',r'E\eta_{9}=\eta_{10}',
                r'EE\eta_{8}=\eta_{10}',r'E^{2}\eta_{8}=\eta_{10}',r'\eta_{9}^{2}=\eta_{9}E^{2}\eta_{8}')
    assert not ({key(s) for s in unwanted} & terms), body
    # R17R4R2 may replace the Prop 2.5 intermediate with its certified
    # transitivity conclusion. The base equality must still be printed.
    from phase177_r17r4r2_prop25_equality_chain.projection import project_prop25_equality_chain
    compressed, sentences = project_prop25_equality_chain(model,order,hidden)
    prop_index, = [i for i,s in enumerate(model.steps) if s is prop]
    visible = (prop,prop.premises[1])
    if prop_index in compressed:
        final_index, = sentences
        visible = (model.steps[final_index],prop.premises[1])
    for step in visible:
        latex,fallback = _group_proof_statement_latex(step.conclusion)
        assert latex is not None and fallback is None and key(latex) in terms, (latex,body)
    assert '準同型定理より' in body
    assert all(model.steps[i] in result.proven_steps for i in hidden)
    print('PHASE177_R17R4R1_HIDDEN_PROOF_INDICES='+str(sorted(hidden)))
    print('PHASE177_R17R4R1_ROOT_STEPS=43')
    print('PHASE177_R17R4R1_REFERENCE_COUNT=8')
    print('PHASE177_R17R4R1_SUSPENSION_ELISION=VERIFIED')
