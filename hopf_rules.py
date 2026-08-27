from dataclasses import dataclass

from expression import Expression
from proof import (
  InferenceRule,
  LiteratureReference,
  PremisePattern,
  ProofRule,
  ProofStep,
)


@dataclass(frozen=True)
class HopfInvariantStatement:
  expression: Expression
  value: int
  source: LiteratureReference | str | None = None
  note: str | None = None


@dataclass(frozen=True)
class HopfInvariantOneStatement:
  expression: Expression


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


def hopf_invariant_one_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = premises[0].conclusion

    return statement.value == 1

  def build_conclusion(
    premises,
  ):
    statement = premises[0].conclusion

    return HopfInvariantOneStatement(
      expression=statement.expression,
    )

  return InferenceRule(
    name=(
      "Hopf invariant one fact "
      "implies Hopf invariant one"
    ),
    description=(
      "An element whose known Hopf "
      "invariant is one is recognized "
      "as a Hopf-invariant-one element."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HopfInvariantStatement
        ),
      ),
    ),
    conclusion_builder=(
      build_conclusion
    ),
    match_guard=guard,
  )






