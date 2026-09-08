from dataclasses import dataclass

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  Expression,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  MapSymbol,
  Multiple,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
  TodaBracket,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  PrimaryComponent,
  PrimaryComponentMembershipStatement,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaPrimaryGroupZeroStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
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
  LiteratureStatement,
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
class TodaHopfInvariantInjectiveStatement:
  map: TodaHopfInvariantMap


@dataclass(frozen=True)
class TodaSuspensionInjectiveStatement:
  map: TodaSuspensionMap


@dataclass(frozen=True)
class TodaDeltaInjectiveStatement:
  map: TodaDeltaMap


@dataclass(frozen=True)
class TodaHopfInvariantZeroStatement:
  map: TodaHopfInvariantMap


@dataclass(frozen=True)
class TodaDeltaZeroStatement:
  map: TodaDeltaMap


@dataclass(frozen=True)
class TodaHopfInvariantSurjectiveStatement:
  map: TodaHopfInvariantMap


@dataclass(frozen=True)
class TodaHopfInvariantIsomorphismStatement:
  map: TodaHopfInvariantMap


@dataclass(frozen=True)
class TodaPi32Eta2DefinitionStatement:
  map: TodaHopfInvariantMap
  element: HomotopyElement
  image: HomotopyElement


@dataclass(frozen=True)
class TodaProp27HopfInvariantUpToSignStatement:
  argument: Expression
  positive_value: Expression


@dataclass(frozen=True)
class TodaPi32WhiteheadSquareUpToSignStatement:
  whitehead_square: Expression
  positive_value: Expression


@dataclass(frozen=True)
class TodaDeltaImageUpToSignStatement:
  map: TodaDeltaMap
  element: Expression
  positive_value: Expression


@dataclass(frozen=True)
class TodaDeltaPreimageUpToSignStatement:
  map: TodaDeltaMap
  value: Expression
  positive_preimage: Expression


def toda_lemma52_delta_two_eta2_preimage_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_statement = (
      premises[
        0
      ].conclusion
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    if (
      delta_statement.map.source_group
      != expected_source
    ):
      return False

    if (
      delta_statement.map.target_group
      != expected_target
    ):
      return False

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    if (
      delta_statement.element
      != iota_5
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    expected_two_eta_2 = Multiple(
      coefficient=2,
      expression=eta_2,
    )

    return (
      delta_statement.positive_value
      == expected_two_eta_2
    )

  def build_conclusion(
    premises,
  ):
    delta_statement = (
      premises[
        0
      ].conclusion
    )

    return (
      TodaDeltaPreimageUpToSignStatement(
        map=delta_statement.map,
        value=(
          delta_statement
          .positive_value
        ),
        positive_preimage=(
          delta_statement
          .element
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.2 "
      "Delta inverse of twice eta_2"
    ),
    description=(
      "For the specific Delta map "
      "from pi_5^5 to pi_3^2, "
      "the independently derived "
      "relation Delta(iota_5) equals "
      "plus or minus 2 eta_2 gives "
      "the Lemma 5.2 connection "
      "Delta^-1(2 eta_2) equals "
      "plus or minus iota_5."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaImageUpToSignStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


@dataclass(frozen=True)
class TodaProp51FiniteDimensionalStatement:
  pi3_2_group_relation: Relation
  eta2_hopf_relation: Relation
  delta_iota5_relation: TodaDeltaImageUpToSignStatement
  higher_eta_group_relation: Relation


@dataclass(frozen=True)
class TodaProp53FiniteDimensionalStatement:
  pi4_2_group_relation: Relation
  pi5_3_group_relation: Relation
  pi6_4_group_relation: Relation
  higher_eta_squared_group_relation: Relation
  higher_range: ScalarGreaterEqualStatement


def toda_prop51_finite_dimensional_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi3_2_group_relation = (
      premises[
        0
      ].conclusion
    )

    eta2_hopf_relation = (
      premises[
        1
      ].conclusion
    )

    delta_iota5_relation = (
      premises[
        2
      ].conclusion
    )

    higher_eta_group_relation = (
      premises[
        3
      ].conclusion
    )

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    pi_3_2 = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    pi_5_5 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_pi3_2_relation = Relation(
      lhs=pi_3_2,
      rhs=FreeCyclicGroup(
        generator=eta_2,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi3_2_group_relation
      != expected_pi3_2_relation
    ):
      return False

    expected_hopf_relation = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=eta_2,
      ),
      rhs=iota_3,
      relation_type=RelationType.EQUALITY,
    )

    if (
      eta2_hopf_relation
      != expected_hopf_relation
    ):
      return False

    expected_delta_relation = (
      TodaDeltaImageUpToSignStatement(
        map=TodaDeltaMap(
          source_group=pi_5_5,
          target_group=pi_3_2,
        ),
        element=iota_5,
        positive_value=Multiple(
          coefficient=2,
          expression=eta_2,
        ),
      )
    )

    if (
      delta_iota5_relation
      != expected_delta_relation
    ):
      return False

    if not isinstance(
      higher_eta_group_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    target_group = (
      higher_eta_group_relation.lhs
    )

    n = (
      target_group
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_target_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      sphere_dimension=n,
    )

    if (
      target_group
      != expected_target_group
    ):
      return False

    if not isinstance(
      higher_eta_group_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      higher_eta_group_relation.rhs.order
      != 2
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      higher_eta_group_relation
      == Relation(
        lhs=expected_target_group,
        rhs=FiniteCyclicGroup(
          order=2,
          generator=eta_n,
        ),
        relation_type=RelationType.EQUALITY,
      )
    )

  def build_conclusion(
    premises,
  ):
    return (
      TodaProp51FiniteDimensionalStatement(
        pi3_2_group_relation=(
          premises[
            0
          ].conclusion
        ),
        eta2_hopf_relation=(
          premises[
            1
          ].conclusion
        ),
        delta_iota5_relation=(
          premises[
            2
          ].conclusion
        ),
        higher_eta_group_relation=(
          premises[
            3
          ].conclusion
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.1 "
      "finite-dimensional integration"
    ),
    description=(
      "Integrate the independently "
      "derived finite-dimensional "
      "results pi_3^2=Z{eta_2}, "
      "H(eta_2)=iota_3, "
      "Delta(iota_5)=plus or minus "
      "2 eta_2, and "
      "pi_(n+1)^n=Z/2{eta_n} "
      "into the finite-dimensional "
      "Toda Proposition 5.1 statement."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaImageUpToSignStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_n3_prop51_delta_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    delta_relation = (
      statement
      .delta_iota5_relation
    )

    pi_5_5 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    pi_3_2 = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    if (
      delta_relation.map.source_group
      != pi_5_5
    ):
      return False

    if (
      delta_relation.map.target_group
      != pi_3_2
    ):
      return False

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    if (
      delta_relation.element
      != iota_5
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    return (
      delta_relation.positive_value
      == Multiple(
        coefficient=2,
        expression=eta_2,
      )
    )

  def build_conclusion(
    premises,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    return TodaDeltaInjectiveStatement(
      map=(
        statement
        .delta_iota5_relation
        .map
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.1 "
      "n=3 Delta injectivity"
    ),
    description=(
      "For the concrete Delta map "
      "from pi_5^5 to pi_3^2, "
      "the Proposition 5.1 data "
      "Delta(iota_5)=plus or minus "
      "2 eta_2 gives the injectivity "
      "required in the n=3 proof of "
      "Toda Proposition 5.3."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_n3_delta_injective_hopf_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
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

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      injectivity.map
      == TodaDeltaMap(
        source_group=expected_middle,
        target_group=expected_target,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Delta injectivity "
      "implies Hopf zero"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_5^3 -> pi_5^5 -> pi_3^2, "
      "injectivity of Delta makes "
      "Ker(Delta) zero. Exactness "
      "therefore makes the image of H "
      "zero."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaInjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_n3_hopf_zero_suspension_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_zero = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
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

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      hopf_zero.map
      == TodaHopfInvariantMap(
        source_group=expected_middle,
        target_group=expected_target,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Hopf zero "
      "implies suspension surjective"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_4^2 -> pi_5^3 -> pi_5^5, "
      "if H is zero then Ker(H) is "
      "all of pi_5^3. Exactness "
      "therefore makes suspension E "
      "surjective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_n3_hopf_eta5_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_relation = (
      premises[
        0
      ].conclusion
    )

    prop51_statement = (
      premises[
        1
      ].conclusion
    )

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    if (
      hopf_relation
      != Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=nu_prime,
        ),
        rhs=eta_5,
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    higher_relation = (
      prop51_statement
      .higher_eta_group_relation
    )

    if not isinstance(
      higher_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      higher_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    n = (
      higher_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_symbolic_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      sphere_dimension=n,
    )

    if (
      higher_relation.lhs
      != expected_symbolic_group
    ):
      return False

    if (
      higher_relation.rhs.order
      != 2
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      higher_relation
      .rhs
      .generator
      == eta_n
    )

  def build_conclusion(
    premises,
  ):
    return TodaHopfInvariantSurjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=TodaPrimaryGroup(
          group_dimension=6,
          sphere_dimension=3,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=6,
          sphere_dimension=5,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Hopf eta_5 surjectivity"
    ),
    description=(
      "Phase 58 gives H(nu-prime)=eta_5. "
      "Proposition 5.1 gives the "
      "order-two higher eta family, "
      "whose n=5 instance is "
      "pi_6^5=Z/2{eta_5}. Therefore "
      "H from pi_6^3 to pi_6^5 is "
      "surjective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_n3_hopf_surjective_delta_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    surjectivity = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
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

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      surjectivity.map
      == TodaHopfInvariantMap(
        source_group=expected_source,
        target_group=expected_middle,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaDeltaZeroStatement(
      map=TodaDeltaMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Hopf surjective "
      "implies Delta zero"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_6^3 -> pi_6^5 -> pi_4^2, "
      "surjectivity of H makes Im(H) "
      "all of pi_6^5. Exactness gives "
      "Ker(Delta)=pi_6^5, so Delta "
      "is zero."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantSurjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_n3_delta_zero_suspension_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_zero = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
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

    if (
      window.source_term
      != expected_source
    ):
      return False

    if (
      window.middle_term
      != expected_middle
    ):
      return False

    if (
      window.target_term
      != expected_target
    ):
      return False

    return (
      delta_zero.map
      == TodaDeltaMap(
        source_group=expected_source,
        target_group=expected_middle,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 Delta zero "
      "implies suspension injective"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_6^5 -> pi_4^2 -> pi_5^3, "
      "Delta zero makes Im(Delta) zero. "
      "Exactness therefore makes the "
      "kernel of suspension E zero, so "
      "E is injective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_n3_suspension_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    surjectivity = (
      premises[
        1
      ].conclusion
    )

    expected_map = TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=2,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=3,
      ),
    )

    return (
      injectivity.map
      == expected_map
      and surjectivity.map
      == expected_map
    )

  def build_conclusion(
    premises,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    return TodaSuspensionIsomorphismStatement(
      map=injectivity.map,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 suspension isomorphism"
    ),
    description=(
      "If the concrete suspension map "
      "from pi_4^2 to pi_5^3 is both "
      "injective and surjective, it is "
      "an isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionSurjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_n3_eta_square_suspension_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    eta3_definition = (
      premises[
        0
      ].conclusion
    )

    eta4_definition = (
      premises[
        1
      ].conclusion
    )

    if (
      eta3_definition.index
      != 3
    ):
      return False

    if (
      eta4_definition.index
      != 4
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      eta3_definition.element
      != eta_3
    ):
      return False

    if (
      eta3_definition.iterated_suspension
      != IteratedSuspension(
        expression=eta_2,
        exponent=1,
      )
    ):
      return False

    eta4_element = (
      eta4_definition.element
    )

    if (
      eta4_element.dimension
      != 4
    ):
      return False

    if (
      eta4_element.source
      != 5
    ):
      return False

    if (
      eta4_element.target
      != 4
    ):
      return False

    if (
      eta4_element.generator
      != GeneratorSymbol(
        family="η",
        index=4,
      )
    ):
      return False

    return (
      eta4_definition.iterated_suspension
      == IteratedSuspension(
        expression=eta_2,
        exponent=2,
      )
    )

  def build_conclusion(
    premises,
  ):
    eta3_definition = (
      premises[
        0
      ].conclusion
    )

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = (
      eta3_definition.element
    )

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    eta_2_squared = Composition(
      left=eta_2,
      right=eta_3,
    )

    eta_3_squared = Composition(
      left=eta_3,
      right=eta_4,
    )

    return Relation(
      lhs=Suspension(
        expression=eta_2_squared,
      ),
      rhs=eta_3_squared,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 eta-square suspension bridge"
    ),
    description=(
      "For the concrete eta-family "
      "definitions at indices 3 and 4, "
      "derive the Proposition 5.3 "
      "n=3 relation "
      "E(eta_2 composed with eta_3) "
      "equals eta_3 composed with eta_4. "
      "This is the concrete relation "
      "E eta_2 squared=eta_3 squared. "
      "No generic eta-square expression "
      "or suspension normalization is "
      "introduced."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    eta_square_relation = (
      premises[
        2
      ].conclusion
    )

    pi_4_2 = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )

    pi_5_3 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    if (
      source_relation.lhs
      != pi_4_2
    ):
      return False

    if not isinstance(
      source_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      source_relation.rhs.order
      != 2
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    eta_2_squared = Composition(
      left=eta_2,
      right=eta_3,
    )

    eta_3_squared = Composition(
      left=eta_3,
      right=eta_4,
    )

    if (
      source_relation.rhs.generator
      != eta_2_squared
    ):
      return False

    suspension_map = (
      isomorphism.map
    )

    if (
      suspension_map.source_group
      != pi_4_2
    ):
      return False

    if (
      suspension_map.target_group
      != pi_5_3
    ):
      return False

    expected_eta_square_relation = Relation(
      lhs=Suspension(
        expression=eta_2_squared,
      ),
      rhs=eta_3_squared,
      relation_type=RelationType.EQUALITY,
    )

    return (
      eta_square_relation
      == expected_eta_square_relation
    )

  def build_conclusion(
    premises,
  ):
    eta_square_relation = (
      premises[
        2
      ].conclusion
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=(
          eta_square_relation.rhs
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=3 pi_5^3 finite-cyclic transport"
    ),
    description=(
      "Transport the independently "
      "derived group "
      "pi_4^2=Z/2{eta_2 squared} "
      "through the independently derived "
      "suspension isomorphism "
      "E:pi_4^2 to pi_5^3. "
      "Using the concrete bridge "
      "E eta_2 squared=eta_3 squared, "
      "derive "
      "pi_5^3=Z/2{eta_3 squared}."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionIsomorphismStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_n4_phase48_injectivity_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    suspension_map = (
      injectivity.map
    )

    expected_structural_source = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=6,
          right=-1,
        ),
        sphere_dimension=ScalarSum(
          left=4,
          right=-1,
        ),
      )
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    )

    return (
      suspension_map.source_group
      == expected_structural_source
      and suspension_map.target_group
      == expected_target
    )

  def build_conclusion(
    premises,
  ):
    return (
      TodaProp44SuspensionInjectiveStatement(
        map=TodaSuspensionMap(
          source_group=TodaPrimaryGroup(
            group_dimension=5,
            sphere_dimension=3,
          ),
          target_group=TodaPrimaryGroup(
            group_dimension=6,
            sphere_dimension=4,
          ),
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=4 Phase 48 injectivity bridge"
    ),
    description=(
      "Specialize the independently "
      "derived Toda Proposition 4.4 "
      "suspension injectivity instance "
      "with i=6 and n=4. "
      "The structural first summand "
      "pi_(6-1)^(4-1) is identified "
      "with the concrete group pi_5^3, "
      "giving injectivity of suspension "
      "E from pi_5^3 to pi_6^4. "
      "No general scalar normalization "
      "is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp44SuspensionInjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_n4_zero_right_suspension_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    zero_statement = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=7,
    )

    if (
      zero_statement.group
      != expected_target
    ):
      return False

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

    return (
      window.source_term
      == expected_source
      and window.middle_term
      == expected_middle
      and window.target_term
      == expected_target
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return (
      TodaSuspensionSurjectiveStatement(
        map=TodaSuspensionMap(
          source_group=window.source_term,
          target_group=window.middle_term,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=4 zero-right "
      "suspension surjectivity"
    ),
    description=(
      "For the concrete E-H exact "
      "window pi_5^3 to pi_6^4 "
      "to pi_6^7, the Toda (5.1) "
      "fact pi_6^7=0 makes the "
      "kernel of H all of pi_6^4. "
      "Exactness therefore makes "
      "suspension E from pi_5^3 "
      "to pi_6^4 surjective."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_n4_suspension_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    surjectivity = (
      premises[
        1
      ].conclusion
    )

    expected_map = TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=3,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=4,
      ),
    )

    return (
      injectivity.map
      == expected_map
      and surjectivity.map
      == expected_map
    )

  def build_conclusion(
    premises,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    return (
      TodaSuspensionIsomorphismStatement(
        map=injectivity.map,
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=4 suspension isomorphism"
    ),
    description=(
      "If the concrete suspension map "
      "E from pi_5^3 to pi_6^4 is "
      "both injective and surjective, "
      "then it is an isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp44SuspensionInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionSurjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_n4_eta_square_suspension_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    eta4_definition = (
      premises[
        0
      ].conclusion
    )

    eta5_definition = (
      premises[
        1
      ].conclusion
    )

    if (
      eta4_definition.index
      != 4
    ):
      return False

    if (
      eta5_definition.index
      != 5
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta4_element = (
      eta4_definition.element
    )

    if (
      eta4_element.dimension
      != 4
    ):
      return False

    if (
      eta4_element.source
      != 5
    ):
      return False

    if (
      eta4_element.target
      != 4
    ):
      return False

    if (
      eta4_element.generator
      != GeneratorSymbol(
        family="η",
        index=4,
      )
    ):
      return False

    if (
      eta4_definition.iterated_suspension
      != IteratedSuspension(
        expression=eta_2,
        exponent=2,
      )
    ):
      return False

    eta5_element = (
      eta5_definition.element
    )

    if (
      eta5_element.dimension
      != 5
    ):
      return False

    if (
      eta5_element.source
      != 6
    ):
      return False

    if (
      eta5_element.target
      != 5
    ):
      return False

    if (
      eta5_element.generator
      != GeneratorSymbol(
        family="η",
        index=5,
      )
    ):
      return False

    return (
      eta5_definition.iterated_suspension
      == IteratedSuspension(
        expression=eta_2,
        exponent=3,
      )
    )

  def build_conclusion(
    premises,
  ):
    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    eta_3_squared = Composition(
      left=eta_3,
      right=eta_4,
    )

    eta_4_squared = Composition(
      left=eta_4,
      right=eta_5,
    )

    return Relation(
      lhs=Suspension(
        expression=eta_3_squared,
      ),
      rhs=eta_4_squared,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=4 eta-square suspension bridge"
    ),
    description=(
      "For the concrete eta-family "
      "definitions at indices 4 and 5, "
      "derive the Proposition 5.3 "
      "n=4 relation "
      "E(eta_3 composed with eta_4) "
      "equals eta_4 composed with eta_5. "
      "This is the concrete relation "
      "E eta_3 squared=eta_4 squared. "
      "No generic eta-square expression "
      "or suspension normalization is "
      "introduced."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_n4_pi6_4_finite_cyclic_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    eta_square_relation = (
      premises[
        2
      ].conclusion
    )

    pi_5_3 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )

    pi_6_4 = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    )

    if (
      source_relation.lhs
      != pi_5_3
    ):
      return False

    if not isinstance(
      source_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      source_relation.rhs.order
      != 2
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    eta_3_squared = Composition(
      left=eta_3,
      right=eta_4,
    )

    eta_4_squared = Composition(
      left=eta_4,
      right=eta_5,
    )

    if (
      source_relation.rhs.generator
      != eta_3_squared
    ):
      return False

    suspension_map = (
      isomorphism.map
    )

    if (
      suspension_map.source_group
      != pi_5_3
    ):
      return False

    if (
      suspension_map.target_group
      != pi_6_4
    ):
      return False

    expected_eta_square_relation = Relation(
      lhs=Suspension(
        expression=eta_3_squared,
      ),
      rhs=eta_4_squared,
      relation_type=RelationType.EQUALITY,
    )

    return (
      eta_square_relation
      == expected_eta_square_relation
    )

  def build_conclusion(
    premises,
  ):
    eta_square_relation = (
      premises[
        2
      ].conclusion
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=4,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=(
          eta_square_relation.rhs
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "n=4 pi_6^4 finite-cyclic transport"
    ),
    description=(
      "Transport the independently "
      "derived group "
      "pi_5^3=Z/2{eta_3 squared} "
      "through the independently "
      "derived suspension isomorphism "
      "E:pi_5^3 to pi_6^4. "
      "Using the concrete bridge "
      "E eta_3 squared=eta_4 squared, "
      "derive "
      "pi_6^4=Z/2{eta_4 squared}."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionIsomorphismStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_eta4_squared_stable_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    higher_range = (
      premises[
        2
      ].conclusion
    )

    pi_6_4 = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=4,
    )

    if (
      source_relation.lhs
      != pi_6_4
    ):
      return False

    if not isinstance(
      source_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      source_relation.rhs.order
      != 2
    ):
      return False

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    eta_4_squared = Composition(
      left=eta_4,
      right=eta_5,
    )

    if (
      source_relation.rhs.generator
      != eta_4_squared
    ):
      return False

    suspension_map = (
      isomorphism.map
    )

    source_group = (
      suspension_map.source_group
    )

    expected_structural_source = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=4,
          right=2,
        ),
        sphere_dimension=4,
      )
    )

    if (
      source_group
      != expected_structural_source
    ):
      return False

    target_group = (
      suspension_map.target_group
    )

    if not isinstance(
      target_group,
      TodaPrimaryGroup,
    ):
      return False

    n = (
      target_group
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      higher_range.left
      != n
    ):
      return False

    if (
      higher_range.right
      != 5
    ):
      return False

    expected_target_group = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
    )

    if (
      target_group
      != expected_target_group
    ):
      return False

    expected_exponent = ScalarSum(
      left=n,
      right=ScalarProduct(
        left=-1,
        right=4,
      ),
    )

    return (
      suspension_map.exponent
      == expected_exponent
    )

  def build_conclusion(
    premises,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    suspension_map = (
      isomorphism.map
    )

    return Relation(
      lhs=(
        suspension_map
        .target_group
      ),
      rhs=FiniteCyclicGroup(
        order=(
          source_relation
          .rhs
          .order
        ),
        generator=IteratedSuspension(
          expression=(
            source_relation
            .rhs
            .generator
          ),
          exponent=(
            suspension_map
            .exponent
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "eta_4 squared stable transport"
    ),
    description=(
      "For symbolic n at least 5, "
      "transport the independently "
      "derived finite cyclic group "
      "pi_6^4=Z/2{eta_4 squared} "
      "through the Toda (4.5) "
      "iterated suspension isomorphism "
      "E^(n-4) from pi_6^4 to "
      "pi_(n+2)^n. The target is "
      "cyclic of order 2 generated by "
      "E^(n-4) eta_4 squared. "
      "No normalization to eta_n "
      "squared is performed."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda45IsomorphismStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_higher_eta_squared_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    higher_range = (
      premises[
        1
      ].conclusion
    )

    n = definition.index

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      higher_range.left
      != n
    ):
      return False

    if (
      higher_range.right
      != 5
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    if (
      definition.element
      != eta_n
    ):
      return False

    expected_definition = (
      IteratedSuspension(
        expression=eta_2,
        exponent=ScalarSum(
          left=n,
          right=-2,
        ),
      )
    )

    return (
      definition.iterated_suspension
      == expected_definition
    )

  def build_conclusion(
    premises,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    n = definition.index

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    eta_4_squared = Composition(
      left=eta_4,
      right=eta_5,
    )

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    n_plus_two = ScalarSum(
      left=n,
      right=2,
    )

    eta_n = definition.element

    eta_n_plus_one = HomotopyElement(
      name="η_(n+1)",
      dimension=n_plus_one,
      source=n_plus_two,
      target=n_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_one,
      ),
    )

    eta_n_squared = Composition(
      left=eta_n,
      right=eta_n_plus_one,
    )

    return Relation(
      lhs=IteratedSuspension(
        expression=eta_4_squared,
        exponent=ScalarSum(
          left=n,
          right=ScalarProduct(
            left=-1,
            right=4,
          ),
        ),
      ),
      rhs=eta_n_squared,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "higher eta-squared bridge"
    ),
    description=(
      "For symbolic n at least 5, "
      "use the eta-family definition "
      "to derive the Proposition 5.3 "
      "bridge from "
      "E^(n-4) eta_4 squared "
      "to eta_n squared, represented "
      "as eta_n composed with "
      "eta_(n+1). "
      "This rule is specific to "
      "Toda Proposition 5.3 and does "
      "not introduce generic suspension "
      "of composition normalization."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    transported_relation = (
      premises[
        0
      ].conclusion
    )

    generator_bridge = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      transported_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      transported_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      transported_relation.rhs.order
      != 2
    ):
      return False

    target_group = (
      transported_relation.lhs
    )

    n = (
      target_group
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_target = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    )

    if (
      target_group
      != expected_target
    ):
      return False

    if (
      transported_relation
      .rhs
      .generator
      != generator_bridge.lhs
    ):
      return False

    return isinstance(
      generator_bridge.rhs,
      Composition,
    )

  def build_conclusion(
    premises,
  ):
    transported_relation = (
      premises[
        0
      ].conclusion
    )

    generator_bridge = (
      premises[
        1
      ].conclusion
    )

    return Relation(
      lhs=transported_relation.lhs,
      rhs=FiniteCyclicGroup(
        order=2,
        generator=generator_bridge.rhs,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "higher eta-squared "
      "finite-cyclic generator bridge"
    ),
    description=(
      "Replace the transported "
      "generator E^(n-4) eta_4 squared "
      "in the independently derived "
      "order-two finite cyclic group "
      "by eta_n squared using the "
      "independently derived "
      "Proposition 5.3 generator bridge."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop53_finite_dimensional_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi4_2_relation = (
      premises[
        0
      ].conclusion
    )

    pi5_3_relation = (
      premises[
        1
      ].conclusion
    )

    pi6_4_relation = (
      premises[
        2
      ].conclusion
    )

    higher_relation = (
      premises[
        3
      ].conclusion
    )

    higher_range = (
      premises[
        4
      ].conclusion
    )

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    eta_2_squared = Composition(
      left=eta_2,
      right=eta_3,
    )

    eta_3_squared = Composition(
      left=eta_3,
      right=eta_4,
    )

    eta_4_squared = Composition(
      left=eta_4,
      right=eta_5,
    )

    expected_pi4_2 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_2_squared,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi4_2_relation
      != expected_pi4_2
    ):
      return False

    expected_pi5_3 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_3_squared,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi5_3_relation
      != expected_pi5_3
    ):
      return False

    expected_pi6_4 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=4,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_4_squared,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi6_4_relation
      != expected_pi6_4
    ):
      return False

    if not isinstance(
      higher_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    n = (
      higher_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      higher_range.left
      != n
    ):
      return False

    if (
      higher_range.right
      != 5
    ):
      return False

    expected_higher_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    )

    if (
      higher_relation.lhs
      != expected_higher_group
    ):
      return False

    if not isinstance(
      higher_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      higher_relation.rhs.order
      != 2
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    eta_n_plus_one = HomotopyElement(
      name="η_(n+1)",
      dimension=n_plus_one,
      source=ScalarSum(
        left=n,
        right=2,
      ),
      target=n_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_one,
      ),
    )

    eta_n_squared = Composition(
      left=eta_n,
      right=eta_n_plus_one,
    )

    return (
      higher_relation.rhs.generator
      == eta_n_squared
    )

  def build_conclusion(
    premises,
  ):
    return (
      TodaProp53FiniteDimensionalStatement(
        pi4_2_group_relation=(
          premises[
            0
          ].conclusion
        ),
        pi5_3_group_relation=(
          premises[
            1
          ].conclusion
        ),
        pi6_4_group_relation=(
          premises[
            2
          ].conclusion
        ),
        higher_eta_squared_group_relation=(
          premises[
            3
          ].conclusion
        ),
        higher_range=(
          premises[
            4
          ].conclusion
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.3 "
      "finite-dimensional integration"
    ),
    description=(
      "Integrate the independently "
      "derived cases "
      "pi_4^2=Z/2{eta_2 squared}, "
      "pi_5^3=Z/2{eta_3 squared}, "
      "pi_6^4=Z/2{eta_4 squared}, "
      "and the symbolic n at least 5 "
      "result "
      "pi_(n+2)^n=Z/2{eta_n squared} "
      "into one finite-dimensional "
      "Toda Proposition 5.3 statement."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


@dataclass(frozen=True)
class TodaEtaFamilyDefinitionStatement:
  index: int | ScalarSymbol
  element: HomotopyElement
  iterated_suspension: IteratedSuspension


@dataclass(frozen=True)
class TodaDeltaImageFreeCyclicStatement:
  map: TodaDeltaMap
  image_group: FreeCyclicGroup


@dataclass(frozen=True)
class TodaSuspensionKernelFreeCyclicStatement:
  map: TodaSuspensionMap
  kernel_group: FreeCyclicGroup


@dataclass(frozen=True)
class TodaSuspensionSurjectiveStatement:
  map: TodaSuspensionMap


@dataclass(frozen=True)
class Toda45IsomorphismStatement:
  map: TodaIteratedSuspensionMap


def toda_prop27_iota2_whitehead_hopf_invariant_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    whitehead_product = (
      premises[
        0
      ].conclusion
    )

    iota_2 = HomotopyElement(
      name="ι_2",
      dimension=2,
      generator=GeneratorSymbol(
        family="ι",
        index=2,
      ),
    )

    expected_whitehead_product = (
      WhiteheadProduct(
        left=iota_2,
        right=iota_2,
      )
    )

    return (
      whitehead_product
      == expected_whitehead_product
    )

  def build_conclusion(
    premises,
  ):
    whitehead_product = (
      premises[
        0
      ].conclusion
    )

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    return (
      TodaProp27HopfInvariantUpToSignStatement(
        argument=whitehead_product,
        positive_value=Multiple(
          coefficient=2,
          expression=iota_3,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 2.7 "
      "iota_2 Whitehead-square "
      "Hopf invariant up to sign"
    ),
    description=(
      "For the Whitehead square "
      "[iota_2,iota_2], the required "
      "Toda Proposition 2.7 consequence "
      "states that its Hopf invariant "
      "is plus or minus 2 iota_3."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          WhiteheadProduct
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


@dataclass(frozen=True)
class TodaProp44IsomorphismStatement:
  map: TodaProp44DecompositionMap


@dataclass(frozen=True)
class TodaProp44FirstSummandRestrictionStatement:
  decomposition_map: TodaProp44DecompositionMap
  suspension_map: TodaSuspensionMap


@dataclass(frozen=True)
class TodaProp44SecondSummandRestrictionStatement:
  decomposition_map: TodaProp44DecompositionMap
  composition: Composition


@dataclass(frozen=True)
class Toda52CompositionIsomorphismStatement:
  source_group: TodaPrimaryGroup
  target_group: TodaPrimaryGroup
  composition: Composition


@dataclass(frozen=True)
class TodaProp44SuspensionInjectiveStatement:
  map: TodaSuspensionMap


def toda_52_eta2_composition_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    zero_statement = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    restriction = (
      premises[
        2
      ].conclusion
    )

    decomposition_map = (
      isomorphism.map
    )

    if (
      restriction.decomposition_map
      != decomposition_map
    ):
      return False

    source_group = (
      decomposition_map.source_group
    )

    if not isinstance(
      source_group,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        source_group.summands
      )
      != 2
    ):
      return False

    first_summand = (
      source_group.summands[
        0
      ]
    )

    second_summand = (
      source_group.summands[
        1
      ]
    )

    if not isinstance(
      first_summand,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      second_summand,
      TodaPrimaryGroup,
    ):
      return False

    target_group = (
      decomposition_map.target_group
    )

    if not isinstance(
      target_group,
      TodaPrimaryGroup,
    ):
      return False

    i = (
      target_group.group_dimension
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    expected_first_summand = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=-1,
        ),
        sphere_dimension=1,
      )
    )

    if (
      first_summand
      != expected_first_summand
    ):
      return False

    if (
      zero_statement.group
      != first_summand
    ):
      return False

    expected_second_summand = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=3,
      )
    )

    if (
      second_summand
      != expected_second_summand
    ):
      return False

    expected_target_group = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=2,
      )
    )

    if (
      target_group
      != expected_target_group
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    if (
      decomposition_map.alpha
      != eta_2
    ):
      return False

    expected_composition = (
      Composition(
        left=eta_2,
        right=(
          decomposition_map.gamma
        ),
      )
    )

    if (
      restriction.composition
      != expected_composition
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=expected_composition,
    )

    return (
      decomposition_map.formula
      == expected_formula
    )

  def build_conclusion(
    premises,
  ):
    isomorphism = (
      premises[
        1
      ].conclusion
    )

    restriction = (
      premises[
        2
      ].conclusion
    )

    decomposition_map = (
      isomorphism.map
    )

    second_summand = (
      decomposition_map
      .source_group
      .summands[
        1
      ]
    )

    return (
      Toda52CompositionIsomorphismStatement(
        source_group=second_summand,
        target_group=(
          decomposition_map
          .target_group
        ),
        composition=(
          restriction.composition
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.2 eta_2 "
      "composition isomorphism"
    ),
    description=(
      "If the first summand "
      "pi_(i-1)^1 is zero, the derived "
      "n=2 and alpha=eta_2 Toda "
      "Proposition 4.4 decomposition "
      "map is an isomorphism, and its "
      "restriction to the second "
      "summand is composition with "
      "eta_2, then composition with "
      "eta_2 gives an isomorphism "
      "from pi_i^3 to pi_i^2."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp44IsomorphismStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp44SecondSummandRestrictionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_52_pi4_2_finite_cyclic_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    pi_4_3 = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )

    if (
      source_relation.lhs
      != pi_4_3
    ):
      return False

    if not isinstance(
      source_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      source_relation.rhs.order
      != 2
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      source_relation.rhs.generator
      != eta_3
    ):
      return False

    source_group = (
      isomorphism.source_group
    )

    target_group = (
      isomorphism.target_group
    )

    if not isinstance(
      source_group,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      target_group,
      TodaPrimaryGroup,
    ):
      return False

    i = (
      source_group
      .group_dimension
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    if (
      source_group
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=3,
      )
    ):
      return False

    if (
      target_group
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=2,
      )
    ):
      return False

    composition = (
      isomorphism.composition
    )

    if not isinstance(
      composition,
      Composition,
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    if (
      composition.left
      != eta_2
    ):
      return False

    gamma = composition.right

    if not isinstance(
      gamma,
      HomotopyElement,
    ):
      return False

    if (
      gamma.dimension
      != i
    ):
      return False

    if (
      gamma.source
      != i
    ):
      return False

    if (
      gamma.target
      != 3
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    eta_2 = (
      isomorphism
      .composition
      .left
    )

    eta_3 = (
      source_relation
      .rhs
      .generator
    )

    eta_2_squared = Composition(
      left=eta_2,
      right=eta_3,
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_2_squared,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 5.2 pi_4^2 "
      "finite-cyclic transport"
    ),
    description=(
      "Specialize the derived Toda "
      "(5.2) composition isomorphism "
      "eta_2 composed with minus from "
      "pi_i^3 to pi_i^2 to i=4. "
      "Together with the independently "
      "derived relation "
      "pi_4^3=Z/2{eta_3}, transport "
      "the generator eta_3 to "
      "eta_2 composed with eta_3 and "
      "derive "
      "pi_4^2=Z/2{eta_2 squared}."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda52CompositionIsomorphismStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi_i_minus_1_1_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    lower_bound = (
      premises[
        0
      ].conclusion
    )

    i = lower_bound.left

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    if (
      lower_bound.right
      != 3
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    lower_bound = (
      premises[
        0
      ].conclusion
    )

    i = lower_bound.left

    return TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=-1,
        ),
        sphere_dimension=1,
      ),
    )

  return InferenceRule(
    name=(
      "Toda pi_(i-1)^1 "
      "zero for i at least 3"
    ),
    description=(
      "For symbolic i at least 3, "
      "the Toda primary group "
      "pi_(i-1)^1 is zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop44_eta2_second_summand_restriction_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    decomposition_map = (
      isomorphism.map
    )

    source_group = (
      decomposition_map.source_group
    )

    if not isinstance(
      source_group,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        source_group.summands
      )
      != 2
    ):
      return False

    first_summand = (
      source_group.summands[
        0
      ]
    )

    second_summand = (
      source_group.summands[
        1
      ]
    )

    if not isinstance(
      first_summand,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      second_summand,
      TodaPrimaryGroup,
    ):
      return False

    target_group = (
      decomposition_map.target_group
    )

    if not isinstance(
      target_group,
      TodaPrimaryGroup,
    ):
      return False

    i = (
      target_group.group_dimension
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    expected_first_summand = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=-1,
        ),
        sphere_dimension=1,
      )
    )

    if (
      first_summand
      != expected_first_summand
    ):
      return False

    expected_second_summand = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=3,
      )
    )

    if (
      second_summand
      != expected_second_summand
    ):
      return False

    expected_target_group = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=2,
      )
    )

    if (
      target_group
      != expected_target_group
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    if (
      decomposition_map.alpha
      != eta_2
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=eta_2,
        right=(
          decomposition_map.gamma
        ),
      ),
    )

    return (
      decomposition_map.formula
      == expected_formula
    )

  def build_conclusion(
    premises,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    decomposition_map = (
      isomorphism.map
    )

    return (
      TodaProp44SecondSummandRestrictionStatement(
        decomposition_map=(
          decomposition_map
        ),
        composition=Composition(
          left=(
            decomposition_map.alpha
          ),
          right=(
            decomposition_map.gamma
          ),
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.4 "
      "eta_2 second-summand restriction"
    ),
    description=(
      "For the derived n=2 and "
      "alpha=eta_2 specialization of "
      "Toda Proposition 4.4, restrict "
      "the decomposition map "
      "E(beta)+eta_2 composed with gamma "
      "to the second direct-sum summand. "
      "The resulting expression is "
      "eta_2 composed with gamma."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp44IsomorphismStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop44_first_summand_restriction_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    decomposition_map = (
      premises[
        0
      ].conclusion
    )

    suspension_map = (
      premises[
        1
      ].conclusion
    )

    source = (
      decomposition_map.source_group
    )

    if (
      len(
        source.summands
      )
      != 2
    ):
      return False

    first_summand = (
      source.summands[
        0
      ]
    )

    second_summand = (
      source.summands[
        1
      ]
    )

    if not isinstance(
      first_summand,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      second_summand,
      TodaPrimaryGroup,
    ):
      return False

    if (
      suspension_map.source_group
      != first_summand
    ):
      return False

    if (
      suspension_map.target_group
      != decomposition_map.target_group
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=(
          decomposition_map.alpha
        ),
        right=(
          decomposition_map.gamma
        ),
      ),
    )

    return (
      decomposition_map.formula
      == expected_formula
    )

  def build_conclusion(
    premises,
  ):
    decomposition_map = (
      premises[
        0
      ].conclusion
    )

    suspension_map = (
      premises[
        1
      ].conclusion
    )

    return (
      TodaProp44FirstSummandRestrictionStatement(
        decomposition_map=decomposition_map,
        suspension_map=suspension_map,
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.4 "
      "first-summand restriction"
    ),
    description=(
      "For the Toda Proposition 4.4 "
      "decomposition map sending "
      "(beta,gamma) to "
      "E(beta)+alpha composed with "
      "gamma, its restriction to the "
      "first direct-sum summand is the "
      "corresponding suspension map."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaProp44DecompositionMap
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaSuspensionMap
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop44_suspension_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    restriction = (
      premises[
        1
      ].conclusion
    )

    if (
      isomorphism.map
      != restriction.decomposition_map
    ):
      return False

    decomposition_map = (
      isomorphism.map
    )

    suspension_map = (
      restriction.suspension_map
    )

    source = (
      decomposition_map.source_group
    )

    if (
      len(
        source.summands
      )
      != 2
    ):
      return False

    first_summand = (
      source.summands[
        0
      ]
    )

    if (
      suspension_map.source_group
      != first_summand
    ):
      return False

    if (
      suspension_map.target_group
      != decomposition_map.target_group
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    restriction = (
      premises[
        1
      ].conclusion
    )

    return (
      TodaProp44SuspensionInjectiveStatement(
        map=(
          restriction.suspension_map
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.4 "
      "suspension injectivity"
    ),
    description=(
      "If the Toda Proposition 4.4 "
      "decomposition map is an "
      "isomorphism and its restriction "
      "to the first direct-sum summand "
      "is the supplied suspension map, "
      "then that suspension map is "
      "injective."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaProp44IsomorphismStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp44FirstSummandRestrictionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop44_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    hopf_relation = (
      premises[
        1
      ].conclusion
    )

    decomposition_map = (
      premises[
        2
      ].conclusion
    )

    alpha = membership.element

    group = membership.group

    n = group.sphere_dimension

    two_n_minus_one = ScalarSum(
      left=ScalarProduct(
        left=2,
        right=n,
      ),
      right=-1,
    )

    if (
      group.group_dimension
      != two_n_minus_one
    ):
      return False

    if (
      decomposition_map.alpha
      != alpha
    ):
      return False

    expected_h_alpha = MapApplication(
      map=EHP_H_MAP,
      expression=alpha,
    )

    if (
      hopf_relation.lhs
      != expected_h_alpha
    ):
      return False

    expected_iota = HomotopyElement(
      name="ι_(2n-1)",
      dimension=two_n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=two_n_minus_one,
      ),
    )

    positive_hopf = (
      hopf_relation.rhs
      == expected_iota
    )

    negative_hopf = (
      hopf_relation.rhs
      == Multiple(
        coefficient=-1,
        expression=expected_iota,
      )
    )

    if not (
      positive_hopf
      or negative_hopf
    ):
      return False

    target = (
      decomposition_map.target_group
    )

    if (
      target.sphere_dimension
      != n
    ):
      return False

    i = target.group_dimension

    source = (
      decomposition_map.source_group
    )

    if (
      len(
        source.summands
      )
      != 2
    ):
      return False

    first_summand = (
      source.summands[
        0
      ]
    )

    second_summand = (
      source.summands[
        1
      ]
    )

    if not isinstance(
      first_summand,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      second_summand,
      TodaPrimaryGroup,
    ):
      return False

    expected_first = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=-1,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=-1,
      ),
    )

    expected_second = TodaPrimaryGroup(
      group_dimension=i,
      sphere_dimension=two_n_minus_one,
    )

    if (
      first_summand
      != expected_first
    ):
      return False

    if (
      second_summand
      != expected_second
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=alpha,
        right=(
          decomposition_map.gamma
        ),
      ),
    )

    return (
      decomposition_map.formula
      == expected_formula
    )

  def build_conclusion(
    premises,
  ):
    decomposition_map = (
      premises[
        2
      ].conclusion
    )

    return (
      TodaProp44IsomorphismStatement(
        map=decomposition_map,
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.4 "
      "decomposition isomorphism"
    ),
    description=(
      "If alpha belongs to "
      "pi_(2n-1)^n and "
      "H(alpha)=plus or minus "
      "iota_(2n-1), Toda "
      "Proposition 4.4 states that "
      "the map from "
      "pi_(i-1)^(n-1) direct sum "
      "pi_i^(2n-1) to pi_i^n "
      "sending (beta,gamma) to "
      "E(beta)+alpha composed with "
      "gamma is an isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaPrimaryGroupMembershipStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp44DecompositionMap
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop44_eta2_n2_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    hopf_relation = (
      premises[
        1
      ].conclusion
    )

    decomposition_map = (
      premises[
        2
      ].conclusion
    )

    pi_3_2 = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    pi_3_3 = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    if (
      definition.map.source_group
      != pi_3_2
    ):
      return False

    if (
      definition.map.target_group
      != pi_3_3
    ):
      return False

    if (
      definition.element
      != eta_2
    ):
      return False

    if (
      definition.image
      != iota_3
    ):
      return False

    expected_hopf_relation = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=eta_2,
      ),
      rhs=iota_3,
      relation_type=RelationType.EQUALITY,
    )

    if (
      hopf_relation
      != expected_hopf_relation
    ):
      return False

    if (
      decomposition_map.alpha
      != eta_2
    ):
      return False

    target_group = (
      decomposition_map.target_group
    )

    if not isinstance(
      target_group,
      TodaPrimaryGroup,
    ):
      return False

    if (
      target_group.sphere_dimension
      != 2
    ):
      return False

    i = target_group.group_dimension

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    source_group = (
      decomposition_map.source_group
    )

    if not isinstance(
      source_group,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        source_group.summands
      )
      != 2
    ):
      return False

    expected_first_summand = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=-1,
        ),
        sphere_dimension=1,
      )
    )

    expected_second_summand = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=3,
      )
    )

    if (
      source_group.summands[
        0
      ]
      != expected_first_summand
    ):
      return False

    if (
      source_group.summands[
        1
      ]
      != expected_second_summand
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=eta_2,
        right=(
          decomposition_map.gamma
        ),
      ),
    )

    return (
      decomposition_map.formula
      == expected_formula
    )

  def build_conclusion(
    premises,
  ):
    decomposition_map = (
      premises[
        2
      ].conclusion
    )

    return (
      TodaProp44IsomorphismStatement(
        map=decomposition_map,
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 4.4 "
      "eta_2 n=2 specialization"
    ),
    description=(
      "Specialize Toda Proposition 4.4 "
      "to n=2 and alpha=eta_2 using "
      "the independently derived "
      "definition of eta_2 and "
      "H(eta_2)=iota_3. The resulting "
      "decomposition map from "
      "pi_(i-1)^1 direct sum pi_i^3 "
      "to pi_i^2 is an isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaPi32Eta2DefinitionStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp44DecompositionMap
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


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


def toda_45_pi4_3_finite_cyclic_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    expected_pi_4_3 = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )

    if (
      source_relation.lhs
      != expected_pi_4_3
    ):
      return False

    if not isinstance(
      source_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      source_relation.rhs.order
      != 2
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      source_relation.rhs.generator
      != eta_3
    ):
      return False

    suspension_map = (
      isomorphism.map
    )

    source_group = (
      suspension_map.source_group
    )

    if (
      source_group.sphere_dimension
      != 3
    ):
      return False

    source_dimension = (
      source_group.group_dimension
    )

    concrete_source_dimension = (
      source_dimension
      == 4
    )

    toda45_source_dimension = (
      source_dimension
      == ScalarSum(
        left=3,
        right=1,
      )
    )

    if not (
      concrete_source_dimension
      or toda45_source_dimension
    ):
      return False

    target_group = (
      suspension_map.target_group
    )

    n = (
      target_group.sphere_dimension
    )

    expected_target_dimension = (
      ScalarSum(
        left=n,
        right=1,
      )
    )

    if (
      target_group.group_dimension
      != expected_target_dimension
    ):
      return False

    expected_exponent = ScalarSum(
      left=n,
      right=ScalarProduct(
        left=-1,
        right=3,
      ),
    )

    return (
      suspension_map.exponent
      == expected_exponent
    )

  def build_conclusion(
    premises,
  ):
    source_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    suspension_map = (
      isomorphism.map
    )

    return Relation(
      lhs=(
        suspension_map
        .target_group
      ),
      rhs=FiniteCyclicGroup(
        order=(
          source_relation
          .rhs
          .order
        ),
        generator=IteratedSuspension(
          expression=(
            source_relation
            .rhs
            .generator
          ),
          exponent=(
            suspension_map
            .exponent
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 4.5 pi_4^3 "
      "finite-cyclic transport"
    ),
    description=(
      "If pi_4^3 is cyclic of "
      "order 2 generated by eta_3 "
      "and the supplied Toda 4.5 "
      "iterated suspension map is an "
      "isomorphism from pi_4^3 to "
      "pi_(n+1)^n, then the target "
      "group is cyclic of order 2 "
      "generated by the corresponding "
      "iterated suspension of eta_3."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          Toda45IsomorphismStatement
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


def toda_exactness_zero_left_implies_hopf_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    zero_statement = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

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

    if (
      zero_statement.group
      != window.source_term
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    hopf_map = TodaHopfInvariantMap(
      source_group=window.middle_term,
      target_group=window.target_term,
    )

    return TodaHopfInvariantInjectiveStatement(
      map=hopf_map,
    )

  return InferenceRule(
    name=(
      "Toda EHP exactness "
      "zero-left Hopf injectivity"
    ),
    description=(
      "If an E-H Toda EHP window is "
      "exact and its source group is "
      "zero, then the corresponding "
      "Hopf invariant map from the "
      "middle group to the target "
      "group is injective."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_suspension_isomorphism_implies_injective_inference_rule():
  def build_conclusion(
    premises,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    return TodaSuspensionInjectiveStatement(
      map=isomorphism.map,
    )

  return InferenceRule(
    name=(
      "Toda suspension isomorphism "
      "implies injectivity"
    ),
    description=(
      "An instance-aware Toda "
      "suspension isomorphism implies "
      "injectivity of the same "
      "suspension map instance."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaSuspensionIsomorphismStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def toda_exactness_injective_right_implies_delta_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

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

    suspension_map = (
      injectivity.map
    )

    if (
      suspension_map.source_group
      != window.middle_term
    ):
      return False

    if (
      suspension_map.target_group
      != window.target_term
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    delta_map = TodaDeltaMap(
      source_group=window.source_term,
      target_group=window.middle_term,
    )

    return TodaDeltaZeroStatement(
      map=delta_map,
    )

  return InferenceRule(
    name=(
      "Toda EHP exactness "
      "injective-right Delta zero"
    ),
    description=(
      "If a Delta-E Toda EHP window "
      "is exact and the corresponding "
      "suspension map E is injective, "
      "then the preceding Delta map "
      "is zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaSuspensionInjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_exactness_zero_delta_implies_hopf_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_zero = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

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

    delta_map = (
      delta_zero.map
    )

    if (
      delta_map.source_group
      != window.middle_term
    ):
      return False

    if (
      delta_map.target_group
      != window.target_term
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    hopf_map = TodaHopfInvariantMap(
      source_group=window.source_term,
      target_group=window.middle_term,
    )

    return TodaHopfInvariantSurjectiveStatement(
      map=hopf_map,
    )

  return InferenceRule(
    name=(
      "Toda EHP exactness "
      "zero-Delta Hopf surjectivity"
    ),
    description=(
      "If an H-Delta Toda EHP window "
      "is exact and the corresponding "
      "Delta map is zero, then the "
      "Hopf invariant map is "
      "surjective."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaDeltaZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_hopf_injective_surjective_implies_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    surjectivity = (
      premises[
        1
      ].conclusion
    )

    return (
      injectivity.map
      == surjectivity.map
    )

  def build_conclusion(
    premises,
  ):
    injectivity = (
      premises[
        0
      ].conclusion
    )

    return TodaHopfInvariantIsomorphismStatement(
      map=injectivity.map,
    )

  return InferenceRule(
    name=(
      "Toda Hopf invariant "
      "injective and surjective "
      "implies isomorphism"
    ),
    description=(
      "If the same instance-aware "
      "Toda Hopf invariant map is both "
      "injective and surjective, then "
      "that Hopf invariant map is an "
      "isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaHopfInvariantInjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaHopfInvariantSurjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi3_2_define_eta2_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    target_relation = (
      premises[
        1
      ].conclusion
    )

    hopf_map = isomorphism.map

    expected_source = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )

    if (
      hopf_map.source_group
      != expected_source
    ):
      return False

    if (
      hopf_map.target_group
      != expected_target
    ):
      return False

    if (
      target_relation.lhs
      != expected_target
    ):
      return False

    if not isinstance(
      target_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    expected_iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    return (
      target_relation.rhs.generator
      == expected_iota_3
    )

  def build_conclusion(
    premises,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    target_relation = (
      premises[
        1
      ].conclusion
    )

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    return TodaPi32Eta2DefinitionStatement(
      map=isomorphism.map,
      element=eta_2,
      image=(
        target_relation
        .rhs
        .generator
      ),
    )

  return InferenceRule(
    name=(
      "Toda pi_3^2 define eta_2 "
      "as unique Hopf preimage"
    ),
    description=(
      "Because the specific Hopf "
      "invariant map from pi_3^2 to "
      "pi_3^3 is an isomorphism, "
      "iota_3 has a unique preimage "
      "in pi_3^2. Denote that unique "
      "preimage by eta_2."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaHopfInvariantIsomorphismStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi3_2_eta2_hopf_relation_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )

    if (
      definition.map.source_group
      != expected_source
    ):
      return False

    if (
      definition.map.target_group
      != expected_target
    ):
      return False

    expected_eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    expected_iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    return (
      definition.element
      == expected_eta_2
      and definition.image
      == expected_iota_3
    )

  def build_conclusion(
    premises,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=definition.element,
      ),
      rhs=definition.image,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda pi_3^2 eta_2 "
      "Hopf relation"
    ),
    description=(
      "The element denoted eta_2 "
      "was defined as the unique "
      "preimage of iota_3 under the "
      "Hopf invariant map, hence "
      "H(eta_2)=iota_3."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaPi32Eta2DefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )



def toda_pi3_2_free_cyclic_generator_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    target_relation = (
      premises[
        1
      ].conclusion
    )

    definition = (
      premises[
        2
      ].conclusion
    )

    if (
      definition.map
      != isomorphism.map
    ):
      return False

    if (
      target_relation.lhs
      != isomorphism.map.target_group
    ):
      return False

    if not isinstance(
      target_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    if (
      target_relation.rhs.generator
      != definition.image
    ):
      return False

    expected_source = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )

    if (
      isomorphism.map.source_group
      != expected_source
    ):
      return False

    if (
      isomorphism.map.target_group
      != expected_target
    ):
      return False

    expected_eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    return (
      definition.element
      == expected_eta_2
    )

  def build_conclusion(
    premises,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    definition = (
      premises[
        2
      ].conclusion
    )

    return Relation(
      lhs=(
        isomorphism
        .map
        .source_group
      ),
      rhs=FreeCyclicGroup(
        generator=(
          definition.element
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda pi_3^2 free cyclic "
      "generator transport"
    ),
    description=(
      "If the Hopf invariant map "
      "from pi_3^2 to pi_3^3 is an "
      "isomorphism, pi_3^3 is freely "
      "generated by iota_3, and eta_2 "
      "is defined as the unique "
      "preimage of iota_3, then "
      "pi_3^2 is freely generated "
      "by eta_2."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaHopfInvariantIsomorphismStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaPi32Eta2DefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
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


@dataclass(frozen=True)
class Toda54BracketUpToSignStatement:
  bracket: TodaBracket
  positive_value: Expression


@dataclass(frozen=True)
class TodaLemma55BracketContainsUpToSignStatement:
  bracket: TodaBracket
  positive_value: Expression


@dataclass(frozen=True)
class TodaLemma55SuspensionUpToSignStatement:
  left: Expression
  positive_value: Expression


@dataclass(frozen=True)
class Toda54IndeterminacyGeneratorStatement:
  bracket: TodaBracket
  generator: Expression


@dataclass(frozen=True)
class Toda36Lemma54SpecializationStatement:
  alpha: HomotopyElement
  beta: Expression
  alpha_star: HomotopyElement
  alpha_star_membership: HomotopyGroupMembershipStatement
  negative_bracket_membership: TodaBracketMembershipStatement


@dataclass(frozen=True)
class TodaLemma54DoubleSuspensionUpToSignStatement:
  left: Expression
  positive_value: Expression


@dataclass(frozen=True)
class TodaLemma54HopfOddMultipleStatement:
  alpha_star: HomotopyElement
  parameter: ScalarSymbol
  generator: HomotopyElement


@dataclass(frozen=True)
class TodaLemma54WhiteheadCorrectionDataStatement:
  whitehead_square: WhiteheadProduct
  sign_parameter: ScalarSymbol
  hopf_positive_value: Expression
  suspension_zero_relation: Relation


@dataclass(frozen=True)
class TodaLemma54Nu4BranchFormula:
  double_suspension_sign: int
  alpha_star_sign: int
  whitehead_coefficient_sign: int
  parameter_offset: int


@dataclass(frozen=True)
class TodaLemma54Nu4ConstructionStatement:
  alpha_star: HomotopyElement
  nu4: HomotopyElement
  parameter: ScalarSymbol
  whitehead_data: TodaLemma54WhiteheadCorrectionDataStatement
  double_suspension_value: Expression
  positive_branch: TodaLemma54Nu4BranchFormula
  negative_branch: TodaLemma54Nu4BranchFormula


@dataclass(frozen=True)
class TodaLemma54Statement:
  nu4: HomotopyElement
  membership: HomotopyGroupMembershipStatement
  hopf_relation: Relation
  double_suspension_relation: Relation
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


def toda_lemma54_literature_statements():
  toda_reference = {
    "author": "H. Toda",
    "title": (
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    "year": 1962,
  }

  return (
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda Proposition 1.3",
        locator="Proposition 1.3",
        **toda_reference,
      ),
      statement=(
        "-E{α,E^nβ,E^nγ}_n "
        "⊂ "
        "{Eα,E^(n+1)β,E^(n+1)γ}_(n+1)."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda (1.15)",
        locator="Equation (1.15)",
        **toda_reference,
      ),
      statement=(
        "{α,E^nβ,E^nγ}_n "
        "⊂ "
        "{α,E^m(E^(n-m)β),"
        "E^m(E^(n-m)γ)}_m."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda (3.2)",
        locator="Equation (3.2)",
        **toda_reference,
      ),
      statement=(
        "E: π_i(S^m) → π_(i+1)(S^(m+1)) "
        "is an isomorphism for i<2m-1 "
        "and is surjective for i=2m-1."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda Theorem 3.6",
        locator="Theorem 3.6",
        **toda_reference,
      ),
      statement=(
        "For the Lemma 5.4 specialization "
        "α=η₂, β=2ι₃, t=1, "
        "there exists α*∈π_7^4 such that "
        "2Eα* belongs to "
        "-{η₅,2ι₆,η₆}_3."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda (4.7)",
        locator="Equation (4.7)",
        **toda_reference,
      ),
      statement=(
        "For the Toda (5.4) bracket, "
        "the indeterminacy used here is "
        "η_n∘π_(n+3)^(n+1) "
        "+ π_(n+2)^n∘η_(n+2)."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda Proposition 5.3",
        locator="Proposition 5.3",
        **toda_reference,
      ),
      statement=(
        "π_(n+2)^n = Z/2{η_n²} "
        "for n≥2."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda (5.3)",
        locator="Equation (5.3)",
        **toda_reference,
      ),
      statement=(
        "ν′∈π_6^3, "
        "H(ν′)=η₅, and "
        "2ν′=η₃∘η₄∘η₅."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda (5.4)",
        locator="Equation (5.4)",
        **toda_reference,
      ),
      statement=(
        "{η_n,2ι_(n+1),η_(n+1)}_t "
        "= {±E^(n-3)ν′} "
        "for n≥3 and 0≤t≤n-2."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda (4.8)",
        locator="Equation (4.8)",
        **toda_reference,
      ),
      statement=(
        "The consequence used in "
        "Lemma 5.4 gives "
        "H(α*)=(2s+1)ι₇."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda Lemma 5.4 proof",
        locator="Lemma 5.4 proof",
        **toda_reference,
      ),
      statement=(
        "H[ι₄,ι₄]=(-1)^u 2ι₇ "
        "and E[ι₄,ι₄]=0."
      ),
    ),
  )


def toda_lemma54_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    hopf_relation = (
      premises[
        1
      ].conclusion
    )

    double_relation = (
      premises[
        2
      ].conclusion
    )

    nu4 = membership.element

    expected_nu4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
      ),
    )

    if (
      nu4
      != expected_nu4
    ):
      return False

    if (
      membership.group_dimension
      != 7
    ):
      return False

    if (
      membership.sphere_dimension
      != 4
    ):
      return False

    iota_7 = HomotopyElement(
      name="ι_7",
      dimension=7,
      generator=GeneratorSymbol(
        family="ι",
        index=7,
      ),
    )

    expected_hopf = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=nu4,
      ),
      rhs=iota_7,
      relation_type=RelationType.EQUALITY,
    )

    if (
      hopf_relation
      != expected_hopf
    ):
      return False

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    expected_double = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=Suspension(
          expression=nu4,
        ),
      ),
      rhs=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      relation_type=RelationType.EQUALITY,
    )

    return (
      double_relation
      == expected_double
    )

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    return (
      TodaLemma54Statement(
        nu4=membership.element,
        membership=membership,
        hopf_relation=(
          premises[
            1
          ].conclusion
        ),
        double_suspension_relation=(
          premises[
            2
          ].conclusion
        ),
        literature_statements=(
          toda_lemma54_literature_statements()
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 integration"
    ),
    description=(
      "Integrate the independently "
      "derived Phase 60-8 conclusions "
      "nu_4 in pi_7^4, "
      "H(nu_4)=iota_7, and "
      "2 E nu_4=E^2 nu-prime "
      "into the final Toda Lemma 5.4 "
      "statement. "
      "The aggregate also records the "
      "literature statements used "
      "throughout the Phase 60 proof."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma54_whitehead_correction_data_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    whitehead_square = (
      premises[
        0
      ].conclusion
    )

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    return (
      whitehead_square
      == WhiteheadProduct(
        left=iota_4,
        right=iota_4,
      )
    )

  def build_conclusion(
    premises,
  ):
    whitehead_square = (
      premises[
        0
      ].conclusion
    )

    u = ScalarSymbol(
      name="u",
    )

    iota_7 = HomotopyElement(
      name="ι_7",
      dimension=7,
      generator=GeneratorSymbol(
        family="ι",
        index=7,
      ),
    )

    return (
      TodaLemma54WhiteheadCorrectionDataStatement(
        whitehead_square=whitehead_square,
        sign_parameter=u,
        hopf_positive_value=Multiple(
          coefficient=2,
          expression=iota_7,
        ),
        suspension_zero_relation=Relation(
          lhs=Suspension(
            expression=whitehead_square,
          ),
          rhs=Zero(),
          relation_type=RelationType.ZERO,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 "
      "Whitehead correction data"
    ),
    description=(
      "For the Whitehead square "
      "[iota_4,iota_4], record the "
      "specific Lemma 5.4 facts "
      "H[iota_4,iota_4]="
      "(-1)^u 2 iota_7 and "
      "E[iota_4,iota_4]=0. "
      "The sign parameter u is retained "
      "structurally rather than solved. "
      "No generic Whitehead-product "
      "Hopf theorem or sign algebra "
      "is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          WhiteheadProduct
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma54_nu4_piecewise_construction_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_odd = (
      premises[
        0
      ].conclusion
    )

    double_statement = (
      premises[
        1
      ].conclusion
    )

    whitehead_data = (
      premises[
        2
      ].conclusion
    )

    alpha_star = (
      hopf_odd.alpha_star
    )

    if (
      double_statement.left
      != Multiple(
        coefficient=2,
        expression=Suspension(
          expression=alpha_star,
        ),
      )
    ):
      return False

    iota_7 = HomotopyElement(
      name="ι_7",
      dimension=7,
      generator=GeneratorSymbol(
        family="ι",
        index=7,
      ),
    )

    if (
      hopf_odd.generator
      != iota_7
    ):
      return False

    if (
      whitehead_data.hopf_positive_value
      != Multiple(
        coefficient=2,
        expression=iota_7,
      )
    ):
      return False

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    expected_whitehead = WhiteheadProduct(
      left=iota_4,
      right=iota_4,
    )

    if (
      whitehead_data.whitehead_square
      != expected_whitehead
    ):
      return False

    expected_zero = Relation(
      lhs=Suspension(
        expression=expected_whitehead,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      whitehead_data.suspension_zero_relation
      != expected_zero
    ):
      return False

    return isinstance(
      double_statement.positive_value,
      IteratedSuspension,
    )

  def build_conclusion(
    premises,
  ):
    hopf_odd = (
      premises[
        0
      ].conclusion
    )

    double_statement = (
      premises[
        1
      ].conclusion
    )

    whitehead_data = (
      premises[
        2
      ].conclusion
    )

    nu4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
      ),
    )

    return (
      TodaLemma54Nu4ConstructionStatement(
        alpha_star=hopf_odd.alpha_star,
        nu4=nu4,
        parameter=hopf_odd.parameter,
        whitehead_data=whitehead_data,
        double_suspension_value=(
          double_statement
          .positive_value
        ),
        positive_branch=(
          TodaLemma54Nu4BranchFormula(
            double_suspension_sign=1,
            alpha_star_sign=1,
            whitehead_coefficient_sign=-1,
            parameter_offset=0,
          )
        ),
        negative_branch=(
          TodaLemma54Nu4BranchFormula(
            double_suspension_sign=-1,
            alpha_star_sign=-1,
            whitehead_coefficient_sign=1,
            parameter_offset=1,
          )
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 "
      "piecewise nu_4 construction"
    ),
    description=(
      "Combine "
      "H(alpha-star)=(2s+1)iota_7, "
      "2 E alpha-star="
      "plus or minus E^2 nu-prime, "
      "H[iota_4,iota_4]="
      "(-1)^u 2 iota_7, and "
      "E[iota_4,iota_4]=0. "
      "If the double-suspension sign "
      "is positive, use "
      "nu_4=alpha-star-"
      "(-1)^u s[iota_4,iota_4]. "
      "If it is negative, use "
      "nu_4=-alpha-star+"
      "(-1)^u(s+1)[iota_4,iota_4]. "
      "Both branches are stored "
      "without introducing a generic "
      "sign solver or symbolic "
      "coefficient expression."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54HopfOddMultipleStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54DoubleSuspensionUpToSignStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54WhiteheadCorrectionDataStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma54_nu4_membership_inference_rule():
  def build_conclusion(
    premises,
  ):
    construction = (
      premises[
        0
      ].conclusion
    )

    return (
      HomotopyGroupMembershipStatement(
        element=construction.nu4,
        group_dimension=7,
        sphere_dimension=4,
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 "
      "nu_4 membership"
    ),
    description=(
      "The piecewise Whitehead-corrected "
      "element nu_4 belongs to pi_7^4."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Nu4ConstructionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
  )


def toda_lemma54_nu4_hopf_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    construction = (
      premises[
        0
      ].conclusion
    )

    if (
      construction.positive_branch
      != TodaLemma54Nu4BranchFormula(
        double_suspension_sign=1,
        alpha_star_sign=1,
        whitehead_coefficient_sign=-1,
        parameter_offset=0,
      )
    ):
      return False

    return (
      construction.negative_branch
      == TodaLemma54Nu4BranchFormula(
        double_suspension_sign=-1,
        alpha_star_sign=-1,
        whitehead_coefficient_sign=1,
        parameter_offset=1,
      )
    )

  def build_conclusion(
    premises,
  ):
    construction = (
      premises[
        0
      ].conclusion
    )

    iota_7 = HomotopyElement(
      name="ι_7",
      dimension=7,
      generator=GeneratorSymbol(
        family="ι",
        index=7,
      ),
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=construction.nu4,
      ),
      rhs=iota_7,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 "
      "nu_4 Hopf correction"
    ),
    description=(
      "For either stored sign branch "
      "of the Lemma 5.4 Whitehead "
      "correction, "
      "H(alpha-star)=(2s+1)iota_7 "
      "and "
      "H[iota_4,iota_4]="
      "(-1)^u 2 iota_7 "
      "give H(nu_4)=iota_7. "
      "This is a theorem-specific "
      "piecewise consequence."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Nu4ConstructionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma54_nu4_double_suspension_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    construction = (
      premises[
        0
      ].conclusion
    )

    suspension_zero = (
      construction
      .whitehead_data
      .suspension_zero_relation
    )

    expected_zero = Relation(
      lhs=Suspension(
        expression=(
          construction
          .whitehead_data
          .whitehead_square
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      suspension_zero
      == expected_zero
    )

  def build_conclusion(
    premises,
  ):
    construction = (
      premises[
        0
      ].conclusion
    )

    return Relation(
      lhs=Multiple(
        coefficient=2,
        expression=Suspension(
          expression=construction.nu4,
        ),
      ),
      rhs=(
        construction
        .double_suspension_value
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 "
      "nu_4 double suspension"
    ),
    description=(
      "In both sign branches of the "
      "Whitehead correction, "
      "E[iota_4,iota_4]=0 removes "
      "the correction term after "
      "suspension. "
      "Combining this with "
      "2 E alpha-star="
      "plus or minus E^2 nu-prime "
      "and the branch-dependent "
      "choice of nu_4 gives "
      "2 E nu_4=E^2 nu-prime."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Nu4ConstructionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma54_pi6_5_finite_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    higher_relation = (
      statement
      .higher_eta_group_relation
    )

    if not isinstance(
      higher_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      higher_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      higher_relation.rhs.order
      != 2
    ):
      return False

    n = (
      higher_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      sphere_dimension=n,
    )

    if (
      higher_relation.lhs
      != expected_group
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      higher_relation.rhs.generator
      == eta_n
    )

  def build_conclusion(
    premises,
  ):
    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_5,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 "
      "pi_6^5 finite-cyclic specialization"
    ),
    description=(
      "Specialize the independently "
      "derived Proposition 5.1 "
      "higher eta-family result "
      "pi_(n+1)^n=Z/2{eta_n} "
      "to n=5, giving "
      "pi_6^5=Z/2{eta_5}. "
      "This concrete result is used "
      "only for the Toda (4.8) "
      "parity argument in Lemma 5.4."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_48_lemma54_hopf_odd_multiple_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    theorem36 = (
      premises[
        0
      ].conclusion
    )

    double_statement = (
      premises[
        1
      ].conclusion
    )

    nu_prime_hopf = (
      premises[
        2
      ].conclusion
    )

    pi6_5_relation = (
      premises[
        3
      ].conclusion
    )

    alpha_star = (
      theorem36
      .alpha_star
    )

    if (
      theorem36
      .alpha_star_membership
      .element
      != alpha_star
    ):
      return False

    if (
      theorem36
      .alpha_star_membership
      .group_dimension
      != 7
    ):
      return False

    if (
      theorem36
      .alpha_star_membership
      .sphere_dimension
      != 4
    ):
      return False

    expected_double_left = Multiple(
      coefficient=2,
      expression=Suspension(
        expression=alpha_star,
      ),
    )

    if (
      double_statement.left
      != expected_double_left
    ):
      return False

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    expected_double_value = (
      IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      )
    )

    if (
      double_statement.positive_value
      != expected_double_value
    ):
      return False

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    expected_hopf = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=nu_prime,
      ),
      rhs=eta_5,
      relation_type=RelationType.EQUALITY,
    )

    if (
      nu_prime_hopf
      != expected_hopf
    ):
      return False

    expected_pi6_5 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_5,
      ),
      relation_type=RelationType.EQUALITY,
    )

    return (
      pi6_5_relation
      == expected_pi6_5
    )

  def build_conclusion(
    premises,
  ):
    theorem36 = (
      premises[
        0
      ].conclusion
    )

    s = ScalarSymbol(
      name="s",
    )

    iota_7 = HomotopyElement(
      name="ι_7",
      dimension=7,
      generator=GeneratorSymbol(
        family="ι",
        index=7,
      ),
    )

    return (
      TodaLemma54HopfOddMultipleStatement(
        alpha_star=(
          theorem36.alpha_star
        ),
        parameter=s,
        generator=iota_7,
      )
    )

  return InferenceRule(
    name=(
      "Toda 4.8 "
      "Lemma 5.4 Hopf odd multiple"
    ),
    description=(
      "For the Lemma 5.4 alpha-star, "
      "Phase 58 gives "
      "H(nu-prime)=eta_5 and the "
      "independently derived group "
      "pi_6^5=Z/2{eta_5} shows that "
      "nu-prime cannot be divisible "
      "by two. "
      "Phase 60-6 gives "
      "2 E alpha-star="
      "plus or minus E^2 nu-prime, "
      "so E^2 nu-prime is divisible "
      "by two. "
      "The Toda (4.8) consequence "
      "required in Lemma 5.4 therefore "
      "makes the Hopf invariant of "
      "alpha-star an odd multiple of "
      "iota_7. "
      "Represent that odd coefficient "
      "as 2s+1 without adding generic "
      "divisibility or parity solving."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda36Lemma54SpecializationStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54DoubleSuspensionUpToSignStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma54_eta6_twice_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    higher_relation = (
      statement
      .higher_eta_group_relation
    )

    if not isinstance(
      higher_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      higher_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      higher_relation.rhs.order
      != 2
    ):
      return False

    n = (
      higher_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      sphere_dimension=n,
    )

    if (
      higher_relation.lhs
      != expected_group
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      higher_relation.rhs.generator
      == eta_n
    )

  def build_conclusion(
    premises,
  ):
    eta_6 = HomotopyElement(
      name="η₆",
      dimension=6,
      source=7,
      target=6,
      generator=GeneratorSymbol(
        family="η",
        index=6,
      ),
    )

    return Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_6,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 "
      "eta_6 twice zero"
    ),
    description=(
      "Specialize the independently "
      "derived Proposition 5.1 "
      "higher eta-family result "
      "pi_(n+1)^n=Z/2{eta_n} "
      "to n=6 and derive "
      "2 eta_6=0. "
      "This is the exact order-two "
      "premise required by the "
      "Theorem 3.6 specialization."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_36_lemma54_specialization_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop51 = (
      premises[
        0
      ].conclusion
    )

    two_eta3_zero = (
      premises[
        1
      ].conclusion
    )

    two_eta6_zero = (
      premises[
        2
      ].conclusion
    )

    if not isinstance(
      prop51,
      TodaProp51FiniteDimensionalStatement,
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    expected_eta3_zero = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_3,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      two_eta3_zero
      != expected_eta3_zero
    ):
      return False

    eta_6 = HomotopyElement(
      name="η₆",
      dimension=6,
      source=7,
      target=6,
      generator=GeneratorSymbol(
        family="η",
        index=6,
      ),
    )

    expected_eta6_zero = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_6,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      two_eta6_zero
      == expected_eta6_zero
    )

  def build_conclusion(
    premises,
  ):
    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    iota_6 = HomotopyElement(
      name="ι_6",
      dimension=6,
      generator=GeneratorSymbol(
        family="ι",
        index=6,
      ),
    )

    eta_6 = HomotopyElement(
      name="η₆",
      dimension=6,
      source=7,
      target=6,
      generator=GeneratorSymbol(
        family="η",
        index=6,
      ),
    )

    alpha_star = HomotopyElement(
      name="α*",
      dimension=7,
      source=7,
      target=4,
    )

    alpha_star_membership = (
      HomotopyGroupMembershipStatement(
        element=alpha_star,
        group_dimension=7,
        sphere_dimension=4,
      )
    )

    target_bracket = TodaBracket(
      first=eta_5,
      second=Multiple(
        coefficient=2,
        expression=iota_6,
      ),
      third=eta_6,
      index=3,
    )

    negative_bracket_membership = (
      TodaBracketMembershipStatement(
        element=Multiple(
          coefficient=-2,
          expression=Suspension(
            expression=alpha_star,
          ),
        ),
        bracket=target_bracket,
      )
    )

    return (
      Toda36Lemma54SpecializationStatement(
        alpha=eta_2,
        beta=Multiple(
          coefficient=2,
          expression=iota_3,
        ),
        alpha_star=alpha_star,
        alpha_star_membership=(
          alpha_star_membership
        ),
        negative_bracket_membership=(
          negative_bracket_membership
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Theorem 3.6 "
      "Lemma 5.4 specialization"
    ),
    description=(
      "Specialize Toda Theorem 3.6 "
      "to alpha=eta_2, "
      "beta=2 iota_3, "
      "n=2, k=1, h=1, m=3, "
      "ell=1, and t=1. "
      "The derived relation "
      "2 eta_3=0 verifies "
      "beta composed with E alpha=0, "
      "and the derived relation "
      "2 eta_6=0 removes the second "
      "bracket term. "
      "The sign exponent is "
      "km+kt+t=5, so there exists "
      "alpha-star in pi_7^4 with "
      "2 E alpha-star in minus "
      "{eta_5,2 iota_6,eta_6}_3. "
      "The negative bracket membership "
      "is represented equivalently as "
      "-2 E alpha-star belonging to "
      "the positive bracket."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_54_n5_t3_specialization_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    bracket = statement.bracket

    if not isinstance(
      bracket.index,
      ScalarSymbol,
    ):
      return False

    if not isinstance(
      bracket.first,
      HomotopyElement,
    ):
      return False

    n = bracket.first.dimension

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    if (
      bracket.first
      != expected_eta_n
    ):
      return False

    expected_iota = HomotopyElement(
      name="ι_(n+1)",
      dimension=ScalarSum(
        left=n,
        right=1,
      ),
      generator=GeneratorSymbol(
        family="ι",
        index=ScalarSum(
          left=n,
          right=1,
        ),
      ),
    )

    if (
      bracket.second
      != Multiple(
        coefficient=2,
        expression=expected_iota,
      )
    ):
      return False

    expected_eta_n_plus_one = (
      HomotopyElement(
        name="η_(n+1)",
        dimension=ScalarSum(
          left=n,
          right=1,
        ),
        source=ScalarSum(
          left=n,
          right=2,
        ),
        target=ScalarSum(
          left=n,
          right=1,
        ),
        generator=GeneratorSymbol(
          family="η",
          index=ScalarSum(
            left=n,
            right=1,
          ),
        ),
      )
    )

    if (
      bracket.third
      != expected_eta_n_plus_one
    ):
      return False

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    expected_value = IteratedSuspension(
      expression=nu_prime,
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
    )

    return (
      statement.positive_value
      == expected_value
    )

  def build_conclusion(
    premises,
  ):
    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    iota_6 = HomotopyElement(
      name="ι_6",
      dimension=6,
      generator=GeneratorSymbol(
        family="ι",
        index=6,
      ),
    )

    eta_6 = HomotopyElement(
      name="η₆",
      dimension=6,
      source=7,
      target=6,
      generator=GeneratorSymbol(
        family="η",
        index=6,
      ),
    )

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    return (
      Toda54BracketUpToSignStatement(
        bracket=TodaBracket(
          first=eta_5,
          second=Multiple(
            coefficient=2,
            expression=iota_6,
          ),
          third=eta_6,
          index=3,
        ),
        positive_value=IteratedSuspension(
          expression=nu_prime,
          exponent=2,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.4 "
      "n=5 t=3 specialization"
    ),
    description=(
      "Specialize the independently "
      "derived symbolic Toda (5.4) "
      "positive-index statement to "
      "n=5 and t=3, obtaining "
      "{eta_5,2 iota_6,eta_6}_3 "
      "equals plus or minus E^2 "
      "nu-prime. "
      "No generic symbolic "
      "substitution engine is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda54BracketUpToSignStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma54_double_suspension_up_to_sign_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    theorem36 = (
      premises[
        0
      ].conclusion
    )

    bracket_value = (
      premises[
        1
      ].conclusion
    )

    membership = (
      theorem36
      .negative_bracket_membership
    )

    if (
      membership.bracket
      != bracket_value.bracket
    ):
      return False

    expected_element = Multiple(
      coefficient=-2,
      expression=Suspension(
        expression=(
          theorem36.alpha_star
        ),
      ),
    )

    return (
      membership.element
      == expected_element
    )

  def build_conclusion(
    premises,
  ):
    theorem36 = (
      premises[
        0
      ].conclusion
    )

    bracket_value = (
      premises[
        1
      ].conclusion
    )

    return (
      TodaLemma54DoubleSuspensionUpToSignStatement(
        left=Multiple(
          coefficient=2,
          expression=Suspension(
            expression=(
              theorem36.alpha_star
            ),
          ),
        ),
        positive_value=(
          bracket_value
          .positive_value
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.4 "
      "double suspension up to sign"
    ),
    description=(
      "Combine the Theorem 3.6 "
      "specialization "
      "-2 E alpha-star in "
      "{eta_5,2 iota_6,eta_6}_3 "
      "with the independently derived "
      "Toda (5.4) value set "
      "{eta_5,2 iota_6,eta_6}_3 "
      "={plus or minus E^2 nu-prime}. "
      "Since this value set is sign "
      "symmetric, derive "
      "2 E alpha-star="
      "plus or minus E^2 nu-prime. "
      "No generic sign solver or "
      "set-membership algebra is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda36Lemma54SpecializationStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda54BracketUpToSignStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_54_t_ge_1_indeterminacy_eta_cube_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop53 = (
      premises[
        0
      ].conclusion
    )

    n_range = (
      premises[
        1
      ].conclusion
    )

    t_range = (
      premises[
        2
      ].conclusion
    )

    if not isinstance(
      prop53,
      TodaProp53FiniteDimensionalStatement,
    ):
      return False

    n = n_range.left
    t = t_range.left

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if not isinstance(
      t,
      ScalarSymbol,
    ):
      return False

    if (
      n_range.right
      != 3
    ):
      return False

    return (
      t_range.right
      == 1
    )

  def build_conclusion(
    premises,
  ):
    n_range = (
      premises[
        1
      ].conclusion
    )

    t_range = (
      premises[
        2
      ].conclusion
    )

    n = n_range.left
    t = t_range.left

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    n_plus_two = ScalarSum(
      left=n,
      right=2,
    )

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=n_plus_one,
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    eta_n_plus_one = HomotopyElement(
      name="η_(n+1)",
      dimension=n_plus_one,
      source=n_plus_two,
      target=n_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_one,
      ),
    )

    eta_n_plus_two = HomotopyElement(
      name="η_(n+2)",
      dimension=n_plus_two,
      source=ScalarSum(
        left=n,
        right=3,
      ),
      target=n_plus_two,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_two,
      ),
    )

    iota_n_plus_one = HomotopyElement(
      name="ι_(n+1)",
      dimension=n_plus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_plus_one,
      ),
    )

    bracket = TodaBracket(
      first=eta_n,
      second=Multiple(
        coefficient=2,
        expression=iota_n_plus_one,
      ),
      third=eta_n_plus_one,
      index=t,
    )

    eta_cube = Composition(
      left=eta_n,
      right=Composition(
        left=eta_n_plus_one,
        right=eta_n_plus_two,
      ),
    )

    return (
      Toda54IndeterminacyGeneratorStatement(
        bracket=bracket,
        generator=eta_cube,
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.4 t>=1 "
      "indeterminacy generated by "
      "eta triple composition"
    ),
    description=(
      "For n>=3 and t>=1, "
      "specialize Toda (4.7) to "
      "{eta_n, 2 iota_(n+1), "
      "eta_(n+1)}_t. "
      "Using the independently derived "
      "Toda Proposition 5.3 "
      "finite-dimensional result, "
      "the two indeterminacy summands "
      "generate the subgroup generated "
      "by eta_n composed with "
      "eta_(n+1) composed with "
      "eta_(n+2). "
      "This is a theorem-specific "
      "indeterminacy consequence and "
      "does not introduce generic "
      "Toda-bracket coset algebra."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp53FiniteDimensionalStatement
        ),
      ),
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
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_54_nu_prime_triple_eta_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    double_relation = (
      premises[
        0
      ].conclusion
    )

    n_range = (
      premises[
        1
      ].conclusion
    )

    n = n_range.left

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      n_range.right
      != 3
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    expected_relation = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=nu_prime,
      ),
      rhs=Composition(
        left=eta_3,
        right=Composition(
          left=eta_4,
          right=eta_5,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

    return (
      double_relation
      == expected_relation
    )

  def build_conclusion(
    premises,
  ):
    double_relation = (
      premises[
        0
      ].conclusion
    )

    n_range = (
      premises[
        1
      ].conclusion
    )

    n = n_range.left

    nu_prime = (
      double_relation
      .lhs
      .expression
    )

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    n_plus_two = ScalarSum(
      left=n,
      right=2,
    )

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=n_plus_one,
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    eta_n_plus_one = HomotopyElement(
      name="η_(n+1)",
      dimension=n_plus_one,
      source=n_plus_two,
      target=n_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_one,
      ),
    )

    eta_n_plus_two = HomotopyElement(
      name="η_(n+2)",
      dimension=n_plus_two,
      source=ScalarSum(
        left=n,
        right=3,
      ),
      target=n_plus_two,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_two,
      ),
    )

    return Relation(
      lhs=Multiple(
        coefficient=2,
        expression=IteratedSuspension(
          expression=nu_prime,
          exponent=ScalarSum(
            left=n,
            right=ScalarProduct(
              left=-1,
              right=3,
            ),
          ),
        ),
      ),
      rhs=Composition(
        left=eta_n,
        right=Composition(
          left=eta_n_plus_one,
          right=eta_n_plus_two,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 5.4 nu-prime "
      "higher triple eta transport"
    ),
    description=(
      "Suspend the independently "
      "derived Toda (5.3) relation "
      "2 nu-prime="
      "eta_3 eta_4 eta_5 "
      "by n-3 suspensions. "
      "The theorem-specific eta-family "
      "transport gives "
      "2 E^(n-3) nu-prime="
      "eta_n eta_(n+1) eta_(n+2). "
      "No generic suspension-of-"
      "composition normalization "
      "is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_54_indeterminacy_double_nu_prime_generator_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    indeterminacy = (
      premises[
        0
      ].conclusion
    )

    transport = (
      premises[
        1
      ].conclusion
    )

    if (
      transport.rhs
      != indeterminacy.generator
    ):
      return False

    if not isinstance(
      transport.lhs,
      Multiple,
    ):
      return False

    if (
      transport.lhs.coefficient
      != 2
    ):
      return False

    return isinstance(
      transport.lhs.expression,
      IteratedSuspension,
    )

  def build_conclusion(
    premises,
  ):
    indeterminacy = (
      premises[
        0
      ].conclusion
    )

    transport = (
      premises[
        1
      ].conclusion
    )

    return (
      Toda54IndeterminacyGeneratorStatement(
        bracket=indeterminacy.bracket,
        generator=transport.lhs,
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.4 indeterminacy "
      "double nu-prime generator bridge"
    ),
    description=(
      "If the Toda (5.4) bracket "
      "indeterminacy is generated by "
      "eta_n eta_(n+1) eta_(n+2), "
      "and the independently derived "
      "Toda (5.3) transport identifies "
      "that element with "
      "2 E^(n-3) nu-prime, "
      "rewrite the theorem-specific "
      "indeterminacy generator as "
      "2 E^(n-3) nu-prime."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda54IndeterminacyGeneratorStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_54_nu_prime_bracket_inclusion_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    n_range = (
      premises[
        1
      ].conclusion
    )

    t_lower_range = (
      premises[
        2
      ].conclusion
    )

    t_upper_range = (
      premises[
        3
      ].conclusion
    )

    n = n_range.left
    t = t_lower_range.left

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if not isinstance(
      t,
      ScalarSymbol,
    ):
      return False

    if (
      n_range.right
      != 3
    ):
      return False

    if (
      t_lower_range.right
      != 1
    ):
      return False

    expected_t_upper_left = ScalarSum(
      left=n,
      right=-2,
    )

    if (
      t_upper_range.left
      != expected_t_upper_left
    ):
      return False

    if (
      t_upper_range.right
      != t
    ):
      return False

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    if (
      specialization.nu_prime
      != nu_prime
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      specialization.alpha
      != eta_3
    ):
      return False

    if (
      specialization.lemma52_index
      != 4
    ):
      return False

    membership = (
      specialization
      .bracket_membership
    )

    if (
      membership.element
      != nu_prime
    ):
      return False

    bracket = membership.bracket

    if (
      bracket.index
      != 1
    ):
      return False

    if (
      bracket.first
      != eta_3
    ):
      return False

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    if (
      bracket.second
      != Multiple(
        coefficient=2,
        expression=iota_4,
      )
    ):
      return False

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    return (
      bracket.third
      == eta_4
    )

  def build_conclusion(
    premises,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    n_range = (
      premises[
        1
      ].conclusion
    )

    t_lower_range = (
      premises[
        2
      ].conclusion
    )

    n = n_range.left
    t = t_lower_range.left

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    n_plus_two = ScalarSum(
      left=n,
      right=2,
    )

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=n_plus_one,
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    eta_n_plus_one = HomotopyElement(
      name="η_(n+1)",
      dimension=n_plus_one,
      source=n_plus_two,
      target=n_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_one,
      ),
    )

    iota_n_plus_one = HomotopyElement(
      name="ι_(n+1)",
      dimension=n_plus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_plus_one,
      ),
    )

    target_bracket = TodaBracket(
      first=eta_n,
      second=Multiple(
        coefficient=2,
        expression=iota_n_plus_one,
      ),
      third=eta_n_plus_one,
      index=t,
    )

    suspended_nu_prime = IteratedSuspension(
      expression=(
        specialization
        .nu_prime
      ),
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
    )

    return TodaBracketMembershipStatement(
      element=suspended_nu_prime,
      bracket=target_bracket,
    )

  return InferenceRule(
    name=(
      "Toda 5.4 "
      "nu-prime suspended bracket inclusion"
    ),
    description=(
      "Starting from the independently "
      "recognized Toda (5.3) membership "
      "nu-prime in "
      "{eta_3, 2 iota_4, eta_4}_1, "
      "apply the minimum consequence "
      "of Toda Proposition 1.3 and "
      "Toda (1.15) required for "
      "Toda (5.4). "
      "For n>=3 and "
      "1<=t<=n-2, derive "
      "E^(n-3) nu-prime in "
      "{eta_n, 2 iota_(n+1), "
      "eta_(n+1)}_t. "
      "This rule does not implement "
      "generic bracket suspension or "
      "the full Proposition 1.3."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda53NuPrimeBracketSpecializationStatement
        ),
      ),
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
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_54_t_ge_1_up_to_sign_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    indeterminacy = (
      premises[
        0
      ].conclusion
    )

    membership = (
      premises[
        1
      ].conclusion
    )

    if (
      indeterminacy.bracket
      != membership.bracket
    ):
      return False

    bracket = membership.bracket

    if not isinstance(
      bracket.index,
      ScalarSymbol,
    ):
      return False

    expected_generator = Multiple(
      coefficient=2,
      expression=membership.element,
    )

    return (
      indeterminacy.generator
      == expected_generator
    )

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[
        1
      ].conclusion
    )

    return (
      Toda54BracketUpToSignStatement(
        bracket=membership.bracket,
        positive_value=membership.element,
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.4 t>=1 "
      "up-to-sign integration"
    ),
    description=(
      "For the Toda (5.4) bracket, "
      "combine the independently "
      "derived indeterminacy subgroup "
      "generated by "
      "2 E^(n-3) nu-prime with the "
      "independently derived membership "
      "of E^(n-3) nu-prime. "
      "The theorem-specific consequence "
      "is that the bracket has values "
      "plus or minus E^(n-3) nu-prime. "
      "No generic coset algebra is "
      "introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda54IndeterminacyGeneratorStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaBracketMembershipStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_32_phase60_suspension_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    n_range = (
      premises[
        0
      ].conclusion
    )

    n = n_range.left

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    return (
      n_range.right
      == 3
    )

  def build_conclusion(
    premises,
  ):
    n_range = (
      premises[
        0
      ].conclusion
    )

    n = n_range.left

    source_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    )

    target_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=3,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    )

    return (
      TodaSuspensionSurjectiveStatement(
        map=TodaSuspensionMap(
          source_group=source_group,
          target_group=target_group,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda 3.2 Phase 60 "
      "suspension surjectivity"
    ),
    description=(
      "For n>=3, specialize Toda (3.2) "
      "to the suspension "
      "E:pi_(n+2)^n to "
      "pi_(n+3)^(n+1). "
      "For n=3 this is the boundary "
      "surjective case, while for n>3 "
      "it is an isomorphism and hence "
      "surjective. "
      "Only the surjectivity consequence "
      "needed for the Toda (5.4) "
      "t=0 bridge is represented."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_54_t0_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    indexed_statement = (
      premises[
        0
      ].conclusion
    )

    surjectivity = (
      premises[
        1
      ].conclusion
    )

    n_range = (
      premises[
        2
      ].conclusion
    )

    bracket = (
      indexed_statement
      .bracket
    )

    n = n_range.left

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      n_range.right
      != 3
    ):
      return False

    if not isinstance(
      bracket.index,
      ScalarSymbol,
    ):
      return False

    expected_source = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=3,
      ),
      sphere_dimension=ScalarSum(
        left=n,
        right=1,
      ),
    )

    suspension_map = (
      surjectivity.map
    )

    if (
      suspension_map.source_group
      != expected_source
    ):
      return False

    if (
      suspension_map.target_group
      != expected_target
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    if (
      bracket.first
      != eta_n
    ):
      return False

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    iota_n_plus_one = HomotopyElement(
      name="ι_(n+1)",
      dimension=n_plus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_plus_one,
      ),
    )

    if (
      bracket.second
      != Multiple(
        coefficient=2,
        expression=iota_n_plus_one,
      )
    ):
      return False

    eta_n_plus_one = HomotopyElement(
      name="η_(n+1)",
      dimension=n_plus_one,
      source=ScalarSum(
        left=n,
        right=2,
      ),
      target=n_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_one,
      ),
    )

    if (
      bracket.third
      != eta_n_plus_one
    ):
      return False

    expected_value = IteratedSuspension(
      expression=HomotopyElement(
        name="ν′",
        dimension=3,
        source=6,
        target=3,
        generator=GeneratorSymbol(
          family="ν",
          decoration="′",
        ),
      ),
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
    )

    return (
      indexed_statement.positive_value
      == expected_value
    )

  def build_conclusion(
    premises,
  ):
    indexed_statement = (
      premises[
        0
      ].conclusion
    )

    indexed_bracket = (
      indexed_statement
      .bracket
    )

    unindexed_bracket = TodaBracket(
      first=indexed_bracket.first,
      second=indexed_bracket.second,
      third=indexed_bracket.third,
    )

    return (
      Toda54BracketUpToSignStatement(
        bracket=unindexed_bracket,
        positive_value=(
          indexed_statement
          .positive_value
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.4 t=0 bridge"
    ),
    description=(
      "Use Toda (1.15) to compare the "
      "positive-index Toda bracket with "
      "the unindexed t=0 bracket. "
      "Toda (3.2) gives surjectivity of "
      "E:pi_(n+2)^n to "
      "pi_(n+3)^(n+1) for n>=3, "
      "so the relevant indeterminacy "
      "groups agree. "
      "Hence the already derived "
      "Toda (5.4) up-to-sign value set "
      "for positive t gives the same "
      "up-to-sign value set for t=0. "
      "No generic indexed-bracket "
      "equivalence framework is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda54BracketUpToSignStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionSurjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma55_alpha_star_bracket_inclusion_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    theorem36 = (
      premises[
        0
      ].conclusion
    )

    beta_membership = (
      premises[
        1
      ].conclusion
    )

    zero_relation = (
      premises[
        2
      ].conclusion
    )

    t_range = (
      premises[
        3
      ].conclusion
    )

    alpha_star = (
      theorem36
      .alpha_star
    )

    expected_alpha_star_membership = (
      HomotopyGroupMembershipStatement(
        element=alpha_star,
        group_dimension=7,
        sphere_dimension=4,
      )
    )

    if (
      theorem36.alpha_star_membership
      != expected_alpha_star_membership
    ):
      return False

    beta = beta_membership.element

    if not isinstance(
      beta,
      HomotopyElement,
    ):
      return False

    group_dimension = (
      beta_membership
      .group_dimension
    )

    if not isinstance(
      group_dimension,
      ScalarSum,
    ):
      return False

    if (
      group_dimension.right
      != 2
    ):
      return False

    t = group_dimension.left

    if not isinstance(
      t,
      ScalarSymbol,
    ):
      return False

    m = (
      beta_membership
      .sphere_dimension
    )

    if not isinstance(
      m,
      ScalarSymbol,
    ):
      return False

    if (
      beta.dimension
      != group_dimension
    ):
      return False

    if (
      beta.source
      != group_dimension
    ):
      return False

    if (
      beta.target
      != m
    ):
      return False

    t_plus_two = ScalarSum(
      left=t,
      right=2,
    )

    t_plus_three = ScalarSum(
      left=t,
      right=3,
    )

    eta_t_plus_two = HomotopyElement(
      name="η_(t+2)",
      dimension=t_plus_two,
      source=t_plus_three,
      target=t_plus_two,
      generator=GeneratorSymbol(
        family="η",
        index=t_plus_two,
      ),
    )

    expected_zero_relation = Relation(
      lhs=Composition(
        left=beta,
        right=eta_t_plus_two,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      zero_relation
      != expected_zero_relation
    ):
      return False

    return (
      t_range
      == ScalarGreaterEqualStatement(
        left=t,
        right=1,
      )
    )

  def build_conclusion(
    premises,
  ):
    theorem36 = (
      premises[
        0
      ].conclusion
    )

    beta_membership = (
      premises[
        1
      ].conclusion
    )

    beta = (
      beta_membership
      .element
    )

    group_dimension = (
      beta_membership
      .group_dimension
    )

    t = (
      group_dimension
      .left
    )

    m = (
      beta_membership
      .sphere_dimension
    )

    m_plus_two = ScalarSum(
      left=m,
      right=2,
    )

    m_plus_three = ScalarSum(
      left=m,
      right=3,
    )

    t_plus_five = ScalarSum(
      left=t,
      right=5,
    )

    t_plus_six = ScalarSum(
      left=t,
      right=6,
    )

    eta_m_plus_two = HomotopyElement(
      name="η_(m+2)",
      dimension=m_plus_two,
      source=m_plus_three,
      target=m_plus_two,
      generator=GeneratorSymbol(
        family="η",
        index=m_plus_two,
      ),
    )

    eta_t_plus_five = HomotopyElement(
      name="η_(t+5)",
      dimension=t_plus_five,
      source=t_plus_six,
      target=t_plus_five,
      generator=GeneratorSymbol(
        family="η",
        index=t_plus_five,
      ),
    )

    bracket = TodaBracket(
      first=eta_m_plus_two,
      second=IteratedSuspension(
        expression=beta,
        exponent=3,
      ),
      third=eta_t_plus_five,
      index=3,
    )

    positive_value = Composition(
      left=IteratedSuspension(
        expression=beta,
        exponent=2,
      ),
      right=IteratedSuspension(
        expression=(
          theorem36
          .alpha_star
        ),
        exponent=t,
      ),
    )

    return (
      TodaLemma55BracketContainsUpToSignStatement(
        bracket=bracket,
        positive_value=positive_value,
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.5 "
      "alpha-star bracket inclusion"
    ),
    description=(
      "For the alpha-star obtained in "
      "the proof of Toda Lemma 5.4, "
      "if beta belongs to pi_(t+2)^m, "
      "beta composed with eta_(t+2) "
      "is zero, and t>=1, then "
      "{eta_(m+2), E^3 beta, "
      "eta_(t+5)}_3 contains "
      "plus or minus "
      "E^2 beta composed with "
      "E^t alpha-star. "
      "This records only the "
      "Lemma 5.5 consequence used in "
      "the source proof and does not "
      "formalize full Toda Theorem 3.6."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda36Lemma54SpecializationStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma55_nu4_suspension_correction_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    construction = (
      premises[
        0
      ].conclusion
    )

    t_range = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      t_range.left,
      ScalarSymbol,
    ):
      return False

    t = t_range.left

    if (
      t_range
      != ScalarGreaterEqualStatement(
        left=t,
        right=1,
      )
    ):
      return False

    if (
      construction.positive_branch
      != TodaLemma54Nu4BranchFormula(
        double_suspension_sign=1,
        alpha_star_sign=1,
        whitehead_coefficient_sign=-1,
        parameter_offset=0,
      )
    ):
      return False

    if (
      construction.negative_branch
      != TodaLemma54Nu4BranchFormula(
        double_suspension_sign=-1,
        alpha_star_sign=-1,
        whitehead_coefficient_sign=1,
        parameter_offset=1,
      )
    ):
      return False

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    expected_whitehead_square = (
      WhiteheadProduct(
        left=iota_4,
        right=iota_4,
      )
    )

    if (
      construction
      .whitehead_data
      .whitehead_square
      != expected_whitehead_square
    ):
      return False

    expected_suspension_zero = Relation(
      lhs=Suspension(
        expression=expected_whitehead_square,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      construction
      .whitehead_data
      .suspension_zero_relation
      == expected_suspension_zero
    )

  def build_conclusion(
    premises,
  ):
    construction = (
      premises[
        0
      ].conclusion
    )

    t_range = (
      premises[
        1
      ].conclusion
    )

    t = t_range.left

    return (
      TodaLemma55SuspensionUpToSignStatement(
        left=IteratedSuspension(
          expression=construction.nu4,
          exponent=t,
        ),
        positive_value=IteratedSuspension(
          expression=construction.alpha_star,
          exponent=t,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.5 "
      "nu_4 suspension correction"
    ),
    description=(
      "For t>=1, the Whitehead "
      "correction in the Lemma 5.4 "
      "construction of nu_4 disappears "
      "after suspension because "
      "E[iota_4,iota_4]=0. "
      "The positive construction branch "
      "gives E^t nu_4=E^t alpha-star, "
      "and the negative branch gives "
      "E^t nu_4=-E^t alpha-star. "
      "The combined consequence is "
      "stored up to sign without "
      "introducing generic Whitehead "
      "correction or sign algebra."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Nu4ConstructionStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma55_alpha_star_to_nu4_composition_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    bracket_statement = (
      premises[
        0
      ].conclusion
    )

    suspension_statement = (
      premises[
        1
      ].conclusion
    )

    positive_value = (
      bracket_statement
      .positive_value
    )

    if not isinstance(
      positive_value,
      Composition,
    ):
      return False

    e2_beta = (
      positive_value
      .left
    )

    et_alpha_star = (
      positive_value
      .right
    )

    if not isinstance(
      e2_beta,
      IteratedSuspension,
    ):
      return False

    if (
      e2_beta.exponent
      != 2
    ):
      return False

    if not isinstance(
      et_alpha_star,
      IteratedSuspension,
    ):
      return False

    if not isinstance(
      suspension_statement.left,
      IteratedSuspension,
    ):
      return False

    et_nu4 = (
      suspension_statement
      .left
    )

    if not isinstance(
      suspension_statement
      .positive_value,
      IteratedSuspension,
    ):
      return False

    suspension_et_alpha_star = (
      suspension_statement
      .positive_value
    )

    if (
      et_alpha_star
      != suspension_et_alpha_star
    ):
      return False

    if (
      et_nu4.exponent
      != et_alpha_star.exponent
    ):
      return False

    if (
      suspension_et_alpha_star.exponent
      != et_alpha_star.exponent
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    bracket_statement = (
      premises[
        0
      ].conclusion
    )

    suspension_statement = (
      premises[
        1
      ].conclusion
    )

    positive_value = (
      bracket_statement
      .positive_value
    )

    return (
      TodaLemma55BracketContainsUpToSignStatement(
        bracket=(
          bracket_statement
          .bracket
        ),
        positive_value=Composition(
          left=positive_value.left,
          right=(
            suspension_statement
            .left
          ),
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.5 "
      "alpha-star to nu_4 "
      "composition bridge"
    ),
    description=(
      "If the Lemma 5.5 bracket "
      "contains plus or minus "
      "E^2 beta composed with "
      "E^t alpha-star, and the "
      "Lemma 5.4 Whitehead correction "
      "gives E^t nu_4 equal up to sign "
      "to E^t alpha-star, then the "
      "same bracket contains plus or "
      "minus E^2 beta composed with "
      "E^t nu_4. "
      "This is a Lemma 5.5-specific "
      "sign/composition bridge and "
      "does not introduce generic "
      "up-to-sign propagation."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma55BracketContainsUpToSignStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma55SuspensionUpToSignStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


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
class Toda53NuPrimeBracketSpecializationStatement:
  nu_prime: HomotopyElement
  alpha: HomotopyElement
  lemma52_index: int
  bracket_membership: TodaBracketMembershipStatement


def toda_53_nu_prime_bracket_specialization_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    nu_prime = HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    )

    if (
      membership.element
      != nu_prime
    ):
      return False

    bracket = membership.bracket

    if (
      bracket.index
      != 1
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      bracket.first
      != eta_3
    ):
      return False

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    expected_second = Multiple(
      coefficient=2,
      expression=iota_4,
    )

    if (
      bracket.second
      != expected_second
    ):
      return False

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    return (
      bracket.third
      == eta_4
    )

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    return (
      Toda53NuPrimeBracketSpecializationStatement(
        nu_prime=membership.element,
        alpha=eta_3,
        lemma52_index=4,
        bracket_membership=membership,
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.3 nu-prime "
      "Lemma 5.2 bracket specialization"
    ),
    description=(
      "Recognize the concrete Toda "
      "(5.3) membership "
      "nu-prime in "
      "{eta_3, 2 iota_4, eta_4}_1 "
      "as the alpha=eta_3 and i=4 "
      "instance to which the already "
      "proved Lemma 5.2 consequence "
      "will be specialized. "
      "This rule does not reimplement "
      "the proof of Lemma 5.2."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaBracketMembershipStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_eta3_twice_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    group_relation = (
      premises[
        0
      ].conclusion
    )

    expected_group = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )

    if (
      group_relation.lhs
      != expected_group
    ):
      return False

    if not isinstance(
      group_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      group_relation.rhs.order
      != 2
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    return (
      group_relation.rhs.generator
      == eta_3
    )

  def build_conclusion(
    premises,
  ):
    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    return Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_3,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda 5.3 eta_3 "
      "twice zero"
    ),
    description=(
      "From the independently derived "
      "relation pi_4^3=Z/2{eta_3}, "
      "derive the concrete order-two "
      "consequence 2 eta_3=0 required "
      "for the alpha=eta_3 "
      "specialization of Lemma 5.2."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_nu_prime_lemma52_hopf_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    two_eta3_zero = (
      premises[
        1
      ].conclusion
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      specialization.alpha
      != eta_3
    ):
      return False

    if (
      specialization.lemma52_index
      != 4
    ):
      return False

    expected_zero = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_3,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      two_eta3_zero
      == expected_zero
    )

  def build_conclusion(
    premises,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=(
          specialization.nu_prime
        ),
      ),
      rhs=IteratedSuspension(
        expression=(
          specialization.alpha
        ),
        exponent=2,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 5.3 nu-prime "
      "Lemma 5.2 Hopf specialization"
    ),
    description=(
      "Specialize the already proved "
      "Lemma 5.2 Hopf conclusion "
      "H(beta)=E^2 alpha to "
      "alpha=eta_3, i=4, and "
      "beta=nu-prime, using the "
      "independently derived "
      "order-two relation 2 eta_3=0."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda53NuPrimeBracketSpecializationStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_nu_prime_lemma52_double_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    two_eta3_zero = (
      premises[
        1
      ].conclusion
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      specialization.alpha
      != eta_3
    ):
      return False

    if (
      specialization.lemma52_index
      != 4
    ):
      return False

    expected_zero = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_3,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      two_eta3_zero
      == expected_zero
    )

  def build_conclusion(
    premises,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    eta_3 = (
      specialization.alpha
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    return Relation(
      lhs=Multiple(
        coefficient=2,
        expression=(
          specialization.nu_prime
        ),
      ),
      rhs=Composition(
        left=eta_3,
        right=Composition(
          left=Suspension(
            expression=eta_3,
          ),
          right=eta_5,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 5.3 nu-prime "
      "Lemma 5.2 double specialization"
    ),
    description=(
      "Specialize the already proved "
      "Lemma 5.2 relation "
      "2 beta=eta_3 composed with "
      "E alpha composed with "
      "eta_(i+1) to alpha=eta_3, "
      "i=4, and beta=nu-prime. "
      "The resulting canonical "
      "Phase 58-3 form is "
      "2 nu-prime=eta_3 composed with "
      "E eta_3 composed with eta_5."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda53NuPrimeBracketSpecializationStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_nu_prime_lemma52_membership_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    two_eta3_zero = (
      premises[
        1
      ].conclusion
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      specialization.alpha
      != eta_3
    ):
      return False

    if (
      specialization.lemma52_index
      != 4
    ):
      return False

    expected_zero = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_3,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      two_eta3_zero
      == expected_zero
    )

  def build_conclusion(
    premises,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    return (
      HomotopyGroupMembershipStatement(
        element=(
          specialization.nu_prime
        ),
        group_dimension=6,
        sphere_dimension=3,
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.3 nu-prime "
      "Lemma 5.2 membership specialization"
    ),
    description=(
      "Specialize the already proved "
      "Lemma 5.2 typing conclusion "
      "beta in pi_(i+2)^3 to "
      "i=4 and beta=nu-prime, "
      "giving nu-prime in pi_6^3."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda53NuPrimeBracketSpecializationStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_eta5_iterated_suspension_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    eta3_definition = (
      premises[
        0
      ].conclusion
    )

    eta5_definition = (
      premises[
        1
      ].conclusion
    )

    if (
      eta3_definition.index
      != 3
    ):
      return False

    if (
      eta5_definition.index
      != 5
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      eta3_definition.element
      != eta_3
    ):
      return False

    expected_eta3_definition = (
      IteratedSuspension(
        expression=eta_2,
        exponent=1,
      )
    )

    if (
      eta3_definition.iterated_suspension
      != expected_eta3_definition
    ):
      return False

    eta5_element = (
      eta5_definition.element
    )

    if (
      eta5_element.dimension
      != 5
    ):
      return False

    if (
      eta5_element.source
      != 6
    ):
      return False

    if (
      eta5_element.target
      != 5
    ):
      return False

    if (
      eta5_element.generator
      != GeneratorSymbol(
        family="η",
        index=5,
      )
    ):
      return False

    expected_eta5_definition = (
      IteratedSuspension(
        expression=eta_2,
        exponent=3,
      )
    )

    return (
      eta5_definition.iterated_suspension
      == expected_eta5_definition
    )

  def build_conclusion(
    premises,
  ):
    eta3_definition = (
      premises[
        0
      ].conclusion
    )

    eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    return Relation(
      lhs=IteratedSuspension(
        expression=(
          eta3_definition.element
        ),
        exponent=2,
      ),
      rhs=eta_5,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 5.3 eta_5 "
      "iterated suspension bridge"
    ),
    description=(
      "For the concrete eta-family "
      "definitions at indices 3 and 5, "
      "derive the Phase 58 consequence "
      "E^2 eta_3=eta_5. "
      "The existing eta-family "
      "constructor uses the structural "
      "name eta_5 at index 5, while "
      "Toda 5.3 uses the canonical "
      "concrete notation eta-subscript-5. "
      "This narrow bridge connects those "
      "representations without changing "
      "the Phase 54 constructor or adding "
      "generic suspension normalization."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_53_eta4_suspension_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    eta3_definition = (
      premises[
        0
      ].conclusion
    )

    eta4_definition = (
      premises[
        1
      ].conclusion
    )

    if (
      eta3_definition.index
      != 3
    ):
      return False

    if (
      eta4_definition.index
      != 4
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      eta3_definition.element
      != eta_3
    ):
      return False

    if (
      eta3_definition.iterated_suspension
      != IteratedSuspension(
        expression=eta_2,
        exponent=1,
      )
    ):
      return False

    eta4_element = (
      eta4_definition.element
    )

    if (
      eta4_element.dimension
      != 4
    ):
      return False

    if (
      eta4_element.source
      != 5
    ):
      return False

    if (
      eta4_element.target
      != 4
    ):
      return False

    if (
      eta4_element.generator
      != GeneratorSymbol(
        family="η",
        index=4,
      )
    ):
      return False

    return (
      eta4_definition.iterated_suspension
      == IteratedSuspension(
        expression=eta_2,
        exponent=2,
      )
    )

  def build_conclusion(
    premises,
  ):
    eta3_definition = (
      premises[
        0
      ].conclusion
    )

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    return Relation(
      lhs=Suspension(
        expression=(
          eta3_definition.element
        ),
      ),
      rhs=eta_4,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 5.3 eta_4 "
      "suspension bridge"
    ),
    description=(
      "For the concrete eta-family "
      "definitions at indices 3 and 4, "
      "derive E eta_3=eta_4. "
      "The existing eta-family constructor "
      "uses the structural name eta_4 at "
      "index 4, while Toda 5.3 uses the "
      "canonical concrete notation "
      "eta-subscript-4. "
      "This narrow bridge does not change "
      "the Phase 54 symbolic eta-family "
      "rule or introduce generic "
      "suspension normalization."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
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
class TodaLemma52BracketCompositionMembershipStatement:
  element: Expression
  outer_left: Expression
  bracket: TodaBracket
  bracket_sign: int
  bracket_suspension_exponent: int


@dataclass(frozen=True)
class TodaLemma52BracketRepresentativeStatement:
  membership: TodaLemma52BracketCompositionMembershipStatement
  representative: Expression


def toda_prop14_lemma52_bracket_transformation_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    bracket = membership.bracket

    if (
      bracket.index
      != 1
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      bracket.first
      != eta_3
    ):
      return False

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    if (
      bracket.second
      != Multiple(
        coefficient=2,
        expression=iota_4,
      )
    ):
      return False

    if not isinstance(
      bracket.third,
      Suspension,
    ):
      return False

    alpha = (
      bracket
      .third
      .expression
    )

    if not isinstance(
      alpha,
      HomotopyElement,
    ):
      return False

    i = alpha.dimension

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    source_bracket = (
      membership.bracket
    )

    alpha = (
      source_bracket
      .third
      .expression
    )

    i = alpha.dimension

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    iota_i = HomotopyElement(
      name="ι_i",
      dimension=i,
      generator=GeneratorSymbol(
        family="ι",
        index=i,
      ),
    )

    inner_bracket = TodaBracket(
      first=Multiple(
        coefficient=2,
        expression=iota_3,
      ),
      second=alpha,
      third=Multiple(
        coefficient=2,
        expression=iota_i,
      ),
    )

    return (
      TodaLemma52BracketCompositionMembershipStatement(
        element=Multiple(
          coefficient=2,
          expression=membership.element,
        ),
        outer_left=source_bracket.first,
        bracket=inner_bracket,
        bracket_sign=1,
        bracket_suspension_exponent=1,
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 1.4 "
      "Lemma 5.2 bracket transformation"
    ),
    description=(
      "For beta in "
      "{eta_3, 2 iota_4, E alpha}_1, "
      "the n=1 specialization of "
      "Toda Proposition 1.4 gives "
      "2 beta in eta_3 composed with "
      "E{2 iota_3, alpha, 2 iota_i}."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaBracketMembershipStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop13_lemma52_bracket_transformation_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    if (
      statement.bracket_sign
      != 1
    ):
      return False

    if (
      statement.bracket_suspension_exponent
      != 1
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      statement.outer_left
      != eta_3
    ):
      return False

    bracket = statement.bracket

    if (
      bracket.index
      is not None
    ):
      return False

    if not isinstance(
      bracket.first,
      Multiple,
    ):
      return False

    if (
      bracket.first.coefficient
      != 2
    ):
      return False

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    if (
      bracket.first.expression
      != iota_3
    ):
      return False

    alpha = bracket.second

    if not isinstance(
      alpha,
      HomotopyElement,
    ):
      return False

    i = alpha.dimension

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    iota_i = HomotopyElement(
      name="ι_i",
      dimension=i,
      generator=GeneratorSymbol(
        family="ι",
        index=i,
      ),
    )

    if (
      bracket.third
      != Multiple(
        coefficient=2,
        expression=iota_i,
      )
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    source_bracket = statement.bracket

    alpha = source_bracket.second
    i = alpha.dimension

    i_plus_one = ScalarSum(
      left=i,
      right=1,
    )

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    iota_i_plus_one = HomotopyElement(
      name="ι_(i+1)",
      dimension=i_plus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=i_plus_one,
      ),
    )

    target_bracket = TodaBracket(
      first=Multiple(
        coefficient=2,
        expression=iota_4,
      ),
      second=Suspension(
        expression=alpha,
      ),
      third=Multiple(
        coefficient=2,
        expression=iota_i_plus_one,
      ),
      index=1,
    )

    return (
      TodaLemma52BracketCompositionMembershipStatement(
        element=statement.element,
        outer_left=statement.outer_left,
        bracket=target_bracket,
        bracket_sign=-1,
        bracket_suspension_exponent=0,
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 1.3 "
      "Lemma 5.2 bracket transformation"
    ),
    description=(
      "The n=0 specialization of "
      "Toda Proposition 1.3 transforms "
      "E{2 iota_3, alpha, 2 iota_i} "
      "into the negative indexed bracket "
      "{2 iota_4, E alpha, "
      "2 iota_(i+1)}_1 required in "
      "Toda Lemma 5.2."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma52BracketCompositionMembershipStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_cor37_lemma52_representative_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    if (
      statement.bracket_sign
      != -1
    ):
      return False

    if (
      statement.bracket_suspension_exponent
      != 0
    ):
      return False

    bracket = statement.bracket

    if (
      bracket.index
      != 1
    ):
      return False

    if not isinstance(
      bracket.first,
      Multiple,
    ):
      return False

    if (
      bracket.first.coefficient
      != 2
    ):
      return False

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    if (
      bracket.first.expression
      != iota_4
    ):
      return False

    if not isinstance(
      bracket.second,
      Suspension,
    ):
      return False

    alpha = (
      bracket
      .second
      .expression
    )

    if not isinstance(
      alpha,
      HomotopyElement,
    ):
      return False

    i = alpha.dimension

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    i_plus_one = ScalarSum(
      left=i,
      right=1,
    )

    iota_i_plus_one = HomotopyElement(
      name="ι_(i+1)",
      dimension=i_plus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=i_plus_one,
      ),
    )

    expected_third = Multiple(
      coefficient=2,
      expression=iota_i_plus_one,
    )

    return (
      bracket.third
      == expected_third
    )

  def build_conclusion(
    premises,
  ):
    statement = (
      premises[
        0
      ].conclusion
    )

    bracket = statement.bracket

    alpha = (
      bracket
      .second
      .expression
    )

    i = alpha.dimension

    i_plus_one = ScalarSum(
      left=i,
      right=1,
    )

    i_plus_two = ScalarSum(
      left=i,
      right=2,
    )

    eta_i_plus_one = HomotopyElement(
      name="η_(i+1)",
      dimension=i_plus_one,
      source=i_plus_two,
      target=i_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=i_plus_one,
      ),
    )

    cor37_element = Composition(
      left=Suspension(
        expression=alpha,
      ),
      right=eta_i_plus_one,
    )

    signed_element = Multiple(
      coefficient=-1,
      expression=cor37_element,
    )

    representative = Composition(
      left=statement.outer_left,
      right=signed_element,
    )

    return (
      TodaLemma52BracketRepresentativeStatement(
        membership=statement,
        representative=representative,
      )
    )

  return InferenceRule(
    name=(
      "Toda Corollary 3.7 "
      "Lemma 5.2 bracket representative"
    ),
    description=(
      "For r=2, Corollary 3.7 gives "
      "E alpha composed with eta_(i+1) "
      "as an element of "
      "{2 iota_4, E alpha, "
      "2 iota_(i+1)}_1. "
      "For the negative bracket used "
      "after Proposition 1.3, the "
      "corresponding representative is "
      "eta_3 composed with minus "
      "(E alpha composed with "
      "eta_(i+1))."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma52BracketCompositionMembershipStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop51_eta4_twice_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop51_statement = (
      premises[
        0
      ].conclusion
    )

    higher_eta_relation = (
      prop51_statement
      .higher_eta_group_relation
    )

    if not isinstance(
      higher_eta_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      higher_eta_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    target_group = (
      higher_eta_relation.lhs
    )

    n = (
      target_group
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      sphere_dimension=n,
    )

    if (
      target_group
      != expected_group
    ):
      return False

    cyclic_group = (
      higher_eta_relation.rhs
    )

    if (
      cyclic_group.order
      != 2
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      cyclic_group.generator
      == eta_n
    )

  def build_conclusion(
    premises,
  ):
    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    return Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_4,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.1 "
      "eta_4 order-two consequence"
    ),
    description=(
      "From the independently derived "
      "finite-dimensional Proposition 5.1 "
      "higher eta-family result, specialize "
      "only the consequence needed in "
      "Lemma 5.2: 2 eta_4 is zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
        proof_rule=ProofRule.INFERENCE,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_21_lemma52_suspended_indeterminacy_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    eta4_zero = (
      premises[
        1
      ].conclusion
    )

    if (
      membership.sphere_dimension
      != 4
    ):
      return False

    group_dimension = (
      membership.group_dimension
    )

    if not isinstance(
      group_dimension,
      ScalarSum,
    ):
      return False

    if (
      group_dimension.right
      != 2
    ):
      return False

    i = (
      group_dimension.left
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    gamma = (
      membership.element
    )

    if (
      gamma.dimension
      != group_dimension
    ):
      return False

    eta_4 = HomotopyElement(
      name="η₄",
      dimension=4,
      source=5,
      target=4,
      generator=GeneratorSymbol(
        family="η",
        index=4,
      ),
    )

    expected_eta4_zero = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta_4,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      eta4_zero
      == expected_eta4_zero
    )

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    gamma = (
      membership.element
    )

    i_plus_two = (
      membership.group_dimension
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    iota_i_plus_two = HomotopyElement(
      name="ι_(i+2)",
      dimension=i_plus_two,
      generator=GeneratorSymbol(
        family="ι",
        index=i_plus_two,
      ),
    )

    indeterminacy_element = Composition(
      left=Composition(
        left=eta_3,
        right=gamma,
      ),
      right=Multiple(
        coefficient=2,
        expression=iota_i_plus_two,
      ),
    )

    return Relation(
      lhs=Suspension(
        expression=indeterminacy_element,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda (2.1) Lemma 5.2 "
      "suspended indeterminacy zero"
    ),
    description=(
      "For gamma in pi_(i+2)(S^4), "
      "Toda (2.1) gives "
      "E(eta_3 gamma 2 iota_(i+2)) "
      "= eta_4 2Egamma "
      "= 2 eta_4 Egamma. "
      "Using 2 eta_4 = 0, the suspended "
      "indeterminacy element is zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
        proof_rule=ProofRule.INFERENCE,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma45_n4_suspension_zero_reflection_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    suspended_zero = (
      premises[
        1
      ].conclusion
    )

    if (
      membership.sphere_dimension
      != 4
    ):
      return False

    group_dimension = (
      membership.group_dimension
    )

    if not isinstance(
      group_dimension,
      ScalarSum,
    ):
      return False

    if (
      group_dimension.right
      != 2
    ):
      return False

    i = (
      group_dimension.left
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    gamma = (
      membership.element
    )

    if (
      gamma.dimension
      != group_dimension
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    iota_i_plus_two = HomotopyElement(
      name="ι_(i+2)",
      dimension=group_dimension,
      generator=GeneratorSymbol(
        family="ι",
        index=group_dimension,
      ),
    )

    indeterminacy_element = Composition(
      left=Composition(
        left=eta_3,
        right=gamma,
      ),
      right=Multiple(
        coefficient=2,
        expression=iota_i_plus_two,
      ),
    )

    expected_suspended_zero = Relation(
      lhs=Suspension(
        expression=indeterminacy_element,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      suspended_zero
      == expected_suspended_zero
    )

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    gamma = (
      membership.element
    )

    i_plus_two = (
      membership.group_dimension
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    iota_i_plus_two = HomotopyElement(
      name="ι_(i+2)",
      dimension=i_plus_two,
      generator=GeneratorSymbol(
        family="ι",
        index=i_plus_two,
      ),
    )

    indeterminacy_element = Composition(
      left=Composition(
        left=eta_3,
        right=gamma,
      ),
      right=Multiple(
        coefficient=2,
        expression=iota_i_plus_two,
      ),
    )

    return Relation(
      lhs=indeterminacy_element,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 4.5 n=4 "
      "indeterminacy zero reflection"
    ),
    description=(
      "Toda Lemma 4.5 says that "
      "suspension is injective for n=4. "
      "For the specific Lemma 5.2 "
      "indeterminacy element, if its "
      "suspension is zero, then the "
      "original element is zero."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
        proof_rule=ProofRule.INFERENCE,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma52_prop26_first_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop51_statement = (
      premises[
        0
      ].conclusion
    )

    higher_eta_relation = (
      prop51_statement
      .higher_eta_group_relation
    )

    if not isinstance(
      higher_eta_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      higher_eta_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    n = (
      higher_eta_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_group = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=1,
      ),
      sphere_dimension=n,
    )

    if (
      higher_eta_relation.lhs
      != expected_group
    ):
      return False

    if (
      higher_eta_relation.rhs.order
      != 2
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      higher_eta_relation
      .rhs
      .generator
      == eta_n
    )

  def build_conclusion(
    premises,
  ):
    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    return Relation(
      lhs=Suspension(
        expression=Composition(
          left=eta_2,
          right=Multiple(
            coefficient=2,
            expression=iota_3,
          ),
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.2 "
      "Proposition 2.6 first zero premise"
    ),
    description=(
      "From the independently derived "
      "order-two higher eta family, "
      "specialize to 2 eta_3 = 0. "
      "Using the Lemma 5.2 instance of "
      "Toda (2.1), this gives "
      "E(eta_2 composed with 2 iota_3)=0."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
        proof_rule=ProofRule.INFERENCE,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma52_hopf_value_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop26_statement = (
      premises[
        0
      ].conclusion
    )

    preimage_statement = (
      premises[
        1
      ].conclusion
    )

    two_alpha_zero = (
      premises[
        2
      ].conclusion
    )

    if (
      prop26_statement.sign
      != -1
    ):
      return False

    if not isinstance(
      prop26_statement.right_factor,
      IteratedSuspension,
    ):
      return False

    if (
      prop26_statement
      .right_factor
      .exponent
      != 2
    ):
      return False

    alpha = (
      prop26_statement
      .right_factor
      .expression
    )

    expected_two_alpha_zero = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=alpha,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      two_alpha_zero
      != expected_two_alpha_zero
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    expected_prop26_value = Composition(
      left=eta_2,
      right=Multiple(
        coefficient=2,
        expression=iota_3,
      ),
    )

    if (
      prop26_statement.delta_preimage_value
      != expected_prop26_value
    ):
      return False

    expected_preimage_value = Multiple(
      coefficient=2,
      expression=eta_2,
    )

    if (
      preimage_statement.value
      != expected_preimage_value
    ):
      return False

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    return (
      preimage_statement
      .positive_preimage
      == iota_5
    )

  def build_conclusion(
    premises,
  ):
    prop26_statement = (
      premises[
        0
      ].conclusion
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=(
          prop26_statement
          .bracket_element
        ),
      ),
      rhs=(
        prop26_statement
        .right_factor
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.2 "
      "Hopf invariant value"
    ),
    description=(
      "Combine the Proposition 2.6 "
      "specialization with "
      "Delta^-1(2 eta_2)=plus or minus "
      "iota_5. Toda (2.1) identifies "
      "eta_2 composed with 2 iota_3 "
      "with 2 eta_2. Since 2 alpha=0, "
      "the sign ambiguity disappears "
      "after two suspensions, giving "
      "H(beta)=E^2 alpha."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaProp26HopfBracketConsequenceStatement
        ),
        proof_rule=ProofRule.INFERENCE,
      ),
      PremisePattern(
        statement_type=(
          TodaDeltaPreimageUpToSignStatement
        ),
        proof_rule=ProofRule.INFERENCE,
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma52_beta_membership_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    bracket = membership.bracket

    if (
      bracket.index
      != 1
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      bracket.first
      != eta_3
    ):
      return False

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    if (
      bracket.second
      != Multiple(
        coefficient=2,
        expression=iota_4,
      )
    ):
      return False

    if not isinstance(
      bracket.third,
      Suspension,
    ):
      return False

    alpha = (
      bracket
      .third
      .expression
    )

    if not isinstance(
      alpha,
      HomotopyElement,
    ):
      return False

    i = alpha.dimension

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    expected_dimension = ScalarSum(
      left=i,
      right=2,
    )

    return (
      membership.element.dimension
      == expected_dimension
    )

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    alpha = (
      membership
      .bracket
      .third
      .expression
    )

    return (
      HomotopyGroupMembershipStatement(
        element=membership.element,
        group_dimension=ScalarSum(
          left=alpha.dimension,
          right=2,
        ),
        sphere_dimension=3,
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.2 "
      "beta homotopy-group membership"
    ),
    description=(
      "An element beta of the indexed "
      "bracket {eta_3, 2 iota_4, "
      "E alpha}_1 belongs to "
      "pi_(i+2)(S^3)."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaBracketMembershipStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma52_double_value_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    representative_statement = (
      premises[
        0
      ].conclusion
    )

    gamma_membership = (
      premises[
        1
      ].conclusion
    )

    indeterminacy_zero = (
      premises[
        2
      ].conclusion
    )

    prop51_statement = (
      premises[
        3
      ].conclusion
    )

    membership = (
      representative_statement
      .membership
    )

    if (
      membership.bracket_sign
      != -1
    ):
      return False

    if (
      membership.bracket_suspension_exponent
      != 0
    ):
      return False

    if not isinstance(
      membership.element,
      Multiple,
    ):
      return False

    if (
      membership.element.coefficient
      != 2
    ):
      return False

    beta = (
      membership
      .element
      .expression
    )

    bracket = membership.bracket

    if (
      bracket.index
      != 1
    ):
      return False

    if not isinstance(
      bracket.second,
      Suspension,
    ):
      return False

    alpha = (
      bracket
      .second
      .expression
    )

    if not isinstance(
      alpha,
      HomotopyElement,
    ):
      return False

    i = alpha.dimension

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    i_plus_one = ScalarSum(
      left=i,
      right=1,
    )

    i_plus_two = ScalarSum(
      left=i,
      right=2,
    )

    if (
      beta.dimension
      != i_plus_two
    ):
      return False

    if (
      gamma_membership.group_dimension
      != i_plus_two
    ):
      return False

    if (
      gamma_membership.sphere_dimension
      != 4
    ):
      return False

    gamma = (
      gamma_membership.element
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    iota_i_plus_two = HomotopyElement(
      name="ι_(i+2)",
      dimension=i_plus_two,
      generator=GeneratorSymbol(
        family="ι",
        index=i_plus_two,
      ),
    )

    expected_indeterminacy_zero = Relation(
      lhs=Composition(
        left=Composition(
          left=eta_3,
          right=gamma,
        ),
        right=Multiple(
          coefficient=2,
          expression=iota_i_plus_two,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      indeterminacy_zero
      != expected_indeterminacy_zero
    ):
      return False

    eta_i_plus_one = HomotopyElement(
      name="η_(i+1)",
      dimension=i_plus_one,
      source=i_plus_two,
      target=i_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=i_plus_one,
      ),
    )

    expected_signed_representative = (
      Composition(
        left=eta_3,
        right=Multiple(
          coefficient=-1,
          expression=Composition(
            left=Suspension(
              expression=alpha,
            ),
            right=eta_i_plus_one,
          ),
        ),
      )
    )

    if (
      representative_statement
      .representative
      != expected_signed_representative
    ):
      return False

    higher_eta_relation = (
      prop51_statement
      .higher_eta_group_relation
    )

    if not isinstance(
      higher_eta_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    if not isinstance(
      higher_eta_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    n = (
      higher_eta_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      higher_eta_relation.rhs.order
      != 2
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    return (
      higher_eta_relation
      .rhs
      .generator
      == eta_n
    )

  def build_conclusion(
    premises,
  ):
    representative_statement = (
      premises[
        0
      ].conclusion
    )

    membership = (
      representative_statement
      .membership
    )

    alpha = (
      membership
      .bracket
      .second
      .expression
    )

    i = alpha.dimension

    i_plus_one = ScalarSum(
      left=i,
      right=1,
    )

    i_plus_two = ScalarSum(
      left=i,
      right=2,
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    eta_i_plus_one = HomotopyElement(
      name="η_(i+1)",
      dimension=i_plus_one,
      source=i_plus_two,
      target=i_plus_one,
      generator=GeneratorSymbol(
        family="η",
        index=i_plus_one,
      ),
    )

    return Relation(
      lhs=membership.element,
      rhs=Composition(
        left=eta_3,
        right=Composition(
          left=Suspension(
            expression=alpha,
          ),
          right=eta_i_plus_one,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.2 "
      "twice beta value"
    ),
    description=(
      "The Proposition 1.4 / "
      "Proposition 1.3 / Corollary 3.7 "
      "chain gives a representative of "
      "the target coset. Phase 57-6 "
      "shows its indeterminacy is zero. "
      "The order-two eta_3 specialization "
      "removes the remaining sign, giving "
      "2 beta = eta_3 composed with "
      "E alpha composed with eta_(i+1)."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaLemma52BracketRepresentativeStatement
        ),
        proof_rule=ProofRule.INFERENCE,
      ),
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.ZERO,
        proof_rule=ProofRule.INFERENCE,
      ),
      PremisePattern(
        statement_type=(
          TodaProp51FiniteDimensionalStatement
        ),
        proof_rule=ProofRule.INFERENCE,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma52_delta_e2_alpha_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_relation = (
      premises[
        0
      ].conclusion
    )

    if not isinstance(
      hopf_relation.lhs,
      MapApplication,
    ):
      return False

    if (
      hopf_relation.lhs.map
      != EHP_H_MAP
    ):
      return False

    if not isinstance(
      hopf_relation.rhs,
      IteratedSuspension,
    ):
      return False

    return (
      hopf_relation
      .rhs
      .exponent
      == 2
    )

  def build_conclusion(
    premises,
  ):
    hopf_relation = (
      premises[
        0
      ].conclusion
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=(
          hopf_relation.rhs
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.2 "
      "Delta E^2 alpha zero"
    ),
    description=(
      "From H(beta)=E^2 alpha and "
      "the H-Delta exactness relation "
      "Delta H=0 used in Lemma 5.2, "
      "derive Delta(E^2 alpha)=0."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
        proof_rule=ProofRule.INFERENCE,
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


@dataclass(frozen=True)
class TodaBracketDefinedStatement:
  bracket: TodaBracket


@dataclass(frozen=True)
class TodaProp26HopfBracketConsequenceStatement:
  bracket_element: Expression
  bracket: TodaBracket
  delta_preimage_value: Expression
  right_factor: Expression
  sign: int


def toda_prop26_lemma52_hopf_bracket_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    first_zero = (
      premises[
        1
      ].conclusion
    )

    second_zero = (
      premises[
        2
      ].conclusion
    )

    bracket = membership.bracket

    if (
      bracket.index
      != 1
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    iota_4 = HomotopyElement(
      name="ι_4",
      dimension=4,
      generator=GeneratorSymbol(
        family="ι",
        index=4,
      ),
    )

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    if (
      bracket.first
      != eta_3
    ):
      return False

    if (
      bracket.second
      != Multiple(
        coefficient=2,
        expression=iota_4,
      )
    ):
      return False

    if not isinstance(
      bracket.third,
      Suspension,
    ):
      return False

    alpha = (
      bracket.third.expression
    )

    expected_first_zero = Relation(
      lhs=Suspension(
        expression=Composition(
          left=eta_2,
          right=Multiple(
            coefficient=2,
            expression=iota_3,
          ),
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      first_zero
      != expected_first_zero
    ):
      return False

    expected_second_zero = Relation(
      lhs=Composition(
        left=Multiple(
          coefficient=2,
          expression=iota_3,
        ),
        right=alpha,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      second_zero
      != expected_second_zero
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[
        0
      ].conclusion
    )

    bracket = membership.bracket

    alpha = (
      bracket
      .third
      .expression
    )

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    return (
      TodaProp26HopfBracketConsequenceStatement(
        bracket_element=(
          membership.element
        ),
        bracket=bracket,
        delta_preimage_value=Composition(
          left=eta_2,
          right=Multiple(
            coefficient=2,
            expression=iota_3,
          ),
        ),
        right_factor=IteratedSuspension(
          expression=alpha,
          exponent=2,
        ),
        sign=-1,
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 2.6 "
      "Lemma 5.2 Hopf bracket consequence"
    ),
    description=(
      "For beta in "
      "{eta_3, 2 iota_4, E alpha}_1, "
      "with E(eta_2 composed with "
      "2 iota_3)=0 and "
      "2 iota_3 composed with alpha=0, "
      "the Lemma 5.2 specialization "
      "of Toda Proposition 2.6 gives "
      "H(beta) in minus "
      "Delta^-1(eta_2 composed with "
      "2 iota_3) composed with "
      "E^2 alpha."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaBracketMembershipStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


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


def toda_delta_iota5_whitehead_square_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_map = (
      premises[
        0
      ].conclusion
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    return (
      delta_map.source_group
      == expected_source
      and delta_map.target_group
      == expected_target
    )

  def build_conclusion(
    premises,
  ):
    delta_map = (
      premises[
        0
      ].conclusion
    )

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    iota_2 = HomotopyElement(
      name="ι_2",
      dimension=2,
      generator=GeneratorSymbol(
        family="ι",
        index=2,
      ),
    )

    whitehead_square = WhiteheadProduct(
      left=iota_2,
      right=iota_2,
    )

    return TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=whitehead_square,
    )

  return InferenceRule(
    name=(
      "Toda Delta iota_5 "
      "Whitehead-square relation"
    ),
    description=(
      "For the specific Delta map "
      "from pi_5^5 to pi_3^2, "
      "Delta(iota_5) equals the "
      "Whitehead square "
      "[iota_2,iota_2] up to sign."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaDeltaMap
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_delta_iota5_two_eta2_up_to_sign_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_statement = (
      premises[
        0
      ].conclusion
    )

    whitehead_statement = (
      premises[
        1
      ].conclusion
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    if (
      delta_statement.map.source_group
      != expected_source
    ):
      return False

    if (
      delta_statement.map.target_group
      != expected_target
    ):
      return False

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    if (
      delta_statement.element
      != iota_5
    ):
      return False

    iota_2 = HomotopyElement(
      name="ι_2",
      dimension=2,
      generator=GeneratorSymbol(
        family="ι",
        index=2,
      ),
    )

    expected_whitehead_square = (
      WhiteheadProduct(
        left=iota_2,
        right=iota_2,
      )
    )

    if (
      delta_statement.positive_value
      != expected_whitehead_square
    ):
      return False

    if (
      whitehead_statement.whitehead_square
      != expected_whitehead_square
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    expected_two_eta_2 = Multiple(
      coefficient=2,
      expression=eta_2,
    )

    return (
      whitehead_statement.positive_value
      == expected_two_eta_2
    )

  def build_conclusion(
    premises,
  ):
    delta_statement = (
      premises[
        0
      ].conclusion
    )

    whitehead_statement = (
      premises[
        1
      ].conclusion
    )

    return TodaDeltaImageUpToSignStatement(
      map=delta_statement.map,
      element=delta_statement.element,
      positive_value=(
        whitehead_statement
        .positive_value
      ),
    )

  return InferenceRule(
    name=(
      "Toda Delta iota_5 "
      "twice eta_2 up-to-sign bridge"
    ),
    description=(
      "For the specific Delta map "
      "from pi_5^5 to pi_3^2, "
      "if Delta(iota_5) equals "
      "[iota_2,iota_2] up to sign "
      "and [iota_2,iota_2] equals "
      "2 eta_2 up to sign, then "
      "Delta(iota_5) equals "
      "2 eta_2 up to sign."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaDeltaImageUpToSignStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaPi32WhiteheadSquareUpToSignStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi3_2_whitehead_square_up_to_sign_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop27_statement = (
      premises[
        0
      ].conclusion
    )

    eta_2_definition = (
      premises[
        1
      ].conclusion
    )

    hopf_relation = (
      premises[
        2
      ].conclusion
    )

    hopf_injectivity = (
      premises[
        3
      ].conclusion
    )

    expected_pi_3_2 = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    expected_pi_3_3 = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )

    if (
      eta_2_definition.map.source_group
      != expected_pi_3_2
    ):
      return False

    if (
      eta_2_definition.map.target_group
      != expected_pi_3_3
    ):
      return False

    if (
      hopf_injectivity.map
      != eta_2_definition.map
    ):
      return False

    eta_2 = eta_2_definition.element

    iota_3 = eta_2_definition.image

    expected_hopf_relation = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=eta_2,
      ),
      rhs=iota_3,
      relation_type=RelationType.EQUALITY,
    )

    if (
      hopf_relation
      != expected_hopf_relation
    ):
      return False

    iota_2 = HomotopyElement(
      name="ι_2",
      dimension=2,
      generator=GeneratorSymbol(
        family="ι",
        index=2,
      ),
    )

    expected_whitehead_square = (
      WhiteheadProduct(
        left=iota_2,
        right=iota_2,
      )
    )

    if (
      prop27_statement.argument
      != expected_whitehead_square
    ):
      return False

    expected_positive_hopf_value = (
      Multiple(
        coefficient=2,
        expression=iota_3,
      )
    )

    return (
      prop27_statement.positive_value
      == expected_positive_hopf_value
    )

  def build_conclusion(
    premises,
  ):
    prop27_statement = (
      premises[
        0
      ].conclusion
    )

    eta_2_definition = (
      premises[
        1
      ].conclusion
    )

    return (
      TodaPi32WhiteheadSquareUpToSignStatement(
        whitehead_square=(
          prop27_statement.argument
        ),
        positive_value=Multiple(
          coefficient=2,
          expression=(
            eta_2_definition.element
          ),
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda pi_3^2 Whitehead square "
      "equals twice eta_2 up to sign"
    ),
    description=(
      "For the specific Hopf invariant "
      "map from pi_3^2 to pi_3^3, "
      "Toda Proposition 2.7 gives "
      "H([iota_2,iota_2]) equal to "
      "plus or minus 2 iota_3. "
      "Since eta_2 maps to iota_3 "
      "and the same Hopf map is "
      "injective, the Whitehead square "
      "[iota_2,iota_2] equals plus or "
      "minus 2 eta_2."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaProp27HopfInvariantUpToSignStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaPi32Eta2DefinitionStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaHopfInvariantInjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi4_3_delta_image_free_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_group_relation = (
      premises[
        0
      ].conclusion
    )

    delta_image = (
      premises[
        1
      ].conclusion
    )

    whitehead_square = (
      premises[
        2
      ].conclusion
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    if (
      source_group_relation.lhs
      != expected_source
    ):
      return False

    if not isinstance(
      source_group_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    iota_5 = HomotopyElement(
      name="ι_5",
      dimension=5,
      generator=GeneratorSymbol(
        family="ι",
        index=5,
      ),
    )

    if (
      source_group_relation.rhs.generator
      != iota_5
    ):
      return False

    if (
      delta_image.map.source_group
      != expected_source
    ):
      return False

    if (
      delta_image.map.target_group
      != expected_target
    ):
      return False

    if (
      delta_image.element
      != iota_5
    ):
      return False

    if (
      delta_image.positive_value
      != whitehead_square.whitehead_square
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    expected_two_eta_2 = Multiple(
      coefficient=2,
      expression=eta_2,
    )

    return (
      whitehead_square.positive_value
      == expected_two_eta_2
    )

  def build_conclusion(
    premises,
  ):
    delta_image = (
      premises[
        1
      ].conclusion
    )

    whitehead_square = (
      premises[
        2
      ].conclusion
    )

    return (
      TodaDeltaImageFreeCyclicStatement(
        map=delta_image.map,
        image_group=FreeCyclicGroup(
          generator=(
            whitehead_square
            .positive_value
          ),
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda pi_4^3 Delta image "
      "generated by twice eta_2"
    ),
    description=(
      "If pi_5^5 is freely generated "
      "by iota_5, Delta(iota_5) equals "
      "the Whitehead square up to sign, "
      "and that Whitehead square equals "
      "twice eta_2 up to sign, then the "
      "image of the specific Delta map "
      "is freely generated by 2 eta_2."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaDeltaImageUpToSignStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaPi32WhiteheadSquareUpToSignStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_image = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

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

    if (
      delta_image.map.source_group
      != window.source_term
    ):
      return False

    if (
      delta_image.map.target_group
      != window.middle_term
    ):
      return False

    expected_source = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )

    return (
      window.source_term
      == expected_source
      and window.middle_term
      == expected_middle
      and window.target_term
      == expected_target
    )

  def build_conclusion(
    premises,
  ):
    delta_image = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    suspension_map = TodaSuspensionMap(
      source_group=window.middle_term,
      target_group=window.target_term,
    )

    return (
      TodaSuspensionKernelFreeCyclicStatement(
        map=suspension_map,
        kernel_group=(
          delta_image.image_group
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda pi_4^3 exactness "
      "Delta image equals E kernel"
    ),
    description=(
      "For the specific Delta-E exact "
      "window pi_5^5 to pi_3^2 to "
      "pi_4^3, exactness identifies "
      "the image of Delta with the "
      "kernel of the corresponding "
      "suspension map."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaDeltaImageFreeCyclicStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    zero_statement = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

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

    if (
      zero_statement.group
      != window.target_term
    ):
      return False

    expected_source = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=5,
    )

    return (
      window.source_term
      == expected_source
      and window.middle_term
      == expected_middle
      and window.target_term
      == expected_target
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        1
      ].conclusion
    )

    window = exactness.window

    return (
      TodaSuspensionSurjectiveStatement(
        map=TodaSuspensionMap(
          source_group=window.source_term,
          target_group=window.middle_term,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda pi_4^3 E-H exactness "
      "zero-right suspension surjectivity"
    ),
    description=(
      "If the specific E-H window "
      "pi_3^2 to pi_4^3 to pi_4^5 "
      "is exact and pi_4^5 is zero, "
      "then the corresponding "
      "suspension map E from pi_3^2 "
      "to pi_4^3 is surjective."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi4_3_finite_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_group_relation = (
      premises[
        0
      ].conclusion
    )

    kernel_statement = (
      premises[
        1
      ].conclusion
    )

    surjectivity = (
      premises[
        2
      ].conclusion
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )

    if (
      source_group_relation.lhs
      != expected_source
    ):
      return False

    if not isinstance(
      source_group_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    if (
      source_group_relation.rhs.generator
      != eta_2
    ):
      return False

    suspension_map = (
      kernel_statement.map
    )

    if (
      surjectivity.map
      != suspension_map
    ):
      return False

    if (
      suspension_map.source_group
      != expected_source
    ):
      return False

    if (
      suspension_map.target_group
      != expected_target
    ):
      return False

    expected_kernel = FreeCyclicGroup(
      generator=Multiple(
        coefficient=2,
        expression=eta_2,
      ),
    )

    return (
      kernel_statement.kernel_group
      == expected_kernel
    )

  def build_conclusion(
    premises,
  ):
    source_group_relation = (
      premises[
        0
      ].conclusion
    )

    kernel_statement = (
      premises[
        1
      ].conclusion
    )

    eta_2 = (
      source_group_relation
      .rhs
      .generator
    )

    target_group = (
      kernel_statement
      .map
      .target_group
    )

    return Relation(
      lhs=target_group,
      rhs=FiniteCyclicGroup(
        order=2,
        generator=Suspension(
          expression=eta_2,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda pi_4^3 finite cyclic "
      "quotient calculation"
    ),
    description=(
      "If pi_3^2 is freely generated "
      "by eta_2, the kernel of the "
      "specific suspension map "
      "E: pi_3^2 -> pi_4^3 is freely "
      "generated by 2 eta_2, and that "
      "suspension map is surjective, "
      "then pi_4^3 is the cyclic group "
      "of order 2 generated by E eta_2."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaSuspensionKernelFreeCyclicStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaSuspensionSurjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_eta_family_definition_statement(
  n,
):
  if not isinstance(
    n,
    (
      int,
      ScalarSymbol,
    ),
  ):
    raise TypeError(
      "n must be an int or ScalarSymbol"
    )

  if (
    isinstance(
      n,
      int,
    )
    and n < 2
  ):
    raise ValueError(
      "eta family requires n >= 2"
    )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  if n == 2:
    name = "η₂"
    source = 3
    exponent = 0
  elif n == 3:
    name = "η₃"
    source = 4
    exponent = 1
  elif isinstance(
    n,
    int,
  ):
    name = (
      "η_"
      + str(
        n
      )
    )
    source = n + 1
    exponent = n - 2
  else:
    name = "η_n"
    source = ScalarSum(
      left=n,
      right=1,
    )
    exponent = ScalarSum(
      left=n,
      right=-2,
    )

  eta_n = HomotopyElement(
    name=name,
    dimension=n,
    source=source,
    target=n,
    generator=GeneratorSymbol(
      family="η",
      index=n,
    ),
  )

  return TodaEtaFamilyDefinitionStatement(
    index=n,
    element=eta_n,
    iterated_suspension=(
      IteratedSuspension(
        expression=eta_2,
        exponent=exponent,
      )
    ),
  )


def toda_eta3_suspension_relation_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    if (
      definition.index
      != 3
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    if (
      definition.element
      != eta_3
    ):
      return False

    return (
      definition.iterated_suspension
      == IteratedSuspension(
        expression=eta_2,
        exponent=1,
      )
    )

  def build_conclusion(
    premises,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    eta_2 = (
      definition
      .iterated_suspension
      .expression
    )

    return Relation(
      lhs=definition.element,
      rhs=Suspension(
        expression=eta_2,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda eta_3 notation "
      "suspension bridge"
    ),
    description=(
      "The eta-family definition "
      "eta_n = E^(n-2) eta_2 "
      "specializes at n=3 to "
      "eta_3 = E eta_2. "
      "This rule does not introduce "
      "a general normalization between "
      "iterated and ordinary suspension."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_higher_eta_family_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    eta_3_relation = (
      premises[
        1
      ].conclusion
    )

    n = definition.index

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    expected_eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    if (
      definition.element
      != expected_eta_n
    ):
      return False

    expected_definition = (
      IteratedSuspension(
        expression=eta_2,
        exponent=ScalarSum(
          left=n,
          right=-2,
        ),
      )
    )

    if (
      definition.iterated_suspension
      != expected_definition
    ):
      return False

    expected_eta_3_relation = Relation(
      lhs=eta_3,
      rhs=Suspension(
        expression=eta_2,
      ),
      relation_type=RelationType.EQUALITY,
    )

    return (
      eta_3_relation
      == expected_eta_3_relation
    )

  def build_conclusion(
    premises,
  ):
    definition = (
      premises[
        0
      ].conclusion
    )

    eta_3_relation = (
      premises[
        1
      ].conclusion
    )

    n = definition.index

    eta_3 = (
      eta_3_relation.lhs
    )

    return Relation(
      lhs=IteratedSuspension(
        expression=eta_3,
        exponent=ScalarSum(
          left=n,
          right=ScalarProduct(
            left=-1,
            right=3,
          ),
        ),
      ),
      rhs=definition.element,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda higher eta-family "
      "iterated suspension bridge"
    ),
    description=(
      "For the eta-family definition "
      "eta_n = E^(n-2) eta_2 and the "
      "specific relation "
      "eta_3 = E eta_2, derive the "
      "eta-family-specific relation "
      "E^(n-3) eta_3 = eta_n. "
      "This rule does not introduce "
      "generic iterated-suspension "
      "composition or normalization."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_higher_eta_finite_cyclic_generator_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    group_relation = (
      premises[
        0
      ].conclusion
    )

    eta_relation = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      group_relation.lhs,
      TodaPrimaryGroup,
    ):
      return False

    target_group = (
      group_relation.lhs
    )

    n = (
      target_group
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    expected_target_group = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
    )

    if (
      target_group
      != expected_target_group
    ):
      return False

    if not isinstance(
      group_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      group_relation.rhs.order
      != 2
    ):
      return False

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    expected_transported_generator = (
      IteratedSuspension(
        expression=eta_3,
        exponent=ScalarSum(
          left=n,
          right=ScalarProduct(
            left=-1,
            right=3,
          ),
        ),
      )
    )

    if (
      group_relation.rhs.generator
      != expected_transported_generator
    ):
      return False

    eta_n = HomotopyElement(
      name="η_n",
      dimension=n,
      source=ScalarSum(
        left=n,
        right=1,
      ),
      target=n,
      generator=GeneratorSymbol(
        family="η",
        index=n,
      ),
    )

    expected_eta_relation = Relation(
      lhs=expected_transported_generator,
      rhs=eta_n,
      relation_type=RelationType.EQUALITY,
    )

    return (
      eta_relation
      == expected_eta_relation
    )

  def build_conclusion(
    premises,
  ):
    group_relation = (
      premises[
        0
      ].conclusion
    )

    eta_relation = (
      premises[
        1
      ].conclusion
    )

    return Relation(
      lhs=group_relation.lhs,
      rhs=FiniteCyclicGroup(
        order=(
          group_relation
          .rhs
          .order
        ),
        generator=(
          eta_relation.rhs
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda higher eta-family "
      "finite-cyclic generator bridge"
    ),
    description=(
      "If pi_(n+1)^n is cyclic of "
      "order 2 generated by "
      "E^(n-3) eta_3 and the "
      "eta-family-specific bridge "
      "identifies E^(n-3) eta_3 "
      "with eta_n, then pi_(n+1)^n "
      "is cyclic of order 2 generated "
      "by eta_n. This rule does not "
      "introduce generic generator "
      "rewriting."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_pi4_3_eta3_generator_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    group_relation = (
      premises[
        0
      ].conclusion
    )

    eta_relation = (
      premises[
        1
      ].conclusion
    )

    expected_group = TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )

    if (
      group_relation.lhs
      != expected_group
    ):
      return False

    if not isinstance(
      group_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      group_relation.rhs.order
      != 2
    ):
      return False

    eta_2 = HomotopyElement(
      name="η₂",
      dimension=2,
      source=3,
      target=2,
      generator=GeneratorSymbol(
        family="η",
        index=2,
      ),
    )

    eta_3 = HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
    )

    expected_suspension = Suspension(
      expression=eta_2,
    )

    if (
      group_relation.rhs.generator
      != expected_suspension
    ):
      return False

    return (
      eta_relation.lhs
      == eta_3
      and eta_relation.rhs
      == expected_suspension
    )

  def build_conclusion(
    premises,
  ):
    group_relation = (
      premises[
        0
      ].conclusion
    )

    eta_relation = (
      premises[
        1
      ].conclusion
    )

    return Relation(
      lhs=group_relation.lhs,
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_relation.lhs,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda pi_4^3 eta_3 "
      "generator notation"
    ),
    description=(
      "If pi_4^3 is cyclic of "
      "order 2 generated by E eta_2 "
      "and eta_3 is defined as "
      "E eta_2, then pi_4^3 is "
      "cyclic of order 2 generated "
      "by eta_3."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma45_n4_two_iota3_composition_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    membership = (
      premises[0].conclusion
    )

    return (
      membership.sphere_dimension
      == 3
    )

  def build_conclusion(
    premises,
  ):
    membership = (
      premises[0].conclusion
    )

    alpha = membership.element

    iota_3 = HomotopyElement(
      name="ι_3",
      dimension=3,
      generator=GeneratorSymbol(
        family="ι",
        index=3,
      ),
    )

    return Relation(
      lhs=Composition(
        left=Multiple(
          coefficient=2,
          expression=iota_3,
        ),
        right=alpha,
      ),
      rhs=Multiple(
        coefficient=2,
        expression=alpha,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 4.5 "
      "n=4 two-iota_3 composition"
    ),
    description=(
      "For alpha in pi_i(S^3), "
      "the n=4, r=2 specialization "
      "of Toda Lemma 4.5 gives "
      "2 iota_3 composed with alpha "
      "equals 2 alpha."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomotopyGroupMembershipStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


