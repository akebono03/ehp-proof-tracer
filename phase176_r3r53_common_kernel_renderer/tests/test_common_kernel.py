"""Rendering fixtures only; no fabricated accepted proof."""
from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase176_r3r47_finite_cyclic_kernel_frontier.tests.test_frontier import kernel_fixture
from phase176_r3r53_common_kernel_renderer.apply import TARGET, OLD, NEW, updated_source
from proof import ProofRule, ProofStep
from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from web_group_proof_common import _group_proof_statement_latex


def rendering_fixture(statement):
    return ProofStep(statement, (), ProofRule.INFERENCE)


@pytest.mark.parametrize('q,n,m', [(6,2,4),(9,5,2),(13,6,8)])
def test_complete_trace_and_shared_kernel_agree(q,n,m):
    goal, _, _ = kernel_fixture(q,n,m)
    direct = render_repository_conclusion_latex(goal)
    assert typed_sentence(goal, rendering_fixture(goal)) == '$' + direct + '$.'
    assert _group_proof_statement_latex(goal) == (direct, None)
    assert r'\langle ' in direct and r'\rangle' in direct
    assert r'\mathbb{Z}' not in direct


def test_suspension_kernel_uses_same_shared_renderer():
    domain = TodaPrimaryGroup(8,4)
    generator = HomotopyElement('a',4,8,4,GeneratorSymbol('ν',4))
    goal = KernelMultipleStatement(TodaSuspensionMap(domain,TodaPrimaryGroup(9,5)),domain,generator,2)
    direct = render_repository_conclusion_latex(goal)
    assert r'\ker(E:' in direct and r'\langle 2' in direct
    assert typed_sentence(goal, rendering_fixture(goal)) == '$' + direct + '$.'


def test_explicit_free_cyclic_kernel_keeps_its_proved_free_group_display():
    domain = TodaPrimaryGroup(3,2)
    generator = HomotopyElement('η₂',2,3,2,GeneratorSymbol('η',2))
    mapping = TodaSuspensionMap(domain,TodaPrimaryGroup(4,3))
    statement = SuspensionKernelFreeCyclicStatement(mapping, FreeCyclicGroup(generator))
    sentence = typed_sentence(statement, rendering_fixture(statement))
    assert r'\ker E=\mathbb{Z}' in sentence
    assert r'\langle' not in sentence


def test_invalid_kernel_domain_refuses_projection():
    goal, _, _ = kernel_fixture(6,2,4)
    invalid = replace(goal, domain=TodaPrimaryGroup(7,5))
    with pytest.raises(TypeError):
        render_repository_conclusion_latex(invalid)
    assert typed_sentence(invalid, rendering_fixture(invalid)) is None


def test_projection_calls_common_renderer(monkeypatch):
    import toda_conclusion_latex_renderer as common
    goal, _, _ = kernel_fixture(6,2,4)
    original = common.render_repository_conclusion_latex
    calls = []
    def spy(statement):
        calls.append(statement)
        return original(statement)
    monkeypatch.setattr(common, 'render_repository_conclusion_latex', spy)
    assert typed_sentence(goal, rendering_fixture(goal)) == '$' + original(goal) + '$.'
    assert len(calls) == 1 and calls[0] is goal


def test_patch_idempotent_and_preserves_every_other_byte():
    raw = TARGET.read_bytes()
    assert updated_source(raw) == raw
    text = raw.decode('utf-8').replace('\r\n','\n')
    assert text.count(NEW) == 1 and OLD not in text
    baseline = text.replace(NEW,OLD,1)
    for eol in ('\n','\r\n'):
        before = baseline.replace('\n', eol).encode('utf-8')
        after = text.replace('\n', eol).encode('utf-8')
        assert updated_source(before) == after
        assert updated_source(after) == after
    with pytest.raises(ValueError):
        updated_source(raw+b'\n# unrelated change\n')
