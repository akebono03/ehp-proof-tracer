"""Observe existing backward derivations without approving or selecting them.

Only the original append_unique_verified_derivation() decides whether an
existing candidate is kept. All data returned here are diagnostic observations.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppendObservation:
    """A root candidate, before/after the production deduplication routine."""

    kept: bool
    options_before: int
    options_after: int
    candidate: object


def is_exact_goal_conclusion(candidate: object, goal: object) -> bool:
    """Distinguish root derivations from similarly printed nested statements."""
    conclusion = getattr(candidate, "conclusion", None)
    return type(conclusion) is type(goal) and conclusion == goal


def forward_and_observe(options: list, candidate: object, *, goal: object,
                        delegate, observations: list[AppendObservation]) -> None:
    """Delegate unchanged, recording a root attempt only after it returns."""
    before = len(options)
    delegate(options, candidate)
    if is_exact_goal_conclusion(candidate, goal):
        observations.append(AppendObservation(
            kept=len(options) > before,
            options_before=before,
            options_after=len(options),
            candidate=candidate,
        ))


def pairwise_kept_indices(observations: list[AppendObservation]) -> tuple[tuple[int, int], ...]:
    """Enumerate kept candidate pairs without merging or ranking them."""
    kept = tuple(i for i, row in enumerate(observations) if row.kept)
    return tuple((left, right) for pos, left in enumerate(kept)
                 for right in kept[pos + 1:])
