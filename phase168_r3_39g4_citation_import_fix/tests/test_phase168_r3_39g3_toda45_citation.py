"""Focused R3-39G-3 tests: actual Proof Tree, citations, and Web Narrative."""
import re

from phase168_r3_27_typed_statement_projection import (
    toda45_specialization_evidence,
    project_toda45_specialization_citation_numbers,
    typed_sentence,
)
from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
from phase168_r3_39f_frozen_comparison.audit import assess
from toda_rules import Toda45IsomorphismStatement


def test_pi54_toda45_specialization_is_from_existing_given():
    current, model, _ = capture(4, 1)
    _, proof = sections(current)
    iso_steps = [step for step in model.steps
                 if isinstance(step.conclusion, Toda45IsomorphismStatement)
                 and toda45_specialization_evidence(step) is not None]
    assert len(iso_steps) == 1
    source, binding_pairs = toda45_specialization_evidence(iso_steps[0])
    assert dict(binding_pairs) == {"k": 1, "m": 4, "n": 3}
    assert source in model.steps
    assert r"(n,m,k)=(3,4,1)" in proof
    assert r"E: \pi_{4}^{3}\to \pi_{5}^{4}" in proof


def test_pi54_citation_is_from_the_exact_source_step():
    current, model, _ = capture(4, 1)
    _, proof = sections(current)
    iso_step = next(step for step in model.steps
                    if isinstance(step.conclusion, Toda45IsomorphismStatement)
                    and toda45_specialization_evidence(step) is not None)
    source, _ = toda45_specialization_evidence(iso_step)
    linked_numbers = {
        number
        for index, candidate in enumerate(model.steps)
        if candidate == source
        for number in model.step_citation_numbers[index]
    }
    assert linked_numbers
    assert all(1 <= number <= len(model.citations) for number in linked_numbers)
    assert any(
        (citation.reference.locator or citation.reference.label) == "(4.5)"
        and citation.number in linked_numbers
        for citation in model.citations
    )
    line = next(line for line in proof.splitlines() if "(n,m,k)=(3,4,1)" in line)
    assert "適用すると" in line
    assert any(f"[R{number}]" in line for number in linked_numbers)
    assert re.search(r"\[R\d+\].{0,100}適用", line)


def test_specialization_prose_requires_actual_proof_evidence():
    current, model, _ = capture(4, 1)
    concrete = next(step.conclusion for step in model.steps
                    if isinstance(step.conclusion, Toda45IsomorphismStatement)
                    and type(step.conclusion.map.exponent) is int)
    assert toda45_specialization_evidence(None) is None
    generic_sentence = typed_sentence(concrete, None)
    assert generic_sentence is not None
    assert "(n,m,k)=" not in generic_sentence


def test_full_frozen_explanation_checklist_is_satisfied():
    for name, n, k in (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1)):
        current, _, _ = capture(n, k)
        reference, proof = sections(current)
        missing = [check["key"] for check in assess(name, proof) if not check["present"]]
        assert not missing, f"{name}: missing {missing}"
        assert reference.strip()


def test_toda45_citation_projection_returns_existing_source_numbers():
    current, model, _ = capture(4, 1)
    _, proof = sections(current)
    index = next(
        i for i, step in enumerate(model.steps)
        if isinstance(step.conclusion, Toda45IsomorphismStatement)
        and toda45_specialization_evidence(step) is not None
    )
    source, _ = toda45_specialization_evidence(model.steps[index])
    expected = tuple(dict.fromkeys(
        number
        for i, step in enumerate(model.steps)
        if step == source
        for number in model.step_citation_numbers[i]
    ))
    assert expected
    actual = project_toda45_specialization_citation_numbers(model, index)
    assert actual == expected
    assert any(f"[R{number}]" in proof for number in actual)
