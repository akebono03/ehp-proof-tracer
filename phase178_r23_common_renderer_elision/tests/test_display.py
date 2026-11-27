"""Common display-only elision, including the real verified n=6 proof."""
from dataclasses import replace
from unittest.mock import patch

import pytest

from expression import Composition
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase169_r10e5_composite_generator_image.rule import expand_composite_generator_image
from phase169_r10e5_composite_generator_image.tests.test_r10e5_composite_generator_image import _nu, _image
from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
from phase177_r17r4r1_prop25_suspension_elision.tests.test_display import proved
from phase177_r17r6r1_suspension_composition_display.projection import match_composition_branch
from phase178_r17r3_common_renderer import projection
from phase178_r20_suspension_isomorphism_bridge_isolated.rule import RULE_NAME as ISO_RULE
from phase178_r22_final_verified_proof_audit.audit import display_observation
from proof import ProofRule, ProofStep
from web_group_proof import build_standard_web_group_proof_view


def definition_model(n):
    goal = _image(n,6,Composition(_nu(n),_nu(n+3)),Composition(_nu(n+1),_nu(n+4)))
    option, = expand_composite_generator_image(goal)
    factors = []
    for part in option.subgoals:
        definition, = expand_defined_stable_element_image(part)
        factors.append(proved(definition.rule,(),part))
    image = proved(option.rule,tuple(factors),goal)
    return ProofNarrativeModel((*factors,image),(),((),(),()),2,ProofSearchStatus.COMPLETE)


@pytest.mark.parametrize('n',[5,6,8])
def test_definition_only_composition(n):
    model = definition_model(n)
    # Preserve the older rank-two projection's default cited-only contract.
    assert match_composition_branch(model,2) is None
    branch,leaves,old = match_composition_branch(model,2,allow_definition_only=True)
    assert branch == frozenset({0,1,2}) and leaves == frozenset()
    composite = typed_sentence(model.steps[2].conclusion,model.steps[2])
    original = ['使用する結果','','証明','',old[0],'',old[1],'',composite,'','□']
    expected = ['使用する結果','','証明','',composite,'','□']
    assert projection.project_composite_suspension_lines(original,model) == expected
    assert projection.project_composite_suspension_lines(expected,model) == expected
    assert all('より, ' not in line for line in expected)
    for i in branch:
        assert projection.project_composite_suspension_lines(original,model,{i}) == original
    assert projection.project_composite_suspension_lines(original,replace(model,status=ProofSearchStatus.PARTIAL)) == original
    assert projection.project_composite_suspension_lines(original,replace(model,open_goals=(model.steps[2].conclusion,))) == original
    extra = ProofStep(model.steps[0].conclusion,(model.steps[0],),ProofRule.INFERENCE)
    shared = replace(model,steps=model.steps+(extra,),step_citation_numbers=((),(),(),()))
    assert projection.project_composite_suspension_lines(original,shared) == original
    assert projection.project_composite_suspension_lines(original,replace(model,step_citation_numbers=((1,),(),()))) == original
    duplicate = original[:4]+[old[0],'']+original[4:]
    assert projection.project_composite_suspension_lines(duplicate,model) == duplicate
    changed = replace(model.steps[2],premises=tuple(reversed(model.steps[2].premises)))
    assert match_composition_branch(replace(model,steps=model.steps[:2]+(changed,)),2,allow_definition_only=True) is None


@pytest.fixture(scope='module')
def actual():
    import phase165_r52_r3_web_adapter as adapter
    real = adapter.build_partial_web_group_proof_view
    captured = []
    def capture(result, **kwargs):
        view = real(result,**kwargs)
        captured.append((result,kwargs.get('narrative_model'),view))
        return view
    with patch.object(adapter,'build_partial_web_group_proof_view',capture):
        view = build_standard_web_group_proof_view(n=6,k=6,max_depth=2,mode='narrative',citation_source='model')
    assert len(captured) == 1
    result,model,rendered = captured[0]
    assert result.status is ProofSearchStatus.COMPLETE and not result.open_goals
    assert view.key == rendered.key == 'generic-complete-proof'
    assert len(result.proven_steps) == len(model.steps) == 18 and len(model.citations) == 5
    composite, = [i for i,s in enumerate(model.steps) if s.inference_rule is not None and s.inference_rule.name == 'suspension preserves composition of separately proved maps']
    iso, = [i for i,s in enumerate(model.steps) if s.inference_rule is not None and s.inference_rule.name == ISO_RULE]
    generic, = [i for i,s in enumerate(model.steps) if s is model.steps[iso].premises[0]]
    with patch.object(projection,'project_composite_suspension_lines',side_effect=lambda lines,*a:lines), \
         patch.object(projection,'project_typed_suspension_iso_lines',side_effect=lambda lines,*a:lines):
        baseline = render_model_backed_narrative_markdown(result,model).splitlines()
    return result,model,rendered,baseline,composite,iso,generic


def test_real_public_display(actual):
    result,model,view,baseline,composite,iso,generic = actual
    before = (model.steps,model.citations,model.step_citation_numbers)
    branch,leaves,old = match_composition_branch(model,composite,allow_definition_only=True)
    assert leaves == frozenset() and len(branch) == 3
    assert all(baseline.count(line) == 1 for line in old)
    combined = typed_sentence(model.steps[composite].conclusion,model.steps[composite])
    bare = typed_sentence(model.steps[iso].conclusion,model.steps[iso])
    reason = typed_sentence(model.steps[generic].conclusion,model.steps[generic])
    assert baseline.count(bare) == baseline.count(reason) == 1
    markdown = render_model_backed_narrative_markdown(result,model)
    lines = markdown.splitlines()
    expected = projection.project_composite_suspension_lines(baseline,model)
    expected = projection.project_typed_suspension_iso_lines(expected,model)
    assert lines == expected
    boundary = lines.index('証明')
    assert lines[:boundary] == baseline[:baseline.index('証明')]
    assert all(s not in lines for s in old) and bare not in lines
    assert lines.count(combined) == lines.count(reason) == 1
    assert lines.index(reason) < lines.index(combined)
    assert lines[-1] == '□'
    # Check the actual Web view, not only the intermediate Markdown.
    observed = display_observation([str(x) for x in view.rendered_lines],
        (r'E(\nu_{5})=\nu_{6}',r'E(\nu_{8})=\nu_{9}'),
        r'E(\nu_{5}^{2})=\nu_{6}^{2}',r'E: \pi_{11}^{5}\to \pi_{12}^{6}')
    assert observed == {'factor_line_counts':[0,0],'composite_line_count':1,'isomorphism_line_count':1}
    assert before == (model.steps,model.citations,model.step_citation_numbers)
    print('PHASE178_R23_ROOT_PROVEN_STEP_COUNT=18')
    print('PHASE178_R23_MODEL_REFERENCE_COUNT=5')
    print('PHASE178_R23_DEFINITION_ONLY_COMPOSITION_ELISION=VERIFIED')
    print('PHASE178_R23_TYPED_ISOMORPHISM_ELISION=VERIFIED')
    print('PHASE178_R23_DISPLAY_OBSERVATION='+str(observed))
    print(markdown)


def test_typed_iso_guard(actual):
    _,model,_,baseline,_,iso,generic = actual
    project = projection.project_typed_suspension_iso_lines
    output = project(baseline,model)
    assert output != baseline and project(output,model) == output
    for i in (iso,generic):
        assert project(baseline,model,{i}) == baseline
    assert project(baseline,replace(model,status=ProofSearchStatus.PARTIAL)) == baseline
    assert project(baseline,replace(model,open_goals=(model.steps[iso].conclusion,))) == baseline
    numbers = list(model.step_citation_numbers)
    numbers[iso] = (1,)
    assert project(baseline,replace(model,step_citation_numbers=tuple(numbers))) == baseline
    bare = typed_sentence(model.steps[iso].conclusion,model.steps[iso])
    reason = typed_sentence(model.steps[generic].conclusion,model.steps[generic])
    pos = baseline.index(bare)
    duplicate = baseline[:pos]+[bare,'']+baseline[pos:]
    assert project(duplicate,model) == duplicate
    unrelated = baseline[:pos]+['別の説明.','']+baseline[pos:]
    assert project(unrelated,model) == unrelated
    without_reason = [s for s in baseline if s != reason]
    assert project(without_reason,model) == without_reason
