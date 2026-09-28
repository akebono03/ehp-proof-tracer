from dataclasses import dataclass
from enum import Enum

from proof import (
  ProofStep,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_latex,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


class TodaGroupProofNarrativeExactnessDisplayContributionKind(
  Enum
):
  EXACTNESS_WINDOW = "exactness_window"
  DERIVED_SHORT_EXACT_SEQUENCE = (
    "derived_short_exact_sequence"
  )


@dataclass(frozen=True)
class TodaGroupProofNarrativeExactnessDisplayContribution:
  kind: (
    TodaGroupProofNarrativeExactnessDisplayContributionKind
  )
  proof_step: ProofStep
  latex: str

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.kind,
      TodaGroupProofNarrativeExactnessDisplayContributionKind,
    ):
      raise TypeError(
        "kind must be a "
        "TodaGroupProofNarrativeExactnessDisplayContributionKind"
      )

    if not isinstance(
      self.proof_step,
      ProofStep,
    ):
      raise TypeError(
        "proof_step must be a ProofStep"
      )

    if not isinstance(
      self.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    ):
      raise ValueError(
        "proof_step conclusion must be a "
        "TodaProp42ExactnessStatement"
      )

    if not isinstance(
      self.latex,
      str,
    ):
      raise TypeError(
        "latex must be a string"
      )

    if not self.latex:
      raise ValueError(
        "latex must not be empty"
      )


def _exactness_window_latex(
  proof_step: ProofStep,
) -> str:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if (
    len(
      rendered
    ) >= 2
    and rendered.startswith(
      "$"
    )
    and rendered.endswith(
      "$"
    )
  ):
    return rendered[
      1:-1
    ]

  return rendered


def extract_toda_group_proof_narrative_exactness_display_contributions(
  presentation: TodaGroupProofPresentation,
  block: TodaGroupProofNarrativeBlock,
) -> tuple[
  TodaGroupProofNarrativeExactnessDisplayContribution,
  ...,
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    block,
    TodaGroupProofNarrativeBlock,
  ):
    raise TypeError(
      "block must be a "
      "TodaGroupProofNarrativeBlock"
    )

  if (
    block.role
    is not TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
  ):
    raise ValueError(
      "block must be an EXACTNESS block"
    )

  selected_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }

  contributions = []

  for proof_step in block.steps:
    if id(
      proof_step
    ) not in selected_step_ids:
      raise ValueError(
        "block proof steps must appear "
        "in presentation nodes"
      )

    if not isinstance(
      proof_step.conclusion,
      TodaProp42ExactnessStatement,
    ):
      continue

    contributions.append(
      TodaGroupProofNarrativeExactnessDisplayContribution(
        kind=(
          TodaGroupProofNarrativeExactnessDisplayContributionKind
          .EXACTNESS_WINDOW
        ),
        proof_step=proof_step,
        latex=_exactness_window_latex(
          proof_step
        ),
      )
    )

    short_exact_sequence_latex = (
      _generic_short_exact_sequence_latex(
        presentation,
        proof_step,
      )
    )

    if short_exact_sequence_latex is None:
      continue

    contributions.append(
      TodaGroupProofNarrativeExactnessDisplayContribution(
        kind=(
          TodaGroupProofNarrativeExactnessDisplayContributionKind
          .DERIVED_SHORT_EXACT_SEQUENCE
        ),
        proof_step=proof_step,
        latex=short_exact_sequence_latex,
      )
    )

  return tuple(
    contributions
  )
