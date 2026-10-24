"""R3-41L: typed specialization sources and reasoned diagonal suspension."""
from __future__ import annotations

import re
from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroupZeroStatement, TodaSuspensionIsomorphismStatement
from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_38_frozen_fulltext_audit.audit import sections
from phase168_r3_39f_frozen_comparison.audit import assess
from proof import ProofRule, Relation


@pytest.fixture(scope="module")
def cases():
    bridge = build_shared_typed_bridge()
    result = {}
    for name, n, k in (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1)):
        contexts = []
        proof = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        assert proof.status is ProofSearchStatus.COMPLETE
        assert contexts
        model = build_linked_proof_narrative_model(proof, contexts[-1])
        result[name] = (proof, model, render_model_backed_narrative_markdown(proof, model))
    return result


def _expected_validated_specialization(model, step):
    if step.rule is not ProofRule.INFERENCE or len(step.premises) != 1:
        return ()
    parent = step.premises[0]
    if parent.rule is not ProofRule.GIVEN:
        return ()
    source, target = parent.conclusion, step.conclusion
    if isinstance(source, Relation) and isinstance(target, Relation):
        valid = specialize_typed_statement(source, target) is not None
    elif isinstance(target, TodaPrimaryGroupZeroStatement):
        if isinstance(source, TodaPrimaryGroupZeroStatement):
            valid = specialize_typed_statement(source, target) is not None
        elif isinstance(source, Toda51BelowDiagonalZeroStatement):
            group = target.group
            i, n = group.group_dimension, group.sphere_dimension
            valid = type(i) is int and type(n) is int and 0 <= i < n and n >= 2
        else:
            valid = False
    else:
        valid = False
    if not valid:
        return ()
    return tuple(dict.fromkeys(
        number for i, candidate in enumerate(model.steps)
        if candidate == parent
        for number in model.step_citation_numbers[i]
    ))


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3"))
def test_validated_general_specializations_have_explanatory_citations(cases, name):
    proof, model, markdown = cases[name]
    _, body = sections(markdown)
    from web_group_proof_common import _group_proof_statement_latex
    for step in model.steps:
        source_numbers = _expected_validated_specialization(model, step)
        if not source_numbers:
            continue
        statement_latex, problem = _group_proof_statement_latex(step.conclusion)
        if statement_latex is None or problem is not None:
            continue
        expected = ", ".join(f"[R{number}]" for number in source_numbers)
        assert f"{expected}より, ${statement_latex}$ を得る." in body
        assert f"導出により, ${statement_latex}$ を得る." not in body
    assert body.rstrip().endswith("□")


def test_toda51_circle_and_diagonal_specializations_are_explicit(cases):
    _, model, markdown = cases["pi3_2"]
    _, proof = sections(markdown)
    assert r"\pi_{2}^{1} = 0" in proof
    assert r"\pi_{1}^{1} = \mathbb{Z}\{\iota_{1}\}" in proof
    assert r"\pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}" in proof
    assert r"\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}" in proof
    for snippet in (
        r"\pi_{2}^{1} = 0",
        r"\pi_{1}^{1} = \mathbb{Z}\{\iota_{1}\}",
        r"\pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}",
        r"\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}",
    ):
        lines = [line for line in proof.splitlines() if snippet in line]
        assert len(lines) == 1
        assert "導出により" not in lines[0]
        assert re.search(r"\[R\d+\]より", lines[0])


def test_pi43_below_diagonal_and_diagonal_specializations_are_explicit(cases):
    _, model, markdown = cases["pi4_3"]
    _, proof = sections(markdown)
    for snippet in (r"\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}", r"\pi_{4}^{5} = 0"):
        lines = [line for line in proof.splitlines() if snippet in line]
        assert len(lines) == 1
        assert "導出により" not in lines[0]
        assert re.search(r"\[R\d+\]より", lines[0])


def test_diagonal_iso_connective_has_matching_generator_premise(cases):
    _, model, markdown = cases["pi3_2"]
    iso_steps = [step for step in model.steps
                 if isinstance(step.conclusion, TodaSuspensionIsomorphismStatement)
                 and any(isinstance(p.conclusion, GeneratorSuspension)
                         and p.conclusion.map == step.conclusion.map
                         for p in step.premises)]
    assert iso_steps
    assert "これより, $E: \\pi_{1}^{1}\\to \\pi_{2}^{2}$ は同型." in markdown


def test_pi54_specialization_and_transport_unchanged(cases):
    _, model, markdown = cases["pi5_4"]
    _, proof = sections(markdown)
    a = proof.index(r"\pi_{4}^{3} = \mathbb{Z}/2")
    b = proof.index("(n,m,k)=(3,4,1)")
    c = proof.index(r"E(\eta_{3})=\eta_{4}")
    assert a < b < c
    assert r"\pi_{5}^{4} = \mathbb{Z}/2\{E\eta_{3}\}" in proof
    assert "導出により" in proof
    assert proof.rstrip().endswith("□")


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3", "pi5_4"))
def test_existing_reference_and_frozen_checks_still_hold(cases, name):
    result, model, markdown = cases[name]
    _, body = sections(markdown)
    expected = {citation.number for citation in model.citations}
    actual = {int(number) for number in re.findall(r"\[R(\d+)\]", body)}
    assert actual == expected
    assert all(citation.statement_bodies for citation in model.citations)
    assert all(item["present"] for item in assess(name, body))
    assert body.rstrip().endswith("□")


def test_unrelated_root_claim_is_not_promoted_to_reference(cases):
    _, model, markdown = cases["pi5_4"]
    _, proof = sections(markdown)
    transport_lines = [line for line in proof.splitlines()
                       if r"\pi_{5}^{4} = \mathbb{Z}/2\{E\eta_{3}\}" in line]
    assert len(transport_lines) == 1
    assert not re.search(r"\[R\d+\]より", transport_lines[0])
