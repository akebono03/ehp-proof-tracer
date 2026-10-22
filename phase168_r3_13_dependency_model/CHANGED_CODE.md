# 変更対象

新規: `phase168_r3_13_dependency_model.py` （リポジトリ直下）、`tests/test_phase168_r3_13_dependency_model.py`（ZIP 内）。既存の Search / Renderer / Web は変更しません。

## 追加するクラス・関数の全文

```python
"""Proof-step dependency projection for the shared narrative pipeline.

This is a structural model, not a new mathematical proof generator.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class NarrativeInference:
    step_index: int
    premise_indices: tuple[int, ...]
    unresolved_premises: tuple[object, ...]
    citation_numbers: tuple[int, ...]
    rule: ProofRule
    is_root: bool


def build_narrative_inferences(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> tuple[NarrativeInference, ...]:
    """Index each inference against proven antecedents without inventing edges.

    ``ProofStep.premises`` may contain statements or ProofStep instances.
    Only exact, earlier unique conclusions count as available premises.
    Ambiguous, absent, or forward dependencies are preserved as unresolved.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if model.steps != result.proven_steps:
        raise ValueError("model steps must match the searched result")
    if len(model.step_citation_numbers) != len(model.steps):
        raise ValueError("step citation map length mismatch")
    known = {citation.number: citation for citation in model.citations}
    if len(known) != len(model.citations):
        raise ValueError("duplicate citation numbers")
    nodes = []
    for index, step in enumerate(model.steps):
        indices = []
        unresolved = []
        for premise in step.premises:
            statement = premise.conclusion if isinstance(premise, ProofStep) else premise
            matches = [
                j for j, earlier in enumerate(model.steps[:index])
                if earlier.conclusion == statement
            ]
            if len(matches) != 1:
                unresolved.append(statement)
            else:
                indices.append(matches[0])
        numbers = model.step_citation_numbers[index]
        if any(
            number not in known or index not in known[number].step_indices
            for number in numbers
        ):
            raise ValueError("step cites a missing or unrelated source")
        nodes.append(NarrativeInference(
            step_index=index,
            premise_indices=tuple(indices),
            unresolved_premises=tuple(unresolved),
            citation_numbers=numbers,
            rule=step.rule,
            is_root=index == model.root_index,
        ))
    return tuple(nodes)
```

## テストの import と関数全文

```python
from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_13_dependency_model import build_narrative_inferences
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def _case():
    source = ProofStep("A", (), ProofRule.GIVEN)
    rule = InferenceRule(name="derived", literature_reference=LiteratureReference(
        label="Toda (5.2)", locator="(5.2)"
    ))
    derived = ProofStep("B", ("A",), ProofRule.INFERENCE, inference_rule=rule)
    result = make_partial_proof_result(
        n=2, k=2, status=ProofSearchStatus.COMPLETE,
        proven_steps=(source, derived), conclusion="B",
    )
    return result, build_proof_narrative_model(result)


def test_exact_prior_premise_dependency_and_source():
    result, model = _case()
    nodes = build_narrative_inferences(result, model)
    assert nodes[1].premise_indices == (0,)
    assert nodes[1].unresolved_premises == ()
    assert nodes[1].citation_numbers == (1,)
    assert nodes[1].is_root


def test_unresolved_premise_is_not_invented():
    result, model = _case()
    wrong = replace(result.proven_steps[1], premises=("UNKNOWN",))
    changed = replace(result, proven_steps=(result.proven_steps[0], wrong))
    changed_model = build_proof_narrative_model(changed)
    nodes = build_narrative_inferences(changed, changed_model)
    assert nodes[1].premise_indices == ()
    assert nodes[1].unresolved_premises == ("UNKNOWN",)


def test_forward_dependency_is_not_accepted():
    result, model = _case()
    first = replace(result.proven_steps[0], premises=("B",))
    changed = replace(result, proven_steps=(first, result.proven_steps[1]))
    nodes = build_narrative_inferences(changed, build_proof_narrative_model(changed))
    assert nodes[0].unresolved_premises == ("B",)


def test_mismatch_rejected():
    result, model = _case()
    other = replace(result, proven_steps=tuple(reversed(result.proven_steps)))
    with pytest.raises(ValueError, match="must match"):
        build_narrative_inferences(other, model)
```
