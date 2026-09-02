from dataclasses import dataclass

from ehp_rules import (
  EHPZeroCompositionStatement,
)
from expression import (
  Composition,
  Expression,
  MapApplication,
  SmashProduct,
  Suspension,
  Zero,
)
from map_facts import EHP_H_MAP
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


@dataclass(frozen=True)
class HopfLeftCompositionLawStatement:
  alpha: Expression
  beta: Expression
  gamma: Expression


def toda_prop22_right_inference_rule(
  alpha,
  gamma,
):
  def conclusion_builder(
    premises,
  ):
    suspended_gamma = Suspension(
      expression=gamma,
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=Composition(
          left=alpha,
          right=suspended_gamma,
        ),
      ),
      rhs=Composition(
        left=MapApplication(
          map=EHP_H_MAP,
          expression=alpha,
        ),
        right=suspended_gamma,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name="Toda Prop.2.2 right formula",
    description=(
      "Toda Prop.2.2 directly gives "
      "H(alpha o E gamma) "
      "= H(alpha) o E gamma."
    ),
    premise_patterns=(),
    conclusion_builder=conclusion_builder,
  )


def toda_prop22_left_inference_rule(
  alpha,
  gamma,
):
  def conclusion_builder(
    premises,
  ):
    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=Composition(
          left=Suspension(
            expression=gamma,
          ),
          right=alpha,
        ),
      ),
      rhs=Composition(
        left=Suspension(
          expression=SmashProduct(
            left=gamma,
            right=gamma,
          ),
        ),
        right=MapApplication(
          map=EHP_H_MAP,
          expression=alpha,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name="Toda Prop.2.2 left formula",
    description=(
      "Toda Prop.2.2 directly gives "
      "H((E gamma) o alpha) "
      "= E(gamma smash gamma) o H(alpha)."
    ),
    premise_patterns=(),
    conclusion_builder=conclusion_builder,
  )


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


def hopf_invariant_statement_to_ehp_h_equality_inference_rule():
  def conclusion_builder(
    premises,
  ):
    statement = (
      premises[0].conclusion
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=statement.expression,
      ),
      rhs=statement.value,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "generalized Hopf invariant "
      "to EHP H equality"
    ),
    description=(
      "Represent a generalized Hopf "
      "invariant fact H(alpha)=beta "
      "as an equality using the actual "
      "EHP H map."
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


def hopf_left_composition_law_inference_rule():
  def conclusion_builder(
    premises,
  ):
    hopf_statement = (
      premises[0].conclusion
    )

    gamma = (
      premises[1].conclusion
    )

    return HopfLeftCompositionLawStatement(
      alpha=hopf_statement.expression,
      beta=hopf_statement.value,
      gamma=gamma,
    )

  return InferenceRule(
    name=(
      "generalized Hopf invariant "
      "enables left composition law"
    ),
    description=(
      "A generalized Hopf invariant "
      "fact H(alpha)=beta and an "
      "expression gamma enable the "
      "left suspended-composition "
      "Hopf law."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HopfInvariantStatement
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


def hopf_left_composition_formula_inference_rule():
  def conclusion_builder(
    premises,
  ):
    law_statement = (
      premises[0].conclusion
    )

    suspended_gamma = Suspension(
      expression=law_statement.gamma,
    )

    suspended_smash = Suspension(
      expression=SmashProduct(
        left=law_statement.gamma,
        right=law_statement.gamma,
      ),
    )

    return HopfInvariantStatement(
      expression=Composition(
        left=suspended_gamma,
        right=law_statement.alpha,
      ),
      value=Composition(
        left=suspended_smash,
        right=law_statement.beta,
      ),
    )

  return InferenceRule(
    name=(
      "generalized Hopf left "
      "composition formula"
    ),
    description=(
      "From the generalized Hopf "
      "left composition law for "
      "alpha, beta, and gamma, derive "
      "H((E gamma) o alpha) "
      "= E(gamma smash gamma) o beta."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HopfLeftCompositionLawStatement
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


def ehp_zero_composition_implies_suspended_hopf_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    ehp_statement = (
      premises[0].conclusion
    )

    return (
      getattr(
        ehp_statement.first_map,
        "name",
        None,
      )
      == "E"
      and getattr(
        ehp_statement.second_map,
        "name",
        None,
      )
      == "H"
    )

  def conclusion_builder(
    premises,
  ):
    expression = (
      premises[1].conclusion
    )

    return HopfInvariantStatement(
      expression=Suspension(
        expression=expression,
      ),
      value=Zero(),
    )

  return InferenceRule(
    name=(
      "EHP E-H zero composition "
      "implies suspended Hopf zero"
    ),
    description=(
      "For the EHP map pair E followed "
      "by H, the zero composition H o E "
      "implies H(E alpha)=0."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          EHPZeroCompositionStatement
        ),
      ),
      PremisePattern(
        statement_type=Expression,
      ),
    ),
    conclusion_builder=(
      conclusion_builder
    ),
    match_guard=guard,
  )












