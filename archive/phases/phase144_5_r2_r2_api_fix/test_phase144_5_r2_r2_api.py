import inspect

from toda_group_proof_narrative_equation_numbering import (
  number_toda_group_proof_narrative_equations,
)


def test_phase144_5_r2_r2_numbering_api_accepts_three_parameters():
  signature = inspect.signature(
    number_toda_group_proof_narrative_equations
  )

  assert tuple(
    signature.parameters
  ) == (
    "markdown",
    "presentation",
    "blocks",
  )
