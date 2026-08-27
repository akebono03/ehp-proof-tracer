from dataclasses import dataclass

from expression import (
  Composition,
  Expression,
  Suspension,
)
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
  value: Expression
  source: LiteratureReference | str | None = None
  note: str | None = None


@dataclass(frozen=True)
class HopfCompositionLawStatement:
  alpha: Expression
  beta: Expression


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


def hopf_composition_law_inference_rule():
  def conclusion_builder(
    premises,
  ):
    statement = (
      premises[0].conclusion
    )

    return HopfCompositionLawStatement(
      alpha=statement.expression,
      beta=statement.value,
    )

  return InferenceRule(
    name=(
      "generalized Hopf invariant "
      "enables composition law"
    ),
    description=(
      "A generalized Hopf invariant "
      "fact H(alpha)=beta enables the "
      "Hopf composition law for "
      "alpha and beta."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HopfInvariantStatement
        ),
      ),
    ),
    conclusion_builder=(
      conclusion_builder
    ),
  )


def hopf_composition_formula_inference_rule():
  def conclusion_builder(
    premises,
  ):
    law_statement = (
      premises[0].conclusion
    )

    gamma = (
      premises[1].conclusion
    )

    suspended_gamma = Suspension(
      expression=gamma,
    )

    return HopfInvariantStatement(
      expression=Composition(
        left=law_statement.alpha,
        right=suspended_gamma,
      ),
      value=Composition(
        left=law_statement.beta,
        right=suspended_gamma,
      ),
    )

  return InferenceRule(
    name=(
      "generalized Hopf "
      "composition formula"
    ),
    description=(
      "From the generalized Hopf "
      "composition law for alpha and "
      "beta, and an expression gamma, "
      "derive "
      "H(alpha o E gamma) "
      "= beta o E gamma."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HopfCompositionLawStatement
        ),
      ),
      PremisePattern(
        statement_type=Expression,
      ),
    ),
    conclusion_builder=(
      conclusion_builder
    ),
  )






