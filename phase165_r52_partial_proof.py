"""Phase 165 R52: range-independent, fail-closed partial proof presentation.

This module records *observed* proof progress. It does not certify a step or
infer a proof from a goal. Callers must supply their already validated steps.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any

from homotopy_groups import TodaPrimaryGroup
from proof import ProofRule, ProofStep


class ProofSearchStatus(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    SEARCH_FAILED = "search_failed"
    NOT_SEARCHED = "not_searched"


class GroupStructureStatus(str, Enum):
    KNOWN = "known"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class CertifiedAbstractStructure:
    """Verified abstract invariants, separate from a named group conclusion."""
    group: TodaPrimaryGroup
    invariant_summands: tuple[tuple[str, int], ...]
    proof_step: ProofStep

    def __post_init__(self) -> None:
        from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
            TodaProp44AbstractGroupResult,
        )
        if not isinstance(self.group, TodaPrimaryGroup):
            raise TypeError("abstract certificate must have a typed target group")
        expected = TodaProp44AbstractGroupResult(
            self.group, self.invariant_summands,
        )
        if (not isinstance(self.proof_step, ProofStep)
                or self.proof_step.rule is not ProofRule.INFERENCE
                or self.proof_step.conclusion != expected
                or self.proof_step.inference_rule is None
                or not callable(self.proof_step.inference_rule.match_guard)
                or not self.proof_step.inference_rule.match_guard(
                    self.proof_step.premises, (),
                )):
            raise ValueError("abstract certificate has no verified inference root")


@dataclass(frozen=True)
class PartialProofResult:
    target: TodaPrimaryGroup
    status: ProofSearchStatus
    structure_status: GroupStructureStatus = GroupStructureStatus.UNKNOWN
    references: tuple[str, ...] = ()
    proven_steps: tuple[ProofStep, ...] = ()
    open_goals: tuple[Any, ...] = ()
    diagnostics: tuple[str, ...] = ()
    conclusion: Any | None = None
    abstract_structure: CertifiedAbstractStructure | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target, TodaPrimaryGroup):
            raise TypeError("target must be TodaPrimaryGroup")
        if not isinstance(self.status, ProofSearchStatus):
            raise TypeError("status must be ProofSearchStatus")
        if not isinstance(self.structure_status, GroupStructureStatus):
            raise TypeError("structure_status must be GroupStructureStatus")
        for name in ("references", "proven_steps", "open_goals", "diagnostics"):
            if not isinstance(getattr(self, name), tuple):
                raise TypeError(f"{name} must be a tuple")
        if not all(isinstance(s, ProofStep) for s in self.proven_steps):
            raise TypeError("proven_steps must contain only ProofStep")
        if not all(isinstance(s, str) and s for s in self.references + self.diagnostics):
            raise ValueError("references and diagnostics must contain nonempty strings")
        if self.status is ProofSearchStatus.COMPLETE:
            if self.conclusion is None or self.open_goals:
                raise ValueError("complete proof requires conclusion and no open goals")
            if not any(step.conclusion == self.conclusion for step in self.proven_steps):
                raise ValueError("completed conclusion requires a matching proven step")
        elif self.conclusion is not None:
            raise ValueError("incomplete result must not claim a final conclusion")
        if self.abstract_structure is not None:
            if (not isinstance(self.abstract_structure, CertifiedAbstractStructure)
                    or self.abstract_structure.group != self.target
                    or self.status not in (
                        ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED,
                    )
                    or self.conclusion is not None
                    or self.structure_status is GroupStructureStatus.KNOWN):
                raise ValueError(
                    "abstract-only evidence cannot certify a named group"
                )
        if self.status is ProofSearchStatus.NOT_SEARCHED and self.proven_steps:
            raise ValueError("not-searched result cannot contain derived steps")
        if self.status is ProofSearchStatus.SEARCH_FAILED and not self.diagnostics:
            raise ValueError("failed search requires a diagnostic")


def make_partial_proof_result(
    *, n: int, k: int, status: ProofSearchStatus,
    structure_status: GroupStructureStatus = GroupStructureStatus.UNKNOWN,
    references: tuple[str, ...] = (),
    proven_steps: tuple[ProofStep, ...] = (),
    open_goals: tuple[Any, ...] = (),
    diagnostics: tuple[str, ...] = (),
    conclusion: Any | None = None,
) -> PartialProofResult:
    """Build a result for arbitrary nonnegative stem and sphere dimension >=2."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be an integer >= 2")
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError("k must be a nonnegative integer")
    return PartialProofResult(
        target=TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n),
        status=status,
        structure_status=structure_status,
        references=references,
        proven_steps=proven_steps,
        open_goals=open_goals,
        diagnostics=diagnostics,
        conclusion=conclusion,
    )


def render_partial_proof_markdown(result: PartialProofResult) -> str:
    """Route complete results to the restored Narrative; incomplete results to partial."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is ProofSearchStatus.COMPLETE:
        from phase165_r56_presentation_adapter import render_completed_shared_narrative
        return render_completed_shared_narrative(result)
    from toda_group_proof_narrative_renderer import render_toda_partial_proof_narrative_markdown
    return render_toda_partial_proof_narrative_markdown(result)
