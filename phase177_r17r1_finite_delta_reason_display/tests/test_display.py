from dataclasses import replace
import re

import pytest

from expression import Composition, Suspension
from phase177_r14_finite_cyclic_delta_injective_isolated.tests.test_rule import (
    fixture, hypothetical, replay,
)
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import (
    ORDER_RULE, INJECTIVE_RULE, expand_summand_generator_order, expand_finite_delta_injective,
)
from phase177_r17r1_finite_delta_reason_display.projection import (
    project_finite_delta_reason, project_concise_delta_display,
)
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase175_r4r12r10r1_cited_511_public.source import canonical_511
from toda_human_readable_renderer import render_toda_public_group_generator_latex
from proof import ProofRule
from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
from web_group_proof_common import _group_proof_statement_latex


@pytest.mark.parametrize('n,m', [(3,2),(4,4),(5,8)])
def test_generic_display(n,m):
    goal,domain,codomain,image,order = fixture(n,m)
    first, = expand_summand_generator_order(order,codomain)
    second, = expand_finite_delta_injective(goal,domain,image,order)
    o = replay(first,(hypothetical(codomain,ProofRule.GIVEN),),order)
    d = replay(second,(hypothetical(domain,ProofRule.GIVEN),hypothetical(image),o),goal)
    expected_order = rf"直和成分の生成元なので, $\operatorname{{ord}}(b)={m}$."
    expected_delta = (rf"始域は位数 ${m}$ の巡回群で, $\Delta(a)=b$ の位数も ${m}$ なので, "
                      rf"$\Delta:\pi_{{{2*n+2}}}^{{{2*n+1}}}\to \pi_{{{2*n}}}^{{{n}}}$ は単射.")
    assert project_finite_delta_reason(order,o) == expected_order
    assert project_finite_delta_reason(goal,d) == expected_delta
    assert typed_sentence(order,o) == expected_order
    assert typed_sentence(goal,d) == expected_delta
    assert project_finite_delta_reason(order,replace(o,premises=())) is None
    assert project_finite_delta_reason(goal,replace(d,premises=d.premises[:2])) is None
    assert project_finite_delta_reason(goal,replace(d,rule=ProofRule.GIVEN)) is None
    wrong_order = replace(o,conclusion=replace(order,order=m+1))
    assert project_finite_delta_reason(wrong_order.conclusion,wrong_order) is None
    assert project_finite_delta_reason(goal,replace(d,premises=(*d.premises[:2],wrong_order))) is None


def test_canonical_composite_renderer():
    value = canonical_511().rhs
    assert isinstance(value,Composition) and isinstance(value.left,Suspension)
    lhs = render_toda_public_group_generator_latex(value.left)
    rhs = render_toda_public_group_generator_latex(value.right)
    assert lhs.startswith(r'E\nu') and lhs != r'E\nu_{3}' and lhs != r'E\nu'
    assert rhs == r'\eta_{7}'
    assert render_toda_public_group_generator_latex(value) == lhs + rhs


def test_actual_display():
    invocation,result,calls,model,view = capture()
    assert result.status.value == 'complete' and not result.open_goals
    assert view.key == 'generic-complete-proof'
    assert len(result.proven_steps) == len(model.steps) == 43
    assert len(model.citations) == 8
    order, = [s for s in model.steps if s.inference_rule is not None and s.inference_rule.name == ORDER_RULE]
    injective, = [s for s in model.steps if s.inference_rule is not None and s.inference_rule.name == INJECTIVE_RULE]
    assert order.conclusion.element == canonical_511().rhs or order.conclusion.element == injective.premises[1].conclusion.target_generator
    b = render_toda_public_group_generator_latex(order.conclusion.element)
    a = render_toda_public_group_generator_latex(injective.premises[1].conclusion.source_generator)
    order_sentence = project_finite_delta_reason(order.conclusion,order)
    injective_sentence = project_finite_delta_reason(injective.conclusion,injective)
    assert order_sentence is not None and rf'\operatorname{{ord}}({b})=2' in order_sentence
    assert injective_sentence is not None and rf'\Delta({a})={b}' in injective_sentence
    assert typed_sentence(order.conclusion,order) == order_sentence
    assert typed_sentence(injective.conclusion,injective) == injective_sentence
    markdown = render_model_backed_narrative_markdown(result,model)
    assert '直和成分の生成元なので' not in markdown
    assert rf'\operatorname{{ord}}({b})=2' not in markdown
    assert '始域は位数' not in markdown
    assert r'よって, $\Delta:\pi_{10}^{9}\to \pi_{8}^{4}$ は単射.' in markdown
    assert order in result.proven_steps and order in injective.premises
    # Inspect the actual typed equality premise, not the separate prose
    # formatter's spelling. Ignore only TeX whitespace and sizing commands.
    equality = delta_image_equality(injective.premises[1].conclusion)
    assert equality is not None
    equality_step, = [parent for parent in injective.premises[1].premises
                      if parent.conclusion == equality]
    assert equality_step in model.steps
    latex, fallback = _group_proof_statement_latex(equality_step.conclusion)
    assert latex is not None and fallback is None
    def display_key(value):
        return re.sub(r'\s+', '', value.replace(r'\left', '').replace(r'\right', ''))
    lines = markdown.splitlines()
    boundary = lines.index('証明')
    concise = r'よって, $\Delta:\pi_{10}^{9}\to \pi_{8}^{4}$ は単射.'
    end = lines.index(concise, boundary + 1)
    prior_math = [term for line in lines[boundary + 1:end]
                  for term in re.findall(r'\$([^$]+)\$', line)]
    expected = display_key(latex)
    assert expected == display_key(rf'\Delta({a})={b}')
    assert expected in {display_key(term) for term in prior_math}, (latex, prior_math)
    print('PHASE177_R17R1R2R1_DELTA_IMAGE_LATEX='+latex)
    print('PHASE177_R17R1R2R1_ROOT_STEPS=43')
    print('PHASE177_R17R1R2R1_REFERENCE_COUNT=8')
    print('PHASE177_R17R1R2R1_DISPLAY=VERIFIED')



def test_concise_projection_guards():
    from types import SimpleNamespace
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
    goal,domain,codomain,image,order = fixture(5,8)
    first, = expand_summand_generator_order(order,codomain)
    second, = expand_finite_delta_injective(goal,domain,image,order)
    domain_step = hypothetical(domain,ProofRule.GIVEN)
    codomain_step = hypothetical(codomain,ProofRule.GIVEN)
    equality_step = hypothetical(delta_image_equality(image))
    image_step = replace(hypothetical(image),premises=(equality_step,))
    witness = replay(first,(codomain_step,),order)
    injective = replay(second,(domain_step,image_step,witness),goal)
    steps = (domain_step,codomain_step,equality_step,image_step,witness,injective)
    model = SimpleNamespace(steps=steps,root_index=5,step_citation_numbers=((),)*6)
    order_indices = tuple(range(6))
    hidden,sentences = project_concise_delta_display(model,order_indices,set())
    assert hidden == frozenset({4})
    assert sentences == {5:r'よって, $\Delta:\pi_{12}^{11}\to \pi_{10}^{5}$ は単射.'}
    for changed, suppressed in (
        (model,{2}), (model,{1}), (model,{5}),
        (SimpleNamespace(steps=steps,root_index=4,step_citation_numbers=((),)*6),set()),
        (SimpleNamespace(steps=steps,root_index=5,step_citation_numbers=((),(),(),(),(1,),())),set()),
        (SimpleNamespace(steps=steps+(replace(hypothetical(order),premises=(witness,)),),
                         root_index=5,step_citation_numbers=((),)*7),set()),
    ):
        assert project_concise_delta_display(changed,order_indices,suppressed) == (frozenset(),{})
