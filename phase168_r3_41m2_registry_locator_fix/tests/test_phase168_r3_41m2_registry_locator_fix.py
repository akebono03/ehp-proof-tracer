"""Phase 168 R3-41M: verify concise, source-bound common proof text."""
from __future__ import annotations

import re

import pytest

from phase165_r12_r20_eta_definition import (
    ASSERTION_ID, REFERENCE_ID, build_cited_eta_family_definition,
)

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_38_frozen_fulltext_audit.audit import sections
from phase168_r3_39f_frozen_comparison.audit import assess
from phase168_r3_26_exactness_projection import project_exactness_chains


@pytest.fixture(scope="module")
def cases():
    bridge = build_shared_typed_bridge()
    found = {}
    for name, n, k in (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1)):
        contexts = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=contexts.append,
        )
        assert result.status is ProofSearchStatus.COMPLETE
        assert contexts
        model = build_linked_proof_narrative_model(result, contexts[-1])
        found[name] = (result, model, render_model_backed_narrative_markdown(result, model))
    return found


@pytest.mark.parametrize("name", ("pi4_3", "pi5_4"))
def test_eta_reference_locator_is_short_in_registry_and_display(cases, name):
    _, model, rendered = cases[name]
    reference, proof = sections(rendered)
    eta_refs = [citation for citation in model.citations
                if (citation.reference.locator or citation.reference.label) == "Chapter V, i)"]
    assert len(eta_refs) == 1
    assert eta_refs[0].reference.locator == "Chapter V, i)"
    assert len(eta_refs[0].assertion_ids) == 1
    assert f"**[R{eta_refs[0].number}] Chapter V, i).**" in reference
    assert "The Groups" not in reference
    assert "eta-family notation" not in reference
    assert r"\eta_n=E^{n-2}\eta_2" in reference
    assert f"[R{eta_refs[0].number}]" in proof


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3"))
def test_prop42_reference_is_just_complete_sequence(cases, name):
    _, model, text = cases[name]
    reference, proof = sections(text)
    refs = [citation for citation in model.citations
            if "Proposition 4.2" in (citation.reference.locator or citation.reference.label)]
    assert len(refs) == 1
    assert f"**[R{refs[0].number}] Proposition 4.2 (4.4).**" in reference
    expected = (r"$\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}"
                r"\xrightarrow{H}\pi_{i+1}^{2n+1}"
                r"\xrightarrow{\Delta}\pi_{i-1}^{n}"
                r"\xrightarrow{E}\pi_i^{n+1}$ は完全.")
    assert expected in reference
    assert "Proposition 4.2 により, EHP の列" not in reference
    assert "は完全である" not in reference
    assert f"[R{refs[0].number}]を用いて次の完全列を考える." in proof
    assert len(project_exactness_chains(model)) == 1


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3"))
def test_general_diagonal_stays_in_reference_only(cases, name):
    _, model, text = cases[name]
    reference, proof = sections(text)
    assert r"\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}" in reference
    assert r"\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}" not in proof
    assert r"\pi_{1}^{1}" in proof if name == "pi3_2" else r"\pi_{5}^{5}" in proof
    assert len(model.steps) == (18 if name == "pi3_2" else 25)


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3", "pi5_4"))
def test_proof_has_concise_typed_sentences_with_all_used_citations(cases, name):
    _, model, text = cases[name]
    reference, proof = sections(text)
    assert " を得る." not in proof
    assert "が成り立つ." not in proof
    assert "である." not in proof
    assert "導出により," not in proof
    assert proof.rstrip().endswith("□")
    assert {int(x) for x in re.findall(r"\[R(\d+)\]", proof)} == {
        citation.number for citation in model.citations
    }
    assert all(citation.statement_bodies for citation in model.citations)
    assert all(check["present"] for check in assess(name, proof))


def test_pi54_transport_remains_ordered_and_typed(cases):
    _, model, text = cases["pi5_4"]
    reference, proof = sections(text)
    assert proof.index(r"\pi_{4}^{3} = \mathbb{Z}/2") < proof.index("(n,m,k)=(3,4,1)")
    assert proof.index("(n,m,k)=(3,4,1)") < proof.index(r"E(\eta_{3})=\eta_{4}")
    assert r"\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}" in proof
    assert len(model.steps) == 10


def test_pi43_review_gate_requires_general_schema_in_reference_not_proof():
    from phase168_r3_39f_frozen_comparison.audit import assess
    minimum = (r"完全性より, $E: \pi_{3}^{2}\to\pi_{4}^{3}$ は全射." + "\n"
               + r"完全性より, $\ker E=\mathbb{Z}\{2\eta_{2}\}$." + "\n"
               + r"準同型定理より $\pi_{4}^{3}\cong\pi_{3}^{2}/\mathbb{Z}\{2\eta_{2}\}$." + "\n")
    checks = {item["key"]: item["present"] for item in assess("pi4_3", minimum)}
    assert checks["diagonal_general_only_in_reference"]
    redundant = minimum + r"$\pi_n^n=\mathbb{Z}\{\iota_n\}$."
    checks_redundant = {item["key"]: item["present"] for item in assess("pi4_3", redundant)}
    assert not checks_redundant["diagonal_general_only_in_reference"]


def test_eta_definition_registry_has_only_printed_section_locator(tmp_path):
    source = tmp_path / "eta_definition.tex"
    source.write_text(r"\(n\ge2\) に対し, \eta_n=E^{\,n-2}\eta_2", encoding="utf-8")
    bridge = build_cited_eta_family_definition(source)
    registered = bridge.registry.reference(REFERENCE_ID)
    assertion = bridge.registry.assertion(ASSERTION_ID)
    assert registered.reference_id == REFERENCE_ID
    assert registered.locator == "Chapter V, i)"
    assert "The Groups" not in registered.locator
    assert "eta-family notation" not in registered.locator
    assert assertion.reference_id == REFERENCE_ID
    assert len(bridge.proof_links) == 1
    assert bridge.proof_links[0].assertion_id == ASSERTION_ID
    assert bridge.proof_links[0].step.inference_rule.literature_reference.locator == "Chapter V, i)"
