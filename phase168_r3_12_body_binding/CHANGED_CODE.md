# Phase 168 R3-12 — complete code

New module is placed in the repository root. `build_narrative_body_lines` is added after `NarrativeBodyLine`. The renderer replaces the entire existing function, keeping its public signature. Test functions are added in the new test file. No old imports are removed elsewhere.

## New module (full)
```python
"""Validated, proof-step-indexed narrative body projection.

This module never infers citations from mathematical text or rule names.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from proof import ProofRule
from web_group_proof_common import _group_proof_statement_latex


@dataclass(frozen=True)
class NarrativeBodyLine:
    step_index: int
    statement_latex: str
    citation_numbers: tuple[int, ...]
    role: str


def build_narrative_body_lines(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> tuple[NarrativeBodyLine, ...]:
    """Bind renderable conclusions to their exact Proof Tree citation indices.

    Unrenderable conclusions are not replaced with guessed prose. Citation
    membership is validated in both directions; a malformed model fails closed.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if model.steps != result.proven_steps:
        raise ValueError("model steps must match the searched result")
    if len(model.step_citation_numbers) != len(model.steps):
        raise ValueError("step citation mapping has the wrong length")
    if result.status is ProofSearchStatus.COMPLETE and model.root_index is None:
        raise ValueError("complete result requires a root step")
    if model.root_index is not None and not 0 <= model.root_index < len(model.steps):
        raise ValueError("root step index is invalid")

    known = {citation.number: citation for citation in model.citations}
    if len(known) != len(model.citations) or set(known) != set(range(1, len(known) + 1)):
        raise ValueError("citation numbers must be unique and contiguous")
    for number, citation in known.items():
        for index in citation.step_indices:
            if not 0 <= index < len(model.steps):
                raise ValueError("citation refers to a nonexistent proof step")
            if number not in model.step_citation_numbers[index]:
                raise ValueError("citation and step map disagree")

    lines = []
    for index, step in enumerate(model.steps):
        numbers = model.step_citation_numbers[index]
        if len(set(numbers)) != len(numbers):
            raise ValueError("a proof step contains duplicate citation numbers")
        for number in numbers:
            if number not in known or index not in known[number].step_indices:
                raise ValueError("step cites a missing or unrelated source")
        latex, fallback_type = _group_proof_statement_latex(step.conclusion)
        if latex is None or fallback_type is not None:
            continue
        role = "given" if step.rule is ProofRule.GIVEN else (
            "root" if index == model.root_index else "inference"
        )
        lines.append(NarrativeBodyLine(index, latex, numbers, role))
    return tuple(lines)

```

## Updated renderer (full)
```python
"""Render an explicitly supplied Proof Narrative Model without source inference."""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_12_body_binding import build_narrative_body_lines


def render_model_backed_narrative_markdown(
    result: PartialProofResult, model: ProofNarrativeModel,
) -> str:
    """Render only used steps and citations already selected by the model.

    This is an opt-in transitional boundary. It does not attempt to reproduce
    the established long-form mathematical argument or infer references.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    body_lines = build_narrative_body_lines(result, model)

    lines = ["使用する結果", ""]
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        lines.append(f"**[R{citation.number}] {locator}.**")
        lines.append("")
    lines.extend(("証明", ""))
    for body_line in body_lines:
        tags = ", ".join(f"[R{number}]" for number in body_line.citation_numbers)
        if body_line.role == "given":
            prefix = f"{tags}より, " if tags else "前提として, "
        elif body_line.role == "root":
            prefix = f"{tags}を用いて, " if tags else "以上より, "
        else:
            prefix = f"{tags}を用いて, " if tags else "導出により, "
        lines.append(f"{prefix}${body_line.statement_latex}$ を得る.")
        lines.append("")
    if result.status is ProofSearchStatus.COMPLETE:
        lines.append("□")
    return "\n".join(lines).rstrip() + "\n"

```

## Tests (full)
```python
from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_12_body_binding import build_narrative_body_lines
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def _case():
    rule = InferenceRule(name="source", literature_reference=LiteratureReference(label="Toda (5.2)", locator="(5.2)"))
    step = ProofStep(conclusion="root", premises=(), rule=ProofRule.INFERENCE, inference_rule=rule)
    result = make_partial_proof_result(n=2, k=2, status=ProofSearchStatus.COMPLETE,
                                       proven_steps=(step,), conclusion="root")
    return result, build_proof_narrative_model(result)


def test_citation_numbers_are_bound_to_actual_steps():
    result, model = _case()
    assert model.step_citation_numbers == ((1,),)
    assert model.citations[0].step_indices == (0,)
    assert build_narrative_body_lines(result, model) == ()  # no fabricated repr for root


def test_unknown_citation_number_is_rejected():
    result, model = _case()
    wrong = replace(model, step_citation_numbers=((2,),))
    with pytest.raises(ValueError, match="missing or unrelated"):
        build_narrative_body_lines(result, wrong)


def test_reverse_citation_mapping_is_checked():
    result, model = _case()
    wrong = replace(model, step_citation_numbers=((),))
    with pytest.raises(ValueError, match="disagree"):
        build_narrative_body_lines(result, wrong)


def test_mismatched_search_result_is_rejected():
    result, model = _case()
    other = replace(result, proven_steps=(ProofStep(conclusion="root", premises=(), rule=ProofRule.GIVEN),))
    with pytest.raises(ValueError, match="must match"):
        build_narrative_body_lines(other, model)

```
