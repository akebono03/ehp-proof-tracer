from dataclasses import dataclass

from expression import Expression
from proof import (
  LiteratureReference,
  ProofRule,
  ProofStep,
)


@dataclass(frozen=True)
class HopfInvariantStatement:
  expression: Expression
  value: int
  source: LiteratureReference | str | None = None
  note: str | None = None


def hopf_invariant_proof_step(
  statement,
):
  if not isinstance(
    statement,
    HopfInvariantStatement,
  ):
    raise TypeError(
      "statement must be a "
      "HopfInvariantStatement"
    )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )




