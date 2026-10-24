"""Phase 168 R3-41P6: exactness prose depends on typed evidence, not names."""
from __future__ import annotations

import re
import inspect
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_38_frozen_fulltext_audit import audit as frozen
from phase168_r3_39f_frozen_comparison.audit import assess
from proof import InferenceRule, ProofRule, ProofStep

PACKAGE = Path(__file__).resolve().parents[1]
CASES = (
    ("pi3_2", 2, 1, 18, 4),
    ("pi4_3", 3, 1, 25, 4),
    ("pi5_4", 4, 1, 10, 3),
)


def _sample_mapping():
    return TodaSuspensionMap(TodaPrimaryGroup(4, 3), TodaPrimaryGroup(5, 4))


@pytest.mark.parametrize("name,n,k,step_total,source_total", CASES)
def test_three_group_public_fulltext_and_provenance_unchanged(name, n, k, step_total, source_total):
    rendered, model, view = frozen.capture(n, k)
    assert rendered == (PACKAGE / "baselines" / f"{name}_current.md").read_text(encoding="utf-8")
    assert len(model.steps) == step_total
    assert len(model.citations) == source_total
    reference, proof = frozen.sections(rendered)
    assert all(c.statement_bodies for c in model.citations)
    assert {int(n) for n in re.findall(r"\[R(\d+)\]", proof)} == {c.number for c in model.citations}
    assert all(row["present"] for row in assess(name, proof))
    assert proof.rstrip().endswith("□")
    for citation in model.citations:
        for index in citation.step_indices:
            assert citation.number in model.step_citation_numbers[index]
    for index, numbers in enumerate(model.step_citation_numbers):
        for number in numbers:
            assert index in next(c.step_indices for c in model.citations if c.number == number)


@pytest.mark.parametrize("rule_name", (
    "exactness-looking name without a typed witness",
    "ordinary unrelated inference",
))
def test_no_exactness_claim_from_inference_rule_name_alone(rule_name):
    injection = MapInjective(_sample_mapping())
    unrelated = ProofStep(
        conclusion="unrelated assertion", premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name=rule_name),
    )
    step = ProofStep(
        conclusion=injection, premises=(unrelated,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="generic injectivity inference"),
    )
    sentence = typed_sentence(injection, step)
    assert sentence is not None
    assert "完全性より" not in sentence
    assert "は単射" in sentence


def test_typed_exactness_premise_preserves_explanation_without_rule_name():
    injection = MapInjective(_sample_mapping())
    exactness = ProofStep(
        conclusion=EHPImageEqualsKernelStatement(window=None),
        premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="renamed typed evidence"),
    )
    step = ProofStep(
        conclusion=injection, premises=(exactness,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="another unrelated name"),
    )
    sentence = typed_sentence(injection, step)
    assert sentence is not None
    assert sentence.startswith("完全性より")


def test_indirect_typed_exactness_premise_preserves_explanation():
    injection = MapInjective(_sample_mapping())
    exactness = ProofStep(
        conclusion=EHPImageEqualsKernelStatement(window=None),
        premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="no string gate"),
    )
    intermediate = ProofStep(
        conclusion="intermediate", premises=(exactness,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="unrelated"),
    )
    step = ProofStep(conclusion=injection, premises=(intermediate,), rule=ProofRule.INFERENCE)
    assert typed_sentence(injection, step).startswith("完全性より")


def test_typed_sentence_contains_no_rule_name_exactness_substring():
    source = inspect.getsource(typed_sentence)
    assert '"exact" in str(getattr(' not in source
    assert "isinstance(p.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement))" in source
