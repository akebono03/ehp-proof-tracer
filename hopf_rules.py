from dataclasses import dataclass

from expression import (
  Composition,
  Expression,
  Suspension,
  Zero,
)
from proof import (
  InferenceRule,
  LiteratureReference,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
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


def hopf_invariant_value_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_statement = (
      premises[0].conclusion
    )

    zero_relation = (
      premises[1].conclusion
    )

    return (
      zero_relation.lhs
      == hopf_statement.value
      and zero_relation.rhs
      == Zero()
    )

  def conclusion_builder(
    premises,
  ):
    hopf_statement = (
      premises[0].conclusion
    )

    return HopfInvariantStatement(
      expression=(
        hopf_statement.expression
      ),
      value=Zero(),
      source=hopf_statement.source,
      note=hopf_statement.note,
    )

  return InferenceRule(
    name=(
      "generalized Hopf invariant "
      "value is zero"
    ),
    description=(
      "If H(x)=y and y is known "
      "to be zero, derive H(x)=0."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HopfInvariantStatement
        ),
      ),
      PremisePattern(
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=(
      conclusion_builder
    ),
    match_guard=guard,
  )











