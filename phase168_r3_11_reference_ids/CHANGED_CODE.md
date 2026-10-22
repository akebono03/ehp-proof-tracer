# R3-11 modified complete module and tests

## `phase168_r3_3_proof_narrative_model.py`

```python
"""Proof-tree-backed citation projection; no rendering or search decisions."""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult
from proof import LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import ProofStepLink, UnifiedStatementRegistry


@dataclass(frozen=True)
class NarrativeCitation:
    number: int
    reference: LiteratureReference
    step_indices: tuple[int, ...]
    assertion_ids: tuple[str, ...] = ()
    reference_ids: tuple[str, ...] = ()


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
    reference_ids: list[list[str]] = []
    registry_index: dict[str, int] = {}
    per_step: list[tuple[int, ...]] = []

    for step_index, step in enumerate(steps):
        linked: list[tuple[LiteratureReference, str | None, str | None]] = []
        if registry is not None:
            for link in proof_links:
                if link.step is None or link.step != step:
                    continue
                assertion = registry.assertion(link.assertion_id)
                entry = registry.reference(assertion.reference_id)
                linked.append((LiteratureReference(
                    label=entry.locator, locator=entry.locator,
                ), assertion.assertion_id, assertion.reference_id))

        located = list(linked)
        inference_rule = step.inference_rule
        if inference_rule is not None and inference_rule.literature_reference is not None:
            rule_reference = inference_rule.literature_reference
            rule_locator = rule_reference.locator or rule_reference.label
            # A registry heading may include a descriptive title following the
            # short printed heading attached to the very same GIVEN. Only that
            # heading/title shape is an alias; a numbered subsection or a
            # genuinely different locator remains a distinct citation.
            def same_source_heading(registered: LiteratureReference) -> bool:
                registered_locator = registered.locator or registered.label
                if registered_locator == rule_locator:
                    return True
                if step.rule is not ProofRule.GIVEN:
                    return False
                prefix = rule_locator + " "
                if not registered_locator.startswith(prefix):
                    return False
                suffix = registered_locator[len(prefix):]
                return suffix.startswith("The ") and len(suffix) > 4

            if not any(same_source_heading(reference) for reference, _, _ in linked):
                located.append((rule_reference, None, None))

        numbers: list[int] = []
        for reference, assertion_id, reference_id in located:
            locator = reference.locator or reference.label
            # The registered identity takes precedence over display labels.
            # Printed locator remains the compatibility fallback for independent
            # registry copies and inference rules without a registry entry.
            if reference_id is not None and reference_id in registry_index:
                ref_index = registry_index[reference_id]
            elif locator in locators:
                ref_index = locators.index(locator)
            else:
                ref_index = len(references)
                locators.append(locator)
                references.append(reference)
                associations.append([])
                assertion_ids.append([])
                reference_ids.append([])
            if reference_id is not None:
                registry_index[reference_id] = ref_index
                if reference_id not in reference_ids[ref_index]:
                    reference_ids[ref_index].append(reference_id)
                # Prefer the richer registered locator over an earlier
                # inference-only display entry for the same printed source.
                if references[ref_index].locator != locator:
                    references[ref_index] = reference
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
            reference_ids=tuple(reference_ids[i]),
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

## New tests

```python
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry


def test_multiple_assertions_share_reference_id():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(reference_id='toda:51', kind=ReferenceKind.EQUATION, locator='(5.1)'))
    links = []
    steps = []
    for key in ('a', 'b'):
        registry.add_assertion(AssertionEntry(assertion_id=key, reference_id='toda:51', kind=AssertionKind.STATEMENT, content=key))
        step = ProofStep(conclusion=key, premises=(), rule=ProofRule.GIVEN)
        steps.append(step)
        links.append(ProofStepLink(assertion_id=key, step=step))
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.COMPLETE, proven_steps=tuple(steps), conclusion='b')
    model = build_proof_narrative_model(result, registry=registry, proof_links=tuple(links))
    assert len(model.citations) == 1
    assert model.citations[0].reference_ids == ('toda:51',)
    assert model.citations[0].assertion_ids == ('a', 'b')
    assert model.citations[0].step_indices == (0, 1)


def test_inference_only_reference_has_no_registry_id():
    step = ProofStep(conclusion='goal', premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name='transport', literature_reference=LiteratureReference(label='Toda (5.2)', locator='(5.2)')))
    result = make_partial_proof_result(n=2, k=2, status=ProofSearchStatus.COMPLETE, proven_steps=(step,), conclusion='goal')
    model = build_proof_narrative_model(result)
    assert model.citations[0].reference_ids == ()
    assert model.citations[0].reference.locator == '(5.2)'


def test_distinct_registered_sources_remain_distinct():
    registry = UnifiedStatementRegistry()
    steps = []
    links = []
    for key, locator in (('eq', '(5.1)'), ('prop', 'Proposition 5.1')):
        registry.add_reference(LiteratureEntry(reference_id=key, kind=ReferenceKind.PROPOSITION, locator=locator))
        registry.add_assertion(AssertionEntry(assertion_id='a:'+key, reference_id=key, kind=AssertionKind.STATEMENT, content=key))
        step = ProofStep(conclusion=key, premises=(), rule=ProofRule.GIVEN)
        steps.append(step)
        links.append(ProofStepLink(assertion_id='a:'+key, step=step))
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.COMPLETE, proven_steps=tuple(steps), conclusion='prop')
    model = build_proof_narrative_model(result, registry=registry, proof_links=tuple(links))
    assert [c.reference_ids for c in model.citations] == [('eq',), ('prop',)]


def test_rule_and_registry_matching_locator_do_not_duplicate():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(reference_id='registered', kind=ReferenceKind.PROPOSITION, locator='Proposition 5.1'))
    registry.add_assertion(AssertionEntry(assertion_id='a', reference_id='registered', kind=AssertionKind.STATEMENT, content='x'))
    step = ProofStep(conclusion='x', premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(name='given', literature_reference=LiteratureReference(label='Toda Proposition 5.1', locator='Proposition 5.1')))
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.COMPLETE, proven_steps=(step,), conclusion='x')
    model = build_proof_narrative_model(result, registry=registry, proof_links=(ProofStepLink(assertion_id='a', step=step),))
    assert len(model.citations) == 1
    assert model.citations[0].reference_ids == ('registered',)

```
