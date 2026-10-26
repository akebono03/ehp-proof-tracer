"""Focused proof-backed eta-square and reference rendering regression tests."""
from __future__ import annotations

import re

import pytest

from expression import Composition, eta, nu
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase168_r3_27_typed_statement_projection import element_tex, typed_sentence
from phase169_r3j1_narrative_import_isolation.audit import capture_actual_narrative, split_narrative
from proof import ProofRule


@pytest.fixture(scope="module")
def actual():
    return capture_actual_narrative()


def test_r3k2_composite_eta_square_notation_is_typed():
    assert element_tex(Composition(eta(2), eta(3))) == r"\eta_{2}^{2}"
    assert element_tex(Composition(eta(3), eta(4))) == r"\eta_{3}^{2}"
    assert element_tex(Composition(eta(2), eta(4))) is None
    assert element_tex(Composition(nu(2), nu(5))) is None


def test_r3k2_composite_image_sentence_projects_conclusion_only():
    mapping = TodaSuspensionMap(TodaPrimaryGroup(4, 2), TodaPrimaryGroup(5, 3))
    image = GeneratorImage(
        map=mapping,
        source_generator=Composition(eta(2), eta(3)),
        target_generator=Composition(eta(3), eta(4)),
    )
    assert typed_sentence(image, None) == r"$E(\eta_{2}^{2})=\eta_{3}^{2}$."


def test_r3k2_real_image_is_in_proof_tree_before_root(actual):
    result, model, markdown, view = actual
    images = [(i, step) for i, step in enumerate(model.steps)
              if isinstance(step.conclusion, GeneratorImage)
              and element_tex(step.conclusion.source_generator) == r"\eta_{2}^{2}"
              and element_tex(step.conclusion.target_generator) == r"\eta_{3}^{2}"]
    assert len(images) == 1
    index, image_step = images[0]
    assert index < model.root_index
    assert image_step.rule is ProofRule.INFERENCE
    assert len(image_step.premises) == 2
    assert all(parent.rule is ProofRule.INFERENCE
               and isinstance(parent.conclusion, GeneratorSuspension)
               for parent in image_step.premises)
    assert r"E(\eta_{2}^{2})=\eta_{3}^{2}" in markdown
    assert markdown.index(r"E(\eta_{2}^{2})=\eta_{3}^{2}") < markdown.rindex(
        r"\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}"
    )
    assert result.proven_steps == model.steps
    assert view.key == "generic-complete-proof"


def test_r3k2_reference_metadata_and_proof_citation_integrity(actual):
    result, model, markdown, view = actual
    refs, proof = split_narrative(markdown)
    eta_reference = [item for item in model.citations
                     if (item.reference.locator or item.reference.label) == "Chapter V, i)"]
    assert len(eta_reference) == 1
    number = eta_reference[0].number
    assert f"[R{number}] η 系列の定義（Chapter V, i）" in refs
    assert f"[R{number}]より, $E(\\eta_{{2}}^{{2}})=\\eta_{{3}}^{{2}}$." in proof
    expected = {citation.number for citation in model.citations}
    actual_numbers = {int(item) for item in re.findall(r"\[R(\d+)\]", proof)}
    assert actual_numbers == expected
    assert len(model.citations) == 6
    assert len(model.steps) == 26


def test_r3k2_superseded_eta_steps_do_not_duplicate_main_explanation(actual):
    _, model, markdown, view = actual
    _, proof = split_narrative(markdown)
    assert proof.count(r"E(\eta_{2}^{2})=\eta_{3}^{2}") == 1
    assert r"[R6]より, $E(\eta_{2})=\eta_{3}$." not in proof
    assert r"[R6]より, $E(\eta_{3})=\eta_{4}$." not in proof
    assert r"\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}" in proof
    assert proof.rstrip().endswith("□")
