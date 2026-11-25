"""Audit helpers and the already-correct shared kernel statement renderer."""
from dataclasses import replace

import pytest

from phase176_r3r52_complete_renderer_boundary.audit import kernel_style, display_audit
from phase176_r3r47_finite_cyclic_kernel_frontier.tests.test_frontier import kernel_fixture
from phase168_r3_27_typed_statement_projection import typed_sentence
from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from proof import ProofRule, ProofStep


@pytest.mark.parametrize('q,n,m', [(6,2,4),(9,5,2),(13,6,8)])
def test_kernel_common_renderer_is_subgroup_and_projection_is_classifiable(q,n,m):
    goal, _, _ = kernel_fixture(q,n,m)
    # This is only a rendering fixture, not a proof accepted by search.
    step = ProofStep(goal, (), ProofRule.INFERENCE)
    assert kernel_style(render_repository_conclusion_latex(goal)) == 'subgroup'
    assert kernel_style(typed_sentence(goal, step)) in ('integer_braces', 'subgroup')


def test_kernel_style_does_not_classify_unrelated_group_equation():
    assert kernel_style(r'\pi_8^3=\mathbb{Z}/2') == 'not_kernel'
    assert kernel_style(None) == 'not_kernel'
    assert kernel_style(r'\ker(H)=\langle 2a\rangle') == 'subgroup'
    assert kernel_style(r'\ker(H)=\mathbb{Z}\{2a\}') == 'integer_braces'


def test_display_diagnostics_do_not_change_text():
    md = '$a=a$.\n$b=c$.\n$b=c$.\n$x=y=z$.\n'
    report = display_audit(md)
    assert report['apparent_identity_equations'] == ['a=a']
    assert report['repeated_equations'] == {'b=c': 2}
    assert not report['english_exactness_present']
