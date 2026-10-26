"""R3Z: general cited schema in Reference, concrete certified form in prose."""
from __future__ import annotations

import re

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, Relation
from web_group_proof_common import _group_proof_statement_latex


@pytest.fixture(scope="module")
def rendered_pi53():
    bridge = build_shared_typed_bridge()
    contexts = []
    proof = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert proof.status is ProofSearchStatus.COMPLETE
    assert len(contexts) == 1
    model = build_linked_proof_narrative_model(proof, contexts[0])
    markdown = render_model_backed_narrative_markdown(proof, model)
    parts = markdown.split("\n証明\n", 1)
    assert len(parts) == 2
    return proof, model, parts[0], parts[1]


def test_r3z_general_higher_eta_is_reference_only(rendered_pi53):
    proof, model, reference, body = rendered_pi53
    assert proof.status is ProofSearchStatus.COMPLETE
    assert len(model.steps) == 28
    assert r"\pi_{n+1}^{n}" in reference
    assert r"\pi_{n+1}^{n}" not in body
    assert r"\eta_{n}" not in body
    assert r"\pi_{6}^{5}" in body
    assert body.rstrip().endswith("□")


def test_r3z_specialization_cites_the_exact_general_source(rendered_pi53):
    _, model, _, body = rendered_pi53
    originals = [
        (index, step) for index, step in enumerate(model.steps)
        if step.rule is ProofRule.GIVEN
        and _is_generic_eta_group_relation(step.conclusion)
    ]
    assert len(originals) == 1
    source_index, source_step = originals[0]
    numbers = model.step_citation_numbers[source_index]
    assert len(numbers) == 1
    specialist = [
        step for step in model.steps
        if step.rule is ProofRule.INFERENCE
        and isinstance(step.conclusion, Relation)
        and any(parent is source_step or parent == source_step
                for parent in step.premises)
        and specialize_typed_statement(source_step.conclusion, step.conclusion) is not None
        and step.conclusion.lhs.group_dimension == 6
        and step.conclusion.lhs.sphere_dimension == 5
    ]
    assert len(specialist) == 1
    latex, problem = _group_proof_statement_latex(specialist[0].conclusion)
    assert latex is not None and problem is None
    assert any(
        f"[R{numbers[0]}]より" in line and f"${latex}$" in line
        for line in body.splitlines()
    )


def test_r3z_all_references_and_final_ehp_conclusion_retained(rendered_pi53):
    _, model, reference, body = rendered_pi53
    expected = {citation.number for citation in model.citations}
    shown = {int(number) for number in re.findall(r"\[R(\d+)\]", body)}
    assert shown == expected
    assert len(model.citations) == 6
    assert "Proposition 5.1" in reference
    assert "(5.1)" in reference
    assert "(5.3)" in reference
    assert r"\pi_{5}^{3}" in body
