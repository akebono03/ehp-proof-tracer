"""Focused rendering and existing rule-boundary tests, not new mathematical proofs."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import conditional_inputs
from phase176_r3r47_finite_cyclic_kernel_frontier.apply import TARGET, updated_source
from proof import Relation, RelationType
from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from toda_rules import TodaDeltaImageUpToSignStatement
from web_group_proof_common import _group_proof_statement_latex


def kernel_fixture(q, n, m):
    domain = TodaPrimaryGroup(q+2, 2*n+1)
    codomain = TodaPrimaryGroup(q, n)
    a = HomotopyElement('a', 2*n+1, q+2, 2*n+1, GeneratorSymbol('ν', 2*n+1))
    b = HomotopyElement('b', n, q, n, GeneratorSymbol('η', n))
    delta = TodaDeltaMap(domain, codomain)
    kernel = KernelMultipleStatement(delta, domain, a, m)
    dst = Relation(codomain, FiniteCyclicGroup(m,b), RelationType.EQUALITY)
    signed = TodaDeltaImageUpToSignStatement(delta, a,b)
    return kernel, dst, signed


@pytest.mark.parametrize('q,n,m', [(6,2,4),(9,5,2),(13,6,8)])
def test_kernel_display_is_generic_subgroup_not_free_cyclic_claim(q,n,m):
    kernel, _, _ = kernel_fixture(q,n,m)
    direct = render_repository_conclusion_latex(kernel)
    latex, fallback = _group_proof_statement_latex(kernel)
    assert fallback is None and latex == direct
    assert r'\ker(\Delta:' in latex
    assert rf'\pi_{{{q+2}}}^{{{2*n+1}}}' in latex
    assert rf'\pi_{{{q}}}^{{{n}}}' in latex
    assert rf'\langle {m}' in latex and r'\rangle' in latex
    assert r'\mathbb{Z}' not in latex


def test_wrong_domain_has_no_kernel_display():
    kernel, _, _ = kernel_fixture(6,2,4)
    wrong = replace(kernel, domain=TodaPrimaryGroup(7,5))
    with pytest.raises(TypeError, match='unsupported typed kernel'):
        render_repository_conclusion_latex(wrong)


def test_suspension_kernel_display_also_supported():
    domain = TodaPrimaryGroup(8,4)
    generator = HomotopyElement('a',4,8,4,GeneratorSymbol('ν',4))
    goal = KernelMultipleStatement(TodaSuspensionMap(domain,TodaPrimaryGroup(9,5)), domain,generator,2)
    latex, fallback = _group_proof_statement_latex(goal)
    assert fallback is None and r'\ker(E:' in latex
    assert r'\langle 2' in latex


@pytest.mark.parametrize('q,n,m',[(6,2,4),(9,5,2),(13,6,8)])
def test_r35_existing_free_domain_boundary(q,n,m):
    kernel, dst, signed = kernel_fixture(q,n,m)
    free = Relation(kernel.domain,FreeCyclicGroup(kernel.source_generator),RelationType.EQUALITY)
    finite = Relation(kernel.domain,FiniteCyclicGroup(2*m,kernel.source_generator),RelationType.EQUALITY)
    # For q=9,n=5 the free-domain fixture is the historical diagonal case.
    assert conditional_inputs(kernel,free,dst,signed) == (free,dst,signed)
    assert conditional_inputs(kernel,finite,dst,signed) is None


def test_renderer_patch_is_idempotent_and_fails_closed():
    current = TARGET.read_bytes()
    assert updated_source(current) == current
    with pytest.raises(ValueError,match='UNREVIEWED_RENDERER_BASELINE'):
        updated_source(current.replace(b'\r\n', b'\n') + b'\n# unreviewed\n')
