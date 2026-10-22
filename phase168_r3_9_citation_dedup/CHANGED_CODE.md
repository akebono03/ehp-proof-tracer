# R3-9 変更コード全文

対象: `phase168_r3_3_proof_narrative_model.py` の `build_proof_narrative_model`。import の変更なし。既存クラス変更なし。テストは新規 `tests/test_phase168_r3_9_citation_dedup.py`。

## 置換対象モジュール全文

```python
"""Proof-tree-backed citation projection; no rendering or search decisions."""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult
from proof import LiteratureReference, ProofStep
from unified_statement_registry import ProofStepLink, UnifiedStatementRegistry


@dataclass(frozen=True)
class NarrativeCitation:
    number: int
    reference: LiteratureReference
    step_indices: tuple[int, ...]
    assertion_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProofNarrativeModel:
    steps: tuple[ProofStep, ...]
    citations: tuple[NarrativeCitation, ...]
    step_citation_numbers: tuple[tuple[int, ...], ...]
    root_index: int | None


def build_proof_narrative_model(
    result: PartialProofResult,
    *,
    registry: UnifiedStatementRegistry | None = None,
    proof_links: tuple[ProofStepLink, ...] = (),
) -> ProofNarrativeModel:
    """Project only explicit proof-step and registered-link citations.

    Matching a link requires an exact ProofStep value; merely matching a
    conclusion or a display string is not sufficient. Root inference citations
    remain eligible. Neither a root conclusion nor an unused registry assertion
    becomes a premise through this projection.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if registry is not None and not isinstance(registry, UnifiedStatementRegistry):
        raise TypeError("registry must be UnifiedStatementRegistry or None")
    if not isinstance(proof_links, tuple) or not all(
        isinstance(link, ProofStepLink) for link in proof_links
    ):
        raise TypeError("proof_links must be a tuple of ProofStepLink")
    if proof_links and registry is None:
        raise ValueError("registry is required for proof_links")

    steps = result.proven_steps
    root_index = next(
        (i for i in range(len(steps) - 1, -1, -1)
         if result.conclusion is not None and steps[i].conclusion == result.conclusion),
        None,
    )
    # Locator is the printed source position. Labels are presentation metadata,
    # not independent source identities. Exact matching avoids conflating nearby
    # propositions or components with different locators.
    references: list[LiteratureReference] = []
    locators: list[str] = []
    associations: list[list[int]] = []
    assertion_ids: list[list[str]] = []
    per_step: list[tuple[int, ...]] = []

    for step_index, step in enumerate(steps):
        linked: list[tuple[LiteratureReference, str | None]] = []
        if registry is not None:
            for link in proof_links:
                if link.step is None or link.step != step:
                    continue
                assertion = registry.assertion(link.assertion_id)
                entry = registry.reference(assertion.reference_id)
                linked.append((LiteratureReference(
                    label=entry.locator, locator=entry.locator,
                ), assertion.assertion_id))

        located = list(linked)
        inference_rule = step.inference_rule
        if inference_rule is not None and inference_rule.literature_reference is not None:
            rule_reference = inference_rule.literature_reference
            rule_locator = rule_reference.locator or rule_reference.label
            if not any(
                (reference.locator or reference.label) == rule_locator
                for reference, _ in linked
            ):
                located.append((rule_reference, None))

        numbers: list[int] = []
        for reference, assertion_id in located:
            locator = reference.locator or reference.label
            try:
                ref_index = locators.index(locator)
            except ValueError:
                ref_index = len(references)
                locators.append(locator)
                references.append(reference)
                associations.append([])
                assertion_ids.append([])
            number = ref_index + 1
            if step_index not in associations[ref_index]:
                associations[ref_index].append(step_index)
            if assertion_id is not None and assertion_id not in assertion_ids[ref_index]:
                assertion_ids[ref_index].append(assertion_id)
            if number not in numbers:
                numbers.append(number)
        per_step.append(tuple(numbers))

    citations = tuple(
        NarrativeCitation(
            number=i + 1,
            reference=reference,
            step_indices=tuple(associations[i]),
            assertion_ids=tuple(assertion_ids[i]),
        )
        for i, reference in enumerate(references)
    )
    return ProofNarrativeModel(
        steps=steps,
        citations=citations,
        step_citation_numbers=tuple(per_step),
        root_index=root_index,
    )

```

## テスト全文

```python
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _make_model(link_locator, rule_locator, second_rule_locator=None):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="ref", kind=ReferenceKind.PROPOSITION,
        locator=link_locator,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="assertion", reference_id="ref",
        kind=AssertionKind.STATEMENT, content="fact",
    ))
    given = ProofStep(
        conclusion="fact", premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="documented given", literature_reference=LiteratureReference(
                label="Toda " + rule_locator, locator=rule_locator,
            ),
        ),
    )
    steps = (given,)
    if second_rule_locator is not None:
        root = ProofStep(
            conclusion="result", premises=(given,), rule=ProofRule.INFERENCE,
            inference_rule=InferenceRule(
                name="derived", literature_reference=LiteratureReference(
                    label="Toda " + second_rule_locator,
                    locator=second_rule_locator,
                ),
            ),
        )
        steps = (given, root)
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=steps, conclusion=steps[-1].conclusion,
    )
    return build_proof_narrative_model(
        result, registry=registry,
        proof_links=(ProofStepLink(assertion_id="assertion", step=given),),
    )


def test_same_step_link_and_rule_is_one_citation():
    model = _make_model("Proposition 5.1", "Proposition 5.1")
    assert len(model.citations) == 1
    assert model.citations[0].assertion_ids == ("assertion",)
    assert model.step_citation_numbers == ((1,),)


def test_distinct_source_on_same_step_is_not_removed():
    model = _make_model("Proposition 5.1", "(5.1)")
    assert [c.reference.locator for c in model.citations] == ["Proposition 5.1", "(5.1)"]
    assert model.step_citation_numbers == ((1, 2),)


def test_root_rule_provenance_survives():
    model = _make_model("Proposition 5.1", "Proposition 5.1", "(5.2)")
    assert [c.reference.locator for c in model.citations] == ["Proposition 5.1", "(5.2)"]
    assert model.step_citation_numbers == ((1,), (2,))


def test_same_locator_different_labels_dedupes_across_steps():
    first = ProofStep(conclusion="a", premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(name="one", literature_reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)")))
    second = ProofStep(conclusion="b", premises=(first,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="two", literature_reference=LiteratureReference(label="(5.1)", locator="(5.1)")))
    result = make_partial_proof_result(n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(first, second), conclusion="b")
    model = build_proof_narrative_model(result)
    assert len(model.citations) == 1
    assert model.citations[0].step_indices == (0, 1)

```
