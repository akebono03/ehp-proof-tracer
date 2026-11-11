"""R63 targeted sentence proof-witness binding and negative tests."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r63_sentence_witness_audit.audit import (
    PINS, certify_targeted_line, displayed_line, git_blob_sha,
    given_witness_indices, source_guard, unique_step_index,
    verified_ancestor_indices,
)


def fixture_model():
    from proof import ProofRule
    given = SimpleNamespace(conclusion="source", rule=ProofRule.GIVEN, premises=())
    inferred = SimpleNamespace(conclusion="inferred", rule=ProofRule.INFERENCE,
                               premises=(given,))
    model = SimpleNamespace(
        steps=(given, inferred),
        step_citation_numbers=((1,), ()),
        citations=(SimpleNamespace(number=1),),
    )
    return model


def test_source_guard_pins_reviewed_code() -> None:
    root = Path(__file__).resolve().parents[2]
    assert len(PINS) == 7
    assert source_guard(root) == tuple(PINS)


def test_unique_step_index_accepts_only_one_target() -> None:
    model = fixture_model()
    assert unique_step_index(model, lambda s: s.conclusion == "source", frozenset({0, 1})) == 0
    with pytest.raises(RuntimeError):
        unique_step_index(model, lambda s: True, frozenset({0, 1}))
    with pytest.raises(RuntimeError):
        unique_step_index(model, lambda s: False, frozenset({0, 1}))


def test_verified_ancestry_and_exact_given_source() -> None:
    model = fixture_model()
    assert verified_ancestor_indices(model, 1) == frozenset({0, 1})
    assert given_witness_indices(model, 1, 1) == (0,)
    with pytest.raises(RuntimeError):
        given_witness_indices(model, 1, 2)


def test_missing_or_ambiguous_premise_rejected() -> None:
    from proof import ProofRule
    model = fixture_model()
    detached = SimpleNamespace(conclusion="unknown", rule=ProofRule.GIVEN, premises=())
    altered = SimpleNamespace(conclusion="consequence", rule=ProofRule.INFERENCE,
                              premises=(detached,))
    incomplete = SimpleNamespace(steps=(model.steps[0], altered))
    with pytest.raises(RuntimeError):
        verified_ancestor_indices(incomplete, 1)
    with pytest.raises(ValueError):
        verified_ancestor_indices(model, 5)


def test_rendered_sentence_requires_exact_ref_prefix_and_formula() -> None:
    markdown = "**[R1] Example.**\n\n[R1]より, $H(\\Delta(x))=y$.\n"
    line = displayed_line(markdown, 1, ("H(", r"\Delta("))
    assert "[R1]より" in line
    with pytest.raises(RuntimeError):
        displayed_line(markdown, 1, ("全射",))
    with pytest.raises(RuntimeError):
        displayed_line(markdown, 2, ("H(",))


def test_negative_attribution_not_in_given_ancestry() -> None:
    model = fixture_model()
    markdown = "[R1]より, $H(x)=y$.\n"
    result = certify_targeted_line(model, markdown, 1, 1, ("H(",))
    assert result["given_witness_indices"] == [0]
    with pytest.raises(RuntimeError):
        certify_targeted_line(model, markdown, 1, 1, ("not the same formula",))


def test_refuses_untrusted_line_inputs() -> None:
    with pytest.raises(TypeError):
        displayed_line(None, 1, ("x",))
    with pytest.raises(ValueError):
        displayed_line("[R1]より", 0, ("x",))
    with pytest.raises(ValueError):
        displayed_line("[R1]より", 1, ())
    with pytest.raises(ValueError):
        displayed_line("[R1]より", 1, ("",))


def test_source_guard_rejects_tampered_blob(tmp_path: Path) -> None:
    relative = next(iter(PINS))
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("tamper", encoding="utf-8")
    with pytest.raises(RuntimeError):
        source_guard(tmp_path)


def test_known_git_blob_fixture() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"


def test_rejects_number_owned_only_by_unrelated_given() -> None:
    from proof import ProofRule
    relevant = SimpleNamespace(conclusion="relevant", rule=ProofRule.GIVEN, premises=())
    unrelated = SimpleNamespace(conclusion="unrelated", rule=ProofRule.GIVEN, premises=())
    derived = SimpleNamespace(conclusion="derived", rule=ProofRule.INFERENCE,
                              premises=(relevant,))
    model = SimpleNamespace(steps=(relevant, unrelated, derived),
                            step_citation_numbers=((), (1,), ()),
                            citations=(SimpleNamespace(number=1),))
    with pytest.raises(RuntimeError, match="R63_CITATION_NOT_IN_GIVEN_ANCESTRY"):
        certify_targeted_line(model, "[R1]より, $H(x)=y$.", 2, 1, ("H(",))
