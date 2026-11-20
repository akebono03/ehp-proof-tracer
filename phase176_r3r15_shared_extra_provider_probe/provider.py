"""Source-screened, generic two-step proposals for an isolated shared-provider probe.

The provider must be passed explicitly as an extra provider. This module does
not register it in production. It never creates a GIVEN or completed proof.
"""
from __future__ import annotations

from typing import Callable

from phase175_r3r9_lemma57_explicit_public.rule import (
    expand_cited_lemma57_explicit_zero,
)
from phase175_r3r9_lemma57_explicit_public.source import (
    TodaLemma57ExplicitNuPrimeZero,
)
from phase176_r3r14_isolated_two_stage_provider.provider import preceding_zero_image
from phase176_r3r10_right_zero_transport_isolated.rule import expand_right_zero_transport
from proof import ProofRule, ProofStep


def build_screened_extra_provider(
    screened_source_steps: tuple[ProofStep, ...],
) -> Callable[[object], tuple]:
    """Offer cited base or right-composition transport as open proof obligations.

    A citation must first have survived the ordinary independent-source screen.
    The right-composition branch is generic, but can close only if the shared
    recursive search actually proves its typed antecedent.
    """
    if len(screened_source_steps) != 1:
        raise ValueError("ONE_SCREENED_SOURCE_REQUIRED")
    step = screened_source_steps[0]
    if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
            or step.premises or type(step.conclusion) is not TodaLemma57ExplicitNuPrimeZero):
        raise ValueError("SCREENED_SOURCE_STEP_INVALID")
    citation = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
    if citation is None or citation.locator != "Lemma 5.7":
        raise ValueError("LEMMA57_CITATION_REQUIRED")
    available = (step.conclusion,)

    def expand(goal: object) -> tuple:
        cited = tuple(expand_cited_lemma57_explicit_zero(goal, available))
        if cited and (len(cited) != 1 or cited[0].subgoals != available):
            raise RuntimeError("CITED_SUBGOALS_CHANGED")
        base = preceding_zero_image(goal)
        right = () if base is None else tuple(expand_right_zero_transport(goal, base))
        return right + cited

    return expand
