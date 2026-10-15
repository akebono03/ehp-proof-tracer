"""Shared, evidence-preserving input model for complete and incomplete narratives.

This module never infers facts, changes proof order, or formats Markdown.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from proof import ProofStep
from toda_group_proof_presentation import TodaGroupProofPresentation


@dataclass(frozen=True)
class NarrativeProofModel:
    """A common snapshot of evidence, not a claim of additional proof."""

    target: TodaPrimaryGroup
    status: ProofSearchStatus
    proven_steps: tuple[ProofStep, ...]
    open_goals: tuple[Any, ...]
    references: tuple[str, ...]
    diagnostics: tuple[str, ...]
    conclusion: Any | None
    root_step: ProofStep | None
    source_kind: str
    source: PartialProofResult | TodaGroupProofPresentation

    def __post_init__(self) -> None:
        if not isinstance(self.target, TodaPrimaryGroup):
            raise TypeError("target must be TodaPrimaryGroup")
        if not isinstance(self.status, ProofSearchStatus):
            raise TypeError("status must be ProofSearchStatus")
        if self.source_kind not in ("search_result", "presentation"):
            raise ValueError("unrecognized narrative source kind")
        if not isinstance(self.proven_steps, tuple) or not all(
            isinstance(step, ProofStep) for step in self.proven_steps
        ):
            raise TypeError("proven_steps must be a tuple of ProofStep")
        if not isinstance(self.open_goals, tuple):
            raise TypeError("open_goals must be a tuple")
        if not isinstance(self.references, tuple) or not all(
            isinstance(ref, str) for ref in self.references
        ):
            raise TypeError("references must be a tuple of strings")
        if not isinstance(self.diagnostics, tuple) or not all(
            isinstance(reason, str) for reason in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if self.root_step is not None and not isinstance(self.root_step, ProofStep):
            raise TypeError("root_step must be ProofStep or None")
        if self.status is ProofSearchStatus.COMPLETE:
            if self.conclusion is None or self.open_goals:
                raise ValueError("completed narrative needs a conclusion and no open goals")
        elif self.conclusion is not None:
            raise ValueError("incomplete narrative cannot claim a conclusion")


def build_narrative_proof_model(
    source: PartialProofResult | TodaGroupProofPresentation,
) -> NarrativeProofModel:
    """Normalize either existing proof input without changing its evidence."""
    if isinstance(source, PartialProofResult):
        roots = tuple(
            step for step in source.proven_steps
            if source.conclusion is not None and step.conclusion == source.conclusion
        )
        return NarrativeProofModel(
            target=source.target,
            status=source.status,
            proven_steps=source.proven_steps,
            open_goals=source.open_goals,
            references=source.references,
            diagnostics=source.diagnostics,
            conclusion=source.conclusion,
            root_step=roots[-1] if roots else None,
            source_kind="search_result",
            source=source,
        )
    if isinstance(source, TodaGroupProofPresentation):
        root = source.root_step
        return NarrativeProofModel(
            target=source.source_replay.group_result.target,
            status=ProofSearchStatus.COMPLETE,
            proven_steps=tuple(node.proof_step for node in source.nodes),
            open_goals=(),
            references=(),
            diagnostics=(),
            conclusion=root.conclusion,
            root_step=root,
            source_kind="presentation",
            source=source,
        )
    raise TypeError("source must be PartialProofResult or TodaGroupProofPresentation")
