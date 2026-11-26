from dataclasses import replace

import pytest

from expression import Composition
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import NarrativeCitation, ProofNarrativeModel
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition, expand_cited_stable_family,
)
from phase169_r10e5_composite_generator_image.rule import expand_composite_generator_image
from phase169_r10e5_composite_generator_image.tests.test_r10e5_composite_generator_image import _nu, _image
from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
from phase175_r4r3_two_summand_quotient.rule import RULE_NAME
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r17r3_rank_two_quotient_display.projection import project_rank_two_quotient_reason
from phase177_r17r4r1_prop25_suspension_elision.tests.test_display import proved
from phase177_r17r6r1_suspension_composition_display.projection import (
    match_composition_branch, project_suspension_composition_display,
)
from proof import LiteratureReference, ProofRule, ProofStep


def branch_fixture(n):
    source = CitedStableFamilyDefinition(4,4,3)
    leaf = ProofStep(source, (), ProofRule.GIVEN)
    goal = _image(n,6,Composition(_nu(n),_nu(n+3)),Composition(_nu(n+1),_nu(n+4)))
    composite, = expand_composite_generator_image(goal)
    first,second = composite.subgoals
    first_option, = expand_cited_stable_family(first,(source,))
    members = []
    for g in first_option.subgoals:
        option, = expand_cited_stable_family(g,(source,))
        members.append(proved(option.rule,(leaf,),g))
    left = proved(first_option.rule,tuple(members),first)
    option, = expand_defined_stable_element_image(second)
    right = proved(option.rule,(),second)
    image = proved(composite.rule,(left,right),goal)
    steps = (leaf,*members,left,right,image)
    return ProofNarrativeModel(steps,(NarrativeCitation(1,LiteratureReference(label='source',locator='source'),(0,)),),
                               ((1,),(),(),(),(),()),5,ProofSearchStatus.COMPLETE)


@pytest.mark.parametrize('n',[4,5,8])
def test_generic_composition_branch(n):
    model = branch_fixture(n)
    nodes,leaves,lines = match_composition_branch(model,5)
    assert nodes == frozenset(range(6)) and leaves == frozenset({0})
    assert len(lines) == 2 and lines[0].startswith('[R1]より, $E(') and lines[1].startswith('$E(')
    assert match_composition_branch(replace(model,step_citation_numbers=((),)*6),5) is None
    assert match_composition_branch(replace(model,step_citation_numbers=((1,),(),(),(),(1,),())),5) is None
    assert match_composition_branch(replace(model,citations=()),5) is None
    bad = replace(model.steps[5],premises=tuple(reversed(model.steps[5].premises)))
    assert match_composition_branch(replace(model,steps=model.steps[:-1]+(bad,)),5) is None
    bad = replace(model.steps[5],premises=model.steps[5].premises[:1])
    assert match_composition_branch(replace(model,steps=model.steps[:-1]+(bad,)),5) is None
    assert match_composition_branch(model,4) is None


def test_actual_composition_display():
    invocation,result,calls,model,view = capture()
    assert result.status is ProofSearchStatus.COMPLETE and not result.open_goals
    assert view.key == 'generic-complete-proof'
    assert len(result.proven_steps) == len(model.steps) == 43 and len(model.citations) == 8
    q, = [i for i,s in enumerate(model.steps) if s.inference_rule is not None and s.inference_rule.name == RULE_NAME]
    step = model.steps[q]
    image, = [i for i,s in enumerate(model.steps) if s is step.premises[-1]]
    nodes,leaves,old = match_composition_branch(model,image)
    assert nodes == frozenset({35,36,37,38,39,40}) and leaves == frozenset({35})
    reason = project_rank_two_quotient_reason(step.conclusion,step)
    assert reason is not None
    first,middle,last = [s if s.endswith('.') else s+'.' for s in reason.split('. ')]
    new = '[R8]を用いて, '+middle.removeprefix('また, ')
    before = (model.steps,model.citations,model.step_citation_numbers)
    markdown = render_model_backed_narrative_markdown(result,model)
    lines = markdown.splitlines()
    body = lines[lines.index('証明')+1:]
    assert body.count(new) == 1 and all(x not in body for x in (*old,middle)), markdown
    assert body.index(first) < body.index(new) < body.index(last)
    # Reconstruct the exact pre-compression presentation to test the pure
    # projection and rejection of unsafe/ambiguous variants independently.
    original = list(lines)
    original[original.index(new)] = middle
    k = original.index(first)
    original[k:k] = [old[0],'',old[1],'']
    projected,plan = project_suspension_composition_display(original,model)
    assert projected == lines and plan['branch_indices'] == sorted(nodes)
    assert plan['citation_numbers'] == [8] and plan['replacement'] == new
    assert project_suspension_composition_display(projected,model) == (projected,{})
    for j in nodes | {q}:
        assert project_suspension_composition_display(original,model,{j}) == (original,{})
    assert project_suspension_composition_display(original,replace(model,status=ProofSearchStatus.PARTIAL)) == (original,{})
    assert project_suspension_composition_display(original,replace(model,open_goals=(step.conclusion,))) == (original,{})
    duplicate = list(original)
    duplicate.insert(duplicate.index(old[0]),old[0])
    assert project_suspension_composition_display(duplicate,model) == (duplicate,{})
    wrong = [s.replace('[R8]より,','[R7]より,') if s == old[0] else s for s in original]
    assert project_suspension_composition_display(wrong,model) == (wrong,{})
    # Even an invisible extra consumer in the model blocks suppression.
    extra = ProofStep(model.steps[38].conclusion,(model.steps[38],),ProofRule.INFERENCE)
    shared = replace(model,steps=model.steps+(extra,),step_citation_numbers=model.step_citation_numbers+((),))
    assert project_suspension_composition_display(original,shared) == (original,{})
    assert before == (model.steps,model.citations,model.step_citation_numbers)
    assert all(model.steps[i] in result.proven_steps for i in nodes)
    print('PHASE177_R17R6R1_BRANCH_INDICES='+str(sorted(nodes)))
    print('PHASE177_R17R6R1_HIDDEN_DISPLAY_INDICES=[38, 39]')
    print('PHASE177_R17R6R1_FINAL_SENTENCE='+new)
    print('PHASE177_R17R6R1_ROOT_STEPS=43')
    print('PHASE177_R17R6R1_REFERENCE_COUNT=8')
