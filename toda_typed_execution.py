"""Execute a selected, fully matched inference from proven premises only."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from proof import InferenceMatch, ProofRule, ProofStep, apply_inference_match
from toda_typed_applicability import TypedApplicableRule, find_typed_applicable_rules


class TypedExecutionOutcome(str, Enum):
    NONE = "none"
    AMBIGUOUS = "ambiguous"
    EXECUTED = "executed"


@dataclass(frozen=True)
class TypedExecutionResult:
    status: TypedExecutionOutcome
    matches: tuple[InferenceMatch, ...]
    selected_candidate_number: int | None = None
    proof_step: ProofStep | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, TypedExecutionOutcome):
            raise TypeError("status must be TypedExecutionOutcome")
        if not isinstance(self.matches, tuple) or any(
            not isinstance(match, InferenceMatch) for match in self.matches
        ):
            raise TypeError("matches must be tuple[InferenceMatch, ...]")
        if self.status is TypedExecutionOutcome.EXECUTED:
            if self.proof_step is None or self.selected_candidate_number is None:
                raise ValueError("executed result requires selected proof")
            if self.proof_step.rule is not ProofRule.INFERENCE:
                raise ValueError("executed result must be an inference ProofStep")
        elif self.proof_step is not None or self.selected_candidate_number is not None:
            raise ValueError("unexecuted result must not claim a proof or selection")


def execute_typed_applicable_rules(
    proven_steps: Iterable[ProofStep],
    *,
    candidate_number: int | None = None,
    rules=None,
) -> TypedExecutionResult:
    """Apply only an exact selected inference match; never fabricate premises."""
    if candidate_number is not None and (
        isinstance(candidate_number, bool)
        or not isinstance(candidate_number, int)
        or candidate_number < 1
    ):
        raise ValueError("candidate_number must be a positive integer")
    applicable = find_typed_applicable_rules(proven_steps, rules=rules)
    matches = tuple(match for entry in applicable for match in entry.matches)
    if not matches:
        if candidate_number is not None:
            raise ValueError("no applicable inference candidate")
        return TypedExecutionResult(TypedExecutionOutcome.NONE, matches)
    if candidate_number is None and len(matches) > 1:
        return TypedExecutionResult(TypedExecutionOutcome.AMBIGUOUS, matches)
    selected = candidate_number or 1
    if selected > len(matches):
        raise ValueError("candidate_number exceeds applicable candidates")
    match = matches[selected - 1]
    step = apply_inference_match(match)
    if not isinstance(step, ProofStep) or tuple(step.premises) != tuple(match.premises):
        raise RuntimeError("inference engine did not preserve matched premises")
    return TypedExecutionResult(
        TypedExecutionOutcome.EXECUTED,
        matches,
        selected_candidate_number=selected,
        proof_step=step,
    )
