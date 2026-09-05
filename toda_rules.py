from dataclasses import dataclass

from expression import (
  Composition,
  Expression,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  Suspension,
  TodaBracket,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FreeCyclicGroup,
  PrimaryComponent,
  PrimaryComponentMembershipStatement,
  TodaEHPExactnessWindow,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ExactnessStatement,
  InferenceRule,
  LiteratureReference,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
  ScalarGreaterEqualStatement,
)


@dataclass(frozen=True)
class TodaProp42ExactnessStatement:
  window: TodaEHPExactnessWindow


@dataclass(frozen=True)
class Toda45IsomorphismStatement:
  map: TodaIteratedSuspensionMap


def toda_45_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    stable_range = (
      premises[
        0
      ].conclusion
    )

    suspension_range = (
      premises[
        1
      ].conclusion
    )

    suspension_map = (
      premises[
        2
      ].conclusion
    )

    n = stable_range.left

    stable_right = (
      stable_range.right
    )

    if not isinstance(
      stable_right,
      ScalarSum,
    ):
      return False

    if (
      stable_right.right
      != 2
    ):
      return False

    k = stable_right.left

    if (
      suspension_range.right
      != n
    ):
      return False

    m = suspension_range.left

    source = (
      suspension_map.source_group
    )

    target = (
      suspension_map.target_group
    )

    source_dimension = (
      source.group_dimension
    )

    if not isinstance(
      source_dimension,
      ScalarSum,
    ):
      return False

    if (
      source_dimension.left
      != n
    ):
      return False

    if (
      source_dimension.right
      != k
    ):
      return False

    if (
      source.sphere_dimension
      != n
    ):
      return False

    target_dimension = (
      target.group_dimension
    )

    if not isinstance(
      target_dimension,
      ScalarSum,
    ):
      return False

    if (
      target_dimension.left
      != m
    ):
      return False

    if (
      target_dimension.right
      != k
    ):
      return False

    if (
      target.sphere_dimension
      != m
    ):
      return False

    expected_exponent = ScalarSum(
      left=m,
      right=ScalarProduct(
        left=-1,
        right=n,
      ),
    )

    return (
      suspension_map.exponent
      == expected_exponent
    )

  def build_conclusion(
    premises,
  ):
    suspension_map = (
      premises[
        2
      ].conclusion
    )

    return Toda45IsomorphismStatement(
      map=suspension_map,
    )

  return InferenceRule(
    name=(
      "Toda 4.5 stable-range "
      "iterated suspension isomorphism"
    ),
    description=(
      "If n is at least k+2 and "
      "m is at least n, Toda (4.5) "
      "states that the iterated "
      "suspension E^(m-n) from "
      "pi_(n+k)^n to pi_(m+k)^m "
      "is an isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaIteratedSuspensionMap
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop42_e_h_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[0].conclusion
    )

    if (
      window.first_map
      != EHP_E_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_H_MAP
    ):
      return False

    source = window.source_term
    middle = window.middle_term
    target = window.target_term

    i = source.group_dimension
    n = source.sphere_dimension

    i_plus_one = ScalarSum(
      left=i,
      right=1,
    )

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    two_n_plus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=1,
    )

    return (
      middle
      == TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=n_plus_one,
      )
      and target
      == TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=two_n_plus_one,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[0].conclusion
    )

    return TodaProp42ExactnessStatement(
      window=window,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.2 "
      "E-H exactness"
    ),
    description=(
      "Toda Proposition 4.2 states "
      "that pi_i^n -> pi_(i+1)^(n+1) "
      "-> pi_(i+1)^(2n+1) is exact "
      "for the E and H maps."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEHPExactnessWindow
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop42_h_delta_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[0].conclusion
    )

    if (
      window.first_map
      != EHP_H_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_DELTA_MAP
    ):
      return False

    source = window.source_term
    middle = window.middle_term
    target = window.target_term

    target_dimension = (
      target.group_dimension
    )

    if not isinstance(
      target_dimension,
      ScalarSum,
    ):
      return False

    if (
      target_dimension.right
      != -1
    ):
      return False

    i = target_dimension.left
    n = target.sphere_dimension

    i_plus_one = ScalarSum(
      left=i,
      right=1,
    )

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    two_n_plus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=1,
    )

    return (
      source
      == TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=n_plus_one,
      )
      and middle
      == TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=two_n_plus_one,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[0].conclusion
    )

    return TodaProp42ExactnessStatement(
      window=window,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.2 "
      "H-Delta exactness"
    ),
    description=(
      "Toda Proposition 4.2 states "
      "that pi_(i+1)^(n+1) -> "
      "pi_(i+1)^(2n+1) -> "
      "pi_(i-1)^n is exact "
      "for the H and Delta maps."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEHPExactnessWindow
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop42_delta_e_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[0].conclusion
    )

    if (
      window.first_map
      != EHP_DELTA_MAP
    ):
      return False

    if (
      window.second_map
      != EHP_E_MAP
    ):
      return False

    source = window.source_term
    middle = window.middle_term
    target = window.target_term

    i = target.group_dimension
    n = middle.sphere_dimension

    i_plus_one = ScalarSum(
      left=i,
      right=1,
    )

    i_minus_one = ScalarSum(
      left=i,
      right=-1,
    )

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    two_n_plus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=1,
    )

    return (
      source
      == TodaPrimaryGroup(
        group_dimension=i_plus_one,
        sphere_dimension=two_n_plus_one,
      )
      and middle
      == TodaPrimaryGroup(
        group_dimension=i_minus_one,
        sphere_dimension=n,
      )
      and target
      == TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=n_plus_one,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[0].conclusion
    )

    return TodaProp42ExactnessStatement(
      window=window,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.2 "
      "Delta-E exactness"
    ),
    description=(
      "Toda Proposition 4.2 states "
      "that pi_(i+1)^(2n+1) -> "
      "pi_(i-1)^n -> pi_i^(n+1) "
      "is exact for the Delta and E maps."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEHPExactnessWindow
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop42_exactness_to_generic_inference_rule():
  def build_conclusion(
    premises,
  ):
    statement = (
      premises[0].conclusion
    )

    window = statement.window

    return ExactnessStatement(
      first_map=window.first_map,
      second_map=window.second_map,
      is_exact=True,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.2 "
      "exactness to generic exactness"
    ),
    description=(
      "A Toda Proposition 4.2 "
      "exactness statement implies the "
      "corresponding generic exactness "
      "statement for its two maps."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def toda_lemma41_odd_case_inference_rule():
  def build_conclusion(
    premises,
  ):
    odd_statement = (
      premises[0].conclusion
    )

    n = odd_statement.scalar

    critical_degree = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=-1,
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=critical_degree,
        sphere_dimension=n,
      ),
      rhs=PrimaryComponent(
        group_dimension=critical_degree,
        sphere_dimension=n,
        prime=2,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 4.1 odd case"
    ),
    description=(
      "If n is odd, Toda Lemma 4.1 "
      "identifies pi_(2n-1)^n with "
      "the 2-primary component "
      "pi_(2n-1)(S^n;2)."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          OddScalarStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def toda_lemma41_even_nonzero_case_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    even_statement = (
      premises[0].conclusion
    )

    nonzero_relation = (
      premises[1].conclusion
    )

    n = even_statement.scalar

    n_minus_one = ScalarSum(
      left=n,
      right=-1,
    )

    expected_iota = HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )

    expected_whitehead = (
      WhiteheadProduct(
        left=expected_iota,
        right=expected_iota,
      )
    )

    return (
      nonzero_relation.lhs
      == expected_whitehead
      and nonzero_relation.rhs
      == Zero()
    )

  def build_conclusion(
    premises,
  ):
    even_statement = (
      premises[0].conclusion
    )

    n = even_statement.scalar

    two_n_minus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=-1,
    )

    two_n_plus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=1,
    )

    iota_two_n_plus_one = (
      HomotopyElement(
        name="ι_(2n+1)",
        dimension=two_n_plus_one,
        generator=GeneratorSymbol(
          family="ι",
          index=two_n_plus_one,
        ),
      )
    )

    free_part = FreeCyclicGroup(
      generator=MapApplication(
        map=MapSymbol(
          name="P",
        ),
        expression=iota_two_n_plus_one,
      ),
    )

    primary_part = PrimaryComponent(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
      prime=2,
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=two_n_minus_one,
        sphere_dimension=n,
      ),
      rhs=DirectSumGroup(
        summands=(
          free_part,
          primary_part,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 4.1 even "
      "Whitehead nonzero case"
    ),
    description=(
      "If n is even and "
      "[iota_(n-1),iota_(n-1)] "
      "is nonzero, then "
      "pi_(2n-1)^n is the direct sum "
      "of Z generated by P(iota_(2n+1)) "
      "and its 2-primary component."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          EvenScalarStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.INEQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma41_even_zero_case_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    even_statement = (
      premises[0].conclusion
    )

    zero_relation = (
      premises[1].conclusion
    )

    n = even_statement.scalar

    n_minus_one = ScalarSum(
      left=n,
      right=-1,
    )

    expected_iota = HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )

    expected_whitehead = (
      WhiteheadProduct(
        left=expected_iota,
        right=expected_iota,
      )
    )

    return (
      zero_relation.lhs
      == expected_whitehead
      and zero_relation.rhs
      == Zero()
    )

  def build_conclusion(
    premises,
  ):
    even_statement = (
      premises[0].conclusion
    )

    n = even_statement.scalar

    two_n_minus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=-1,
    )

    alpha = HomotopyElement(
      name="α",
      dimension=two_n_minus_one,
    )

    free_part = FreeCyclicGroup(
      generator=alpha,
    )

    primary_part = PrimaryComponent(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
      prime=2,
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=two_n_minus_one,
        sphere_dimension=n,
      ),
      rhs=DirectSumGroup(
        summands=(
          free_part,
          primary_part,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 4.1 even "
      "Whitehead zero case"
    ),
    description=(
      "If n is even and "
      "[iota_(n-1),iota_(n-1)] "
      "is zero, then pi_(2n-1)^n "
      "is the direct sum of Z "
      "generated by alpha and its "
      "2-primary component."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          EvenScalarStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma41_even_zero_h_alpha_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    even_statement = (
      premises[0].conclusion
    )

    zero_relation = (
      premises[1].conclusion
    )

    n = even_statement.scalar

    n_minus_one = ScalarSum(
      left=n,
      right=-1,
    )

    expected_iota = HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )

    expected_whitehead = (
      WhiteheadProduct(
        left=expected_iota,
        right=expected_iota,
      )
    )

    return (
      zero_relation.lhs
      == expected_whitehead
      and zero_relation.rhs
      == Zero()
    )

  def build_conclusion(
    premises,
  ):
    even_statement = (
      premises[0].conclusion
    )

    n = even_statement.scalar

    two_n_minus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=-1,
    )

    alpha = HomotopyElement(
      name="α",
      dimension=two_n_minus_one,
    )

    iota_two_n_minus_one = (
      HomotopyElement(
        name="ι_(2n-1)",
        dimension=two_n_minus_one,
        generator=GeneratorSymbol(
          family="ι",
          index=two_n_minus_one,
        ),
      )
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=alpha,
      ),
      rhs=iota_two_n_minus_one,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 4.1 even zero "
      "alpha Hopf condition"
    ),
    description=(
      "If n is even and "
      "[iota_(n-1),iota_(n-1)] "
      "is zero, the alpha generator "
      "in Toda Lemma 4.1 satisfies "
      "H(alpha)=iota_(2n-1)."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          EvenScalarStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma41_even_zero_suspension_primary_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    even_statement = (
      premises[0].conclusion
    )

    zero_relation = (
      premises[1].conclusion
    )

    n = even_statement.scalar

    n_minus_one = ScalarSum(
      left=n,
      right=-1,
    )

    expected_iota = HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )

    expected_whitehead = (
      WhiteheadProduct(
        left=expected_iota,
        right=expected_iota,
      )
    )

    return (
      zero_relation.lhs
      == expected_whitehead
      and zero_relation.rhs
      == Zero()
    )

  def build_conclusion(
    premises,
  ):
    even_statement = (
      premises[0].conclusion
    )

    n = even_statement.scalar

    two_n_minus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=-1,
    )

    two_n = ScalarProduct(
      left=2,
      right=n,
    )

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    alpha = HomotopyElement(
      name="α",
      dimension=two_n_minus_one,
    )

    return (
      PrimaryComponentMembershipStatement(
        element=Suspension(
          expression=alpha,
        ),
        component=PrimaryComponent(
          group_dimension=two_n,
          sphere_dimension=n_plus_one,
          prime=2,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 4.1 even zero "
      "alpha suspension primary condition"
    ),
    description=(
      "If n is even and "
      "[iota_(n-1),iota_(n-1)] "
      "is zero, the alpha generator "
      "in Toda Lemma 4.1 satisfies "
      "E(alpha) in "
      "pi_(2n)(S^(n+1);2)."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          EvenScalarStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


@dataclass(frozen=True)
class TodaBracketMembershipStatement:
  element: Expression
  bracket: TodaBracket
  source: LiteratureReference | str | None = None
  note: str | None = None


def toda_bracket_membership_proof_step(
  statement,
):
  if not isinstance(
    statement,
    TodaBracketMembershipStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaBracketMembershipStatement"
    )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )


@dataclass(frozen=True)
class TodaBracketMembershipTheoremStatement:
  element: Expression
  bracket: TodaBracket
  source: LiteratureReference | str | None = None
  note: str | None = None


def toda_bracket_membership_theorem_proof_step(
  statement,
):
  if not isinstance(
    statement,
    TodaBracketMembershipTheoremStatement,
  ):
    raise TypeError(
      "statement must be a "
      "TodaBracketMembershipTheoremStatement"
    )

  return ProofStep(
    conclusion=statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )


@dataclass(frozen=True)
class TodaBracketDefinedStatement:
  bracket: TodaBracket


def toda_bracket_membership_from_theorem_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    theorem_statement = premises[0].conclusion
    defined_statement = premises[1].conclusion

    return (
      theorem_statement.bracket
      == defined_statement.bracket
    )

  def conclusion_builder(
    premises,
  ):
    theorem_statement = premises[0].conclusion

    return TodaBracketMembershipStatement(
      element=theorem_statement.element,
      bracket=theorem_statement.bracket,
      source=theorem_statement.source,
      note=theorem_statement.note,
    )

  return InferenceRule(
    name=(
      "Toda bracket membership "
      "from theorem"
    ),
    description=(
      "If a literature-backed Toda "
      "membership theorem applies to "
      "a defined bracket, derive the "
      "corresponding bracket membership."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaBracketMembershipTheoremStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaBracketDefinedStatement
        ),
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
  )


def indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data,
):
  def guard(
    premises,
    bindings,
  ):
    theorem_statement = (
      premises[0].conclusion
    )

    defined_statement = (
      premises[1].conclusion
    )

    return (
      indexed_data.is_consistent()
      and indexed_data.bracket
      .are_defining_compositions_type_compatible()
      and theorem_statement.bracket
      == indexed_data.bracket
      and defined_statement.bracket
      == indexed_data.bracket
    )

  def build_conclusion(
    premises,
  ):
    theorem_statement = (
      premises[0].conclusion
    )

    return TodaBracketMembershipStatement(
      element=theorem_statement.element,
      bracket=theorem_statement.bracket,
      source=theorem_statement.source,
      note=theorem_statement.note,
    )

  return InferenceRule(
    name=(
      "Indexed Toda membership theorem "
      "bridge with structural and typing guards"
    ),
    description=(
      "A matching indexed Toda theorem fact "
      "and definedness derive membership only "
      "when the supplied indexed bracket data "
      "is structurally consistent and its "
      "displayed entries are type-compatible."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaBracketMembershipTheoremStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaBracketDefinedStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_bracket_defined_by_zero_compositions_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    first_relation = premises[0].conclusion
    second_relation = premises[1].conclusion

    first_composition = first_relation.lhs
    second_composition = second_relation.lhs

    if not isinstance(
      first_composition,
      Composition,
    ):
      return False

    if not isinstance(
      second_composition,
      Composition,
    ):
      return False

    return (
      first_composition.right
      == second_composition.left
    )

  def conclusion_builder(
    premises,
  ):
    first_relation = premises[0].conclusion
    second_relation = premises[1].conclusion

    first_composition = first_relation.lhs
    second_composition = second_relation.lhs

    return TodaBracketDefinedStatement(
      bracket=TodaBracket(
        first=first_composition.left,
        second=first_composition.right,
        third=second_composition.right,
      ),
    )

  return InferenceRule(
    name=(
      "Toda bracket defined by "
      "zero compositions"
    ),
    description=(
      "If a∘b and b∘c are zero, "
      "the three-fold Toda bracket "
      "{a,b,c} is defined."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
  )


def indexed_toda_bracket_index1_defined_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    first_relation = premises[0].conclusion
    second_relation = premises[1].conclusion
    suspension_relation = premises[2].conclusion

    first_composition = first_relation.lhs
    second_composition = second_relation.lhs

    if not isinstance(
      first_composition,
      Composition,
    ):
      return False

    if not isinstance(
      second_composition,
      Composition,
    ):
      return False

    if not isinstance(
      first_composition.right,
      Suspension,
    ):
      return False

    if (
      first_composition.right.expression
      != second_composition.left
    ):
      return False

    if not isinstance(
      suspension_relation.lhs,
      Suspension,
    ):
      return False

    return (
      suspension_relation.lhs.expression
      == second_composition.right
    )

  def conclusion_builder(
    premises,
  ):
    first_relation = premises[0].conclusion
    suspension_relation = premises[2].conclusion

    first_composition = first_relation.lhs

    return TodaBracketDefinedStatement(
      bracket=TodaBracket(
        first=first_composition.left,
        second=first_composition.right,
        third=suspension_relation.rhs,
        index=1,
      ),
    )

  return InferenceRule(
    name=(
      "Indexed Toda bracket index 1 "
      "defined by base zero compositions"
    ),
    description=(
      "If a∘Eb=0, b∘c=0, and Ec=d, "
      "then the indexed Toda bracket "
      "{a,Eb,d}_1 is defined."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
      ),
    ),
    conclusion_builder=conclusion_builder,
    match_guard=guard,
  )





