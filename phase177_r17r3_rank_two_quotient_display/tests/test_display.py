from dataclasses import replace

import pytest

from expression import HomotopyElement
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase175_r4r3_two_summand_quotient.rule import RULE_NAME, expand_two_summand_quotient
from phase175_r4r3_two_summand_quotient.tests.test_rule import synthetic
from phase177_r17r3_rank_two_quotient_display.projection import project_rank_two_quotient_reason
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase168_r3_27_typed_statement_projection import typed_sentence, group_tex
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, Relation, apply_inference_match, find_inference_matches_for_rule
from toda_human_readable_renderer import render_toda_public_group_generator_latex
from web_group_proof_common import _group_proof_statement_latex


def quotient_fixture(n, stem, swap=False):
    q = n + stem
    A, B, C = TodaPrimaryGroup(q,n), TodaPrimaryGroup(q+1,n+1), TodaPrimaryGroup(q+2,2*n+1)
    a, b = (HomotopyElement(name,n,q,n) for name in ('a','b'))
    z = HomotopyElement('z',2*n+1,q+2,2*n+1)
    y = HomotopyElement('y',n+1,q+1,n+1)
    parts = (FiniteCyclicGroup(2,a),FiniteCyclicGroup(2,b))
    middle = Relation(A,DirectSumGroup(tuple(reversed(parts)) if swap else parts))
    domain = Relation(C,FiniteCyclicGroup(2,z))
    delta = GeneratorImage(TodaDeltaMap(C,A),z,b)
    image = GeneratorImage(TodaSuspensionMap(A,B),a,y)
    goal = CyclicStructureStatement(B,y,2)
    option, = expand_two_summand_quotient(goal,middle,domain,delta,image)
    parents = tuple(synthetic(s,ProofRule.GIVEN if i < 2 else ProofRule.INFERENCE)
                    for i,s in enumerate(option.subgoals))
    matches = find_inference_matches_for_rule(option.rule,parents)
    step, = (apply_inference_match(match) for match in matches if match.premises == parents)
    return step, a, b


@pytest.mark.parametrize('n,stem,swap', [(4,4,False),(4,5,True),(5,5,False)])
def test_generic_quotient_display(n,stem,swap):
    step,a,b = quotient_fixture(n,stem,swap)
    killed = render_toda_public_group_generator_latex(b)
    survivor = render_toda_public_group_generator_latex(a)
    expected = (
        rf"完全性より, $\ker E=\operatorname{{Im}}\Delta=\mathbb{{Z}}/2\{{{killed}\}}$. "
        rf"また, $E({survivor})=y$. "
        rf"$E$ は全射なので, 準同型定理より $\pi_{{{n+stem+1}}}^{{{n+1}}}\cong \pi_{{{n+stem}}}^{{{n}}}/\ker E$."
    )
    assert project_rank_two_quotient_reason(step.conclusion,step) == expected
    assert typed_sentence(step.conclusion,step) == expected
    for i in range(6):
        assert project_rank_two_quotient_reason(step.conclusion,replace(step,premises=step.premises[:i]+step.premises[i+1:])) is None
    for i in range(2,6):
        bad = list(step.premises)
        bad[i] = replace(bad[i],rule=ProofRule.GIVEN)
        assert project_rank_two_quotient_reason(step.conclusion,replace(step,premises=tuple(bad))) is None
    bad = list(step.premises)
    bad[-1] = replace(bad[-1],conclusion=replace(bad[-1].conclusion,source_generator=b))
    assert project_rank_two_quotient_reason(step.conclusion,replace(step,premises=tuple(bad))) is None
    assert project_rank_two_quotient_reason(step.conclusion,replace(step,rule=ProofRule.GIVEN)) is None


def test_actual_rank_two_quotient_display():
    invocation,result,calls,model,view = capture()
    assert result.status.value == 'complete' and not result.open_goals
    assert view.key == 'generic-complete-proof'
    assert len(result.proven_steps) == len(model.steps) == 43 and len(model.citations) == 8
    step, = [s for s in model.steps if s.inference_rule is not None and s.inference_rule.name == RULE_NAME]
    assert len(step.premises) == 6
    text = project_rank_two_quotient_reason(step.conclusion,step)
    assert text is not None and typed_sentence(step.conclusion,step) == text
    markdown = render_model_backed_narrative_markdown(result,model)
    body = markdown.split('\n証明\n',1)[1]
    pieces = text.split('. ')
    sentences = [p+'.' if not p.endswith('.') else p for p in pieces]
    # R17R6R1 transfers the factor-definition citation to the same
    # certified composite image; the other quotient sentences stay intact.
    assert sentences[1].startswith('また, ')
    sentences[1] = '[R8]を用いて, '+sentences[1].removeprefix('また, ')
    positions = [body.index(s) for s in sentences]
    assert positions == sorted(positions) and len(set(positions)) == 3
    root_latex, fallback = _group_proof_statement_latex(result.conclusion)
    assert root_latex is not None and fallback is None
    assert body.count('$'+root_latex+'$') == 1
    assert positions[-1] < body.index('$'+root_latex+'$')
    print('PHASE177_R17R3_ROOT_STEPS=43')
    print('PHASE177_R17R3_REFERENCE_COUNT=8')
    print('PHASE177_R17R3_QUOTIENT_DISPLAY=VERIFIED')
