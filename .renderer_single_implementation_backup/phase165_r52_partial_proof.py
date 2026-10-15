"""Phase 165 R52: range-independent, fail-closed partial proof presentation.

This module records *observed* proof progress. It does not certify a step or
infer a proof from a goal. Callers must supply their already validated steps.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any

from homotopy_groups import TodaPrimaryGroup
from proof import ProofStep


class ProofSearchStatus(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    SEARCH_FAILED = "search_failed"
    NOT_SEARCHED = "not_searched"


class GroupStructureStatus(str, Enum):
    KNOWN = "known"
    UNKNOWN = "unknown"


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
    """Use the original full Narrative for completed search; retain partial display."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is ProofSearchStatus.COMPLETE:
        from phase165_r56_presentation_adapter import render_completed_shared_narrative
        return render_completed_shared_narrative(result)
    from toda_group_proof_generic_narrative_renderer import (
        render_toda_partial_proof_narrative_markdown,
    )
    return render_toda_partial_proof_narrative_markdown(result)
