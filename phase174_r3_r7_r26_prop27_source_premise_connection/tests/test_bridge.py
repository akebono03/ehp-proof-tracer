"""Isolated fixtures are not public or certified Proof Search witnesses."""
from __future__ import annotations

from dataclasses import replace

import pytest

from proof import (
    InferenceRule, LiteratureReference, ProofRule, ProofStep,
    find_inference_match, run_inference_until_stable_with_history,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, Prop27TypedHopfDeltaStatement,
    prop27_typed_specialization_rule, typed_specialization,
)
from phase174_r3_r7_r26_prop27_source_premise_connection.bridge import (
    PROP27_REFERENCE, Prop27SourceEvidence, audited_prop27_source,
    extract_prop27_source, prop27_source_premise_rule,
)
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def source_fixture() -> Prop27SourceEvidence:
    return audited_prop27_source(ROOT)


def synthetic_source_step(evidence, *, cited=True, with_parent=True,
                          proof_rule=ProofRule.INFERENCE):
    reference = PROP27_REFERENCE if cited else LiteratureReference(
        label="wrong", locator="Proposition 5.9",
    )
    rule = InferenceRule(name="test-only hypothetical certified evidence", literature_reference=reference)
    parent = ProofStep(conclusion="test-only external verification", premises=(), rule=ProofRule.INFERENCE)
    return ProofStep(
        conclusion=evidence,
        premises=(parent,) if with_parent else (),
        rule=proof_rule,
        inference_rule=rule,
    )


def test_exact_adopted_source_and_n6():
    evidence = source_fixture()
    assert evidence.only_even_n and evidence.sign_undetermined
    assert len(evidence.theorem_sha256) == 64
    assert typed_specialization(6).source_iota_dimension == 13


def test_windows_newline_same_fingerprint():
    sample = (ROOT / "sources/toda/Toda_02_2.tex").read_text(encoding="utf-8-sig")
    assert extract_prop27_source(sample.replace("\n", "\r\n")) == source_fixture()


@pytest.mark.parametrize("change", [
    (r"\pm\,2", r"+\,2"),
    (r"\iota_{2n-1}", r"\iota_{2n+1}"),
    ("$n$ が偶数のとき", "$n$ が奇数のとき"),
])
def test_mutated_source_rejected(change):
    original = (ROOT / "sources/toda/Toda_02_2.tex").read_text(encoding="utf-8-sig")
    assert change[0] in original
    with pytest.raises(ValueError):
        extract_prop27_source(original.replace(change[0], change[1]))


def test_source_text_is_not_proof():
    assert find_inference_match(prop27_source_premise_rule(source_fixture()), ()) is None


@pytest.mark.parametrize("kwargs", [
    {"cited": False}, {"with_parent": False}, {"proof_rule": ProofRule.GIVEN},
])
def test_unsupported_source_step_rejected(kwargs):
    evidence = source_fixture()
    assert find_inference_match(prop27_source_premise_rule(evidence), (
        synthetic_source_step(evidence, **kwargs),
    )) is None


def test_wrong_hash_rejected():
    evidence = source_fixture()
    fake = replace(evidence, theorem_sha256="a" * 64)
    assert find_inference_match(prop27_source_premise_rule(evidence), (
        synthetic_source_step(fake),
    )) is None


def test_conditional_two_inference_chain_n6_only():
    evidence = source_fixture()
    source_step = synthetic_source_step(evidence)
    first_rule = prop27_source_premise_rule(evidence)
    first = run_inference_until_stable_with_history(first_rule, (source_step,))
    schema_steps = tuple(s for s in first.steps if isinstance(s.conclusion, Prop27GeneralTheoremPremise))
    assert len(schema_steps) == 1
    assert schema_steps[0].rule is ProofRule.INFERENCE
    assert schema_steps[0].premises == (source_step,)
    second = run_inference_until_stable_with_history(
        prop27_typed_specialization_rule(6), schema_steps,
    )
    derived = tuple(s for s in second.steps if isinstance(s.conclusion, Prop27TypedHopfDeltaStatement))
    assert len(derived) == 1
    assert derived[0].conclusion == typed_specialization(6)
    assert derived[0].premises == schema_steps
    assert derived[0].rule is ProofRule.INFERENCE
    assert derived[0].conclusion.sign_undetermined


def test_bridge_never_injects_given():
    rule = prop27_source_premise_rule(source_fixture())
    assert rule.premise_patterns[0].proof_rule is ProofRule.INFERENCE
    assert rule.conclusion_pattern == Prop27GeneralTheoremPremise()
