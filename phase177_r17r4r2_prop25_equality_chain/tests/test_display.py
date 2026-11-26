from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r3_unsigned_delta_composition_isolated.rule import RULE_NAME, unsigned_prop25_rule
from phase177_r10_composition_associativity_isolated.rule import expand_composition_associativity_equality
from phase177_r17r4r1_prop25_suspension_elision.projection import project_prop25_suspension_elision
from phase177_r17r4r1_prop25_suspension_elision.tests.test_display import fixture, proved, key
from phase177_r17r4r2_prop25_equality_chain.projection import project_prop25_equality_chain
from proof import ProofRule, ProofStep, Relation
from relation_rules import equality_symmetry_inference_rule, equality_transitivity_inference_rule
from web_group_proof_common import _group_proof_statement_latex


def chain_fixture(m, reverse=False):
    model = fixture(m)
    old = model.steps[-1]
    cite, base, identity = old.premises
    beta = old.conclusion.rhs.right
    x = HomotopyElement('u', m, m+1, m)
    y = HomotopyElement('v', m+1, 2*m, m+1)
    base_value = Relation(base.conclusion.lhs, Composition(x,y))
    base = replace(base, conclusion=base_value)
    prop_value = Relation(old.conclusion.lhs, Composition(base_value.rhs,beta))
    prop = proved(unsigned_prop25_rule(prop_value,base_value,identity.conclusion),
                  (cite,base,identity),prop_value)
    final_rhs = Composition(x,Composition(y,beta))
    bridge = Relation(prop_value.rhs,final_rhs)
    if reverse:
        backward = Relation(bridge.rhs,bridge.lhs)
        option, = expand_composition_associativity_equality(backward)
        witness = proved(option.rule,(),backward)
        assoc = proved(equality_symmetry_inference_rule(),(witness,),bridge)
        branch = (witness,assoc)
    else:
        option, = expand_composition_associativity_equality(bridge)
        assoc = proved(option.rule,(),bridge)
        branch = (assoc,)
    final = proved(equality_transitivity_inference_rule(),(prop,assoc),
                   Relation(prop_value.lhs,final_rhs))
    steps = (cite,base)+model.steps[2:-1]+(prop,)+branch+(final,)
    return replace(model,steps=steps,step_citation_numbers=model.step_citation_numbers+((),)*(len(branch)+1),
                   root_index=len(steps)-1)


@pytest.mark.parametrize('m',[3,4,5])
@pytest.mark.parametrize('reverse',[False,True])
def test_generic_chain(m,reverse):
    model = chain_fixture(m,reverse)
    order = tuple(range(len(model.steps)))
    prior = project_prop25_suspension_elision(model,order)
    assert prior == frozenset(range(2,11))
    p = 11
    a,i = order[-2:]
    intermediates = set(range(p,i))
    hidden,sentences = project_prop25_equality_chain(model,order,prior)
    latex,fallback = _group_proof_statement_latex(model.steps[i].conclusion)
    assert fallback is None and latex
    assert hidden == frozenset(intermediates)
    assert sentences == {i:f'[R1]を用いて, ${latex}$.'}
    for changed,suppressed,protected in (
        (replace(model,status=ProofSearchStatus.PARTIAL),prior,set()),
        (model,prior,{p}), (model,prior,{a}), (model,prior,{i}),
        (model,prior|{1},set()), (model,prior-{10},set()),
        (model,prior|{p},set()),
    ):
        assert project_prop25_equality_chain(changed,order,suppressed,protected) == (frozenset(),{})
    for j in intermediates - {p} | {i}:
        numbers = list(model.step_citation_numbers)
        numbers[j] = (1,)
        changed = replace(model,step_citation_numbers=tuple(numbers))
        assert project_prop25_equality_chain(changed,order,prior) == (frozenset(),{})
    for j in intermediates:
        extra = ProofStep(model.steps[i].conclusion,(model.steps[i],model.steps[j]),ProofRule.INFERENCE)
        shared = replace(model,steps=model.steps+(extra,),step_citation_numbers=model.step_citation_numbers+((),),root_index=len(order))
        assert project_prop25_equality_chain(shared,order+(len(order),),prior) == (frozenset(),{})
    for j in intermediates:
        assert project_prop25_equality_chain(model,order,prior,{j}) == (frozenset(),{})
    # The earlier general projection can hide a valid symmetry line.
    if reverse:
        assert project_prop25_equality_chain(model,order,prior|{a}) == (hidden,sentences)
        wrong_assoc = replace(model.steps[a],conclusion=model.steps[a-1].conclusion)
        wrong_final = replace(model.steps[i],premises=(model.steps[p],wrong_assoc))
        invalid = replace(model,steps=model.steps[:a]+(wrong_assoc,wrong_final))
        assert project_prop25_equality_chain(invalid,order,prior) == (frozenset(),{})
    bad = replace(model.steps[i],premises=tuple(reversed(model.steps[i].premises)))
    changed = replace(model,steps=model.steps[:-1]+(bad,))
    assert project_prop25_equality_chain(changed,order,prior) == (frozenset(),{})


def test_actual_chain_display():
    invocation,result,calls,model,view = capture()
    assert result.status.value == 'complete' and not result.open_goals
    assert view.key == 'generic-complete-proof'
    assert len(result.proven_steps) == len(model.steps) == 43 and len(model.citations) == 8
    scope = root_ancestor_step_indices(model.steps,model.root_index)
    order = tuple(e.step_index for e in project_narrative_order(model) if e.step_index in scope)
    prior = project_prop25_suspension_elision(model,order)
    hidden,sentences = project_prop25_equality_chain(model,order,prior)
    assert len(hidden) == 3 and len(sentences) == 1, [(i,s.inference_rule.name if s.inference_rule else None,repr(s.conclusion),model.step_citation_numbers[i]) for i,s in enumerate(model.steps)]
    i, = sentences
    final = model.steps[i]
    prop,assoc = final.premises
    assert prop.inference_rule.name == RULE_NAME
    assert assoc.inference_rule.name == 'equality symmetry'
    witness, = assoc.premises
    assert witness.inference_rule.name == 'typed composition associativity equality'
    assert {id(model.steps[j]) for j in hidden} == {id(prop),id(assoc),id(witness)}
    assert project_prop25_equality_chain(model,order,prior|{next(j for j in hidden if model.steps[j] is assoc)}) == (hidden,sentences)
    before = (model.steps,model.citations,model.step_citation_numbers)
    body = render_model_backed_narrative_markdown(result,model).split('\n証明\n',1)[1]
    assert body.count(sentences[i]) == 1, body
    import re
    terms = {key(s) for s in re.findall(r'\$([^$]+)\$',body)}
    for s in (prop,assoc,witness):
        latex,fallback = _group_proof_statement_latex(s.conclusion)
        assert latex and fallback is None and key(latex) not in terms, (latex,body)
    for s in (final,prop.premises[1]):
        latex,fallback = _group_proof_statement_latex(s.conclusion)
        assert latex and fallback is None and key(latex) in terms, (latex,body)
    assert before == (model.steps,model.citations,model.step_citation_numbers)
    assert all(model.steps[j] in result.proven_steps for j in hidden)
    print('PHASE177_R17R4R2_HIDDEN_PROOF_INDICES='+str(sorted(hidden)))
    print('PHASE177_R17R4R2_FINAL_SENTENCE='+sentences[i])
    print('PHASE177_R17R4R2_ROOT_STEPS=43')
    print('PHASE177_R17R4R2_REFERENCE_COUNT=8')
