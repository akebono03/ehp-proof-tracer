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
  ScalarPower,
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
  FiniteHomotopyGroupStatement,
  FreeCyclicGroup,
  HomotopyEHPExactnessWindow,
  HomotopyGroup,
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
class Toda211OrdinaryEHPApplicabilityStatement:
  window: HomotopyEHPExactnessWindow
  m_is_odd: bool
  i_less_than_3m_minus_1: bool


@dataclass(frozen=True)
class Toda211OrdinaryEHPExactnessStatement:
  window: HomotopyEHPExactnessWindow


def toda_211_ordinary_ehp_applicability_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    if not isinstance(
      window,
      HomotopyEHPExactnessWindow,
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

    source = (
      window.source_term
    )

    middle = (
      window.middle_term
    )

    target = (
      window.target_term
    )

    if not isinstance(
      source,
      HomotopyGroup,
    ):
      return False

    if not isinstance(
      middle,
      HomotopyGroup,
    ):
      return False

    if not isinstance(
      target,
      HomotopyGroup,
    ):
      return False

    i = (
      source.group_dimension
    )

    m = (
      source.sphere_dimension
    )

    if not isinstance(
      i,
      int,
    ):
      return False

    if not isinstance(
      m,
      int,
    ):
      return False

    if (
      m
      <= 1
    ):
      return False

    expected_middle = HomotopyGroup(
      group_dimension=i + 1,
      sphere_dimension=m + 1,
    )

    expected_target = HomotopyGroup(
      group_dimension=i + 1,
      sphere_dimension=2 * m + 1,
    )

    if (
      middle
      != expected_middle
    ):
      return False

    if (
      target
      != expected_target
    ):
      return False

    m_is_odd = (
      m % 2
      == 1
    )

    i_less_than_threshold = (
      i
      < 3 * m - 1
    )

    return (
      m_is_odd
      or i_less_than_threshold
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    i = (
      window
      .source_term
      .group_dimension
    )

    m = (
      window
      .source_term
      .sphere_dimension
    )

    return (
      Toda211OrdinaryEHPApplicabilityStatement(
        window=window,
        m_is_odd=(
          m % 2
          == 1
        ),
        i_less_than_3m_minus_1=(
          i
          < 3 * m - 1
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda (2.11) ordinary "
      "EHP applicability"
    ),
    description=(
      "For m>1, Toda equation (2.11) "
      "is an exact sequence of ordinary "
      "homotopy groups when m is odd "
      "or i<3m-1. "
      "When m is even and i>=3m-1, "
      "Toda (2.11) is instead interpreted "
      "on the 2-primary components. "
      "This rule derives only the ordinary "
      "applicability case and is limited "
      "to concrete integer dimensions."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          HomotopyEHPExactnessWindow
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_211_ordinary_ehp_exactness_inference_rule():
  def build_conclusion(
    premises,
  ):
    applicability = (
      premises[
        0
      ].conclusion
    )

    return (
      Toda211OrdinaryEHPExactnessStatement(
        window=(
          applicability.window
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda (2.11) ordinary "
      "EHP exactness"
    ),
    description=(
      "Derive ordinary EHP exactness "
      "from an independently derived "
      "Toda (2.11) ordinary applicability "
      "statement. "
      "The structural EHP window remains "
      "an upstream premise through the "
      "applicability proof step."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda211OrdinaryEHPApplicabilityStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
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
class TodaDeltaSurjectiveStatement:
  map: TodaDeltaMap


@dataclass(frozen=True)
class TodaDeltaKernelFreeCyclicStatement:
  map: TodaDeltaMap
  kernel_group: FreeCyclicGroup


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
class TodaDeltaImageUpToSignStatement:
  map: TodaDeltaMap
  element: Expression
  positive_value: Expression


@dataclass(frozen=True)
class TodaDeltaPreimageUpToSignStatement:
  map: TodaDeltaMap
  value: Expression
  positive_preimage: Expression


@dataclass(frozen=True)
class TodaPi32WhiteheadSquareUpToSignStatement:
  whitehead_square: Expression
  positive_value: Expression


@dataclass(frozen=True)
class Toda58WhiteheadSquareUpToSignStatement:
  whitehead_square: WhiteheadProduct
  positive_value: Expression


@dataclass(frozen=True)
class Toda58EquationStatement:
  delta_nu_relation: TodaDeltaImageUpToSignStatement
  whitehead_nu_relation: Toda58WhiteheadSquareUpToSignStatement
  delta_whitehead_relation: TodaDeltaImageUpToSignStatement
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


@dataclass(frozen=True)
class TodaLemma57TwoIota5ImageMembershipStatement:
  element: IteratedSuspension
  source_group: TodaPrimaryGroup


def serre_42_finite_homotopy_group_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    group = (
      premises[
        0
      ].conclusion
    )

    if not isinstance(
      group,
      HomotopyGroup,
    ):
      return False

    i = (
      group
      .group_dimension
    )

    n = (
      group
      .sphere_dimension
    )

    if not isinstance(
      i,
      int,
    ):
      return False

    if not isinstance(
      n,
      int,
    ):
      return False

    if (
      i
      == n
    ):
      return False

    if (
      i
      == 2 * n - 1
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    group = (
      premises[
        0
      ].conclusion
    )

    return (
      FiniteHomotopyGroupStatement(
        group=group,
      )
    )

  return InferenceRule(
    name=(
      "Serre (4.2) "
      "finite homotopy group"
    ),
    description=(
      "Apply Serre's finiteness theorem "
      "as quoted in Toda (4.2): "
      "pi_i(S^n) is finite except when "
      "i=n or i=2n-1. "
      "This Phase 72R-4 rule is limited "
      "to concrete integer dimensions. "
      "It does not introduce symbolic "
      "inequality reasoning or primary "
      "decomposition semantics."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          HomotopyGroup
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma57_e2_eta2_alpha_composition_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hypothesis = (
      premises[
        0
      ].conclusion
    )

    if not isinstance(
      hypothesis.element,
      IteratedSuspension,
    ):
      return False

    if (
      hypothesis.element.exponent
      != 2
    ):
      return False

    alpha = (
      hypothesis
      .element
      .expression
    )

    if not isinstance(
      alpha,
      HomotopyElement,
    ):
      return False

    i = alpha.source

    if not isinstance(
      i,
      (
        int,
        ScalarSymbol,
      ),
    ):
      return False

    if (
      alpha.target
      != 3
    ):
      return False

    expected_source_group = (
      TodaPrimaryGroup(
        group_dimension=(
          (
            i + 2
          )
          if isinstance(
            i,
            int,
          )
          else ScalarSum(
            left=i,
            right=2,
          )
        ),
        sphere_dimension=5,
      )
    )

    return (
      hypothesis.source_group
      == expected_source_group
    )

  def build_conclusion(
    premises,
  ):
    hypothesis = (
      premises[
        0
      ].conclusion
    )

    alpha = (
      hypothesis
      .element
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
      lhs=IteratedSuspension(
        expression=Composition(
          left=eta_2,
          right=alpha,
        ),
        exponent=2,
      ),
      rhs=Composition(
        left=eta_4,
        right=hypothesis.element,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.7 "
      "double suspension composition"
    ),
    description=(
      "For the Lemma 5.7 hypothesis "
      "E^2 alpha in "
      "2 iota_5 composed with "
      "pi_(i+2)(S^5), derive the "
      "specific suspension identity "
      "E^2(eta_2 composed with alpha) "
      "= eta_4 composed with E^2 alpha. "
      "The homotopy-group index i is "
      "read from the source dimension "
      "of alpha, allowing both symbolic "
      "alpha and concrete elements such "
      "as nu-prime. "
      "No generic suspension-composition "
      "normalizer is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaLemma57TwoIota5ImageMembershipStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma57_e2_eta2_alpha_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hypothesis = (
      premises[
        0
      ].conclusion
    )

    composition_relation = (
      premises[
        1
      ].conclusion
    )

    eta4_zero = (
      premises[
        2
      ].conclusion
    )

    if not isinstance(
      hypothesis.element,
      IteratedSuspension,
    ):
      return False

    if (
      hypothesis.element.exponent
      != 2
    ):
      return False

    alpha = (
      hypothesis
      .element
      .expression
    )

    if not isinstance(
      alpha,
      HomotopyElement,
    ):
      return False

    i = alpha.source

    if not isinstance(
      i,
      (
        int,
        ScalarSymbol,
      ),
    ):
      return False

    if (
      alpha.target
      != 3
    ):
      return False

    expected_group_dimension = (
      (
        i + 2
      )
      if isinstance(
        i,
        int,
      )
      else ScalarSum(
        left=i,
        right=2,
      )
    )

    expected_source_group = (
      TodaPrimaryGroup(
        group_dimension=(
          expected_group_dimension
        ),
        sphere_dimension=5,
      )
    )

    if (
      hypothesis.source_group
      != expected_source_group
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

    expected_composition_relation = (
      Relation(
        lhs=IteratedSuspension(
          expression=Composition(
            left=eta_2,
            right=alpha,
          ),
          exponent=2,
        ),
        rhs=Composition(
          left=eta_4,
          right=hypothesis.element,
        ),
        relation_type=RelationType.EQUALITY,
      )
    )

    if (
      composition_relation
      != expected_composition_relation
    ):
      return False

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
    composition_relation = (
      premises[
        1
      ].conclusion
    )

    return Relation(
      lhs=composition_relation.lhs,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.7 "
      "double suspension zero"
    ),
    description=(
      "For the Lemma 5.7 hypothesis "
      "E^2 alpha in "
      "2 iota_5 composed with "
      "pi_(i+2)(S^5), use "
      "E^2(eta_2 alpha)=eta_4 E^2 alpha "
      "and the independently derived "
      "2 eta_4=0 relation to obtain "
      "E^2(eta_2 alpha)=0. "
      "The homotopy-group index is read "
      "from alpha.source so concrete "
      "nu-prime specialization is "
      "accepted without changing the "
      "generic HomotopyElement model. "
      "No generic image algebra is "
      "introduced."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaLemma57TwoIota5ImageMembershipStatement
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
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma45_n3_suspension_zero_reflection_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hypothesis = (
      premises[
        0
      ].conclusion
    )

    double_suspension_zero = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      hypothesis.element,
      IteratedSuspension,
    ):
      return False

    if (
      hypothesis.element.exponent
      != 2
    ):
      return False

    alpha = (
      hypothesis
      .element
      .expression
    )

    if not isinstance(
      alpha,
      HomotopyElement,
    ):
      return False

    i = alpha.source

    if not isinstance(
      i,
      (
        int,
        ScalarSymbol,
      ),
    ):
      return False

    if (
      alpha.target
      != 3
    ):
      return False

    expected_group_dimension = (
      (
        i + 2
      )
      if isinstance(
        i,
        int,
      )
      else ScalarSum(
        left=i,
        right=2,
      )
    )

    expected_source_group = (
      TodaPrimaryGroup(
        group_dimension=(
          expected_group_dimension
        ),
        sphere_dimension=5,
      )
    )

    if (
      hypothesis.source_group
      != expected_source_group
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

    eta2_alpha = Composition(
      left=eta_2,
      right=alpha,
    )

    expected_double_suspension_zero = (
      Relation(
        lhs=IteratedSuspension(
          expression=eta2_alpha,
          exponent=2,
        ),
        rhs=Zero(),
        relation_type=RelationType.ZERO,
      )
    )

    return (
      double_suspension_zero
      == expected_double_suspension_zero
    )

  def build_conclusion(
    premises,
  ):
    hypothesis = (
      premises[
        0
      ].conclusion
    )

    alpha = (
      hypothesis
      .element
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

    return Relation(
      lhs=Suspension(
        expression=Composition(
          left=eta_2,
          right=alpha,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 4.5 "
      "n=3 suspension zero reflection"
    ),
    description=(
      "For the Toda Lemma 5.7 branch, "
      "apply the n=3 injectivity "
      "consequence of Toda Lemma 4.5. "
      "If E^2(eta_2 composed with alpha) "
      "is zero, then "
      "E(eta_2 composed with alpha) "
      "is zero. "
      "The homotopy-group index is read "
      "from alpha.source, supporting "
      "both symbolic alpha and concrete "
      "nu-prime. "
      "No generic suspension-zero "
      "reflection rule is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        statement_type=(
          TodaLemma57TwoIota5ImageMembershipStatement
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


def toda_lemma57_nu_prime_hypothesis_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    lemma54_statement = (
      premises[
        0
      ].conclusion
    )

    nu5_definition = (
      premises[
        1
      ].conclusion
    )

    expected_nu5_definition = (
      toda_nu_family_definition_statement(
        5
      )
    )

    if (
      nu5_definition
      != expected_nu5_definition
    ):
      return False

    nu_4 = (
      lemma54_statement
      .nu4
    )

    if (
      nu5_definition
      .iterated_suspension
      .expression
      != nu_4
    ):
      return False

    if (
      nu5_definition
      .iterated_suspension
      .exponent
      != 1
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

    expected_double_relation = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=Suspension(
          expression=nu_4,
        ),
      ),
      rhs=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      relation_type=RelationType.EQUALITY,
    )

    return (
      lemma54_statement
      .double_suspension_relation
      == expected_double_relation
    )

  def build_conclusion(
    premises,
  ):
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
      TodaLemma57TwoIota5ImageMembershipStatement(
        element=IteratedSuspension(
          expression=nu_prime,
          exponent=2,
        ),
        source_group=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=5,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.7 "
      "nu-prime hypothesis"
    ),
    description=(
      "Specialize Toda Lemma 5.4 and "
      "the concrete nu_5 definition. "
      "Lemma 5.4 gives "
      "2 E nu_4 = E^2 nu-prime, while "
      "nu_5 is defined by E nu_4. "
      "Therefore E^2 nu-prime lies in "
      "2 iota_5 composed with pi_8(S^5), "
      "which is exactly the hypothesis "
      "needed to reuse the general "
      "Toda Lemma 5.7 inference chain. "
      "No generic image-membership or "
      "existential-witness machinery "
      "is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Statement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma57_pi6_2_eta2_nu_prime_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop56_statement = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
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

    expected_pi6_3_relation = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=nu_prime,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      prop56_statement
      .pi6_3_group_relation
      != expected_pi6_3_relation
    ):
      return False

    source_group = (
      isomorphism
      .source_group
    )

    target_group = (
      isomorphism
      .target_group
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
      isomorphism
      .composition
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

    gamma = (
      composition
      .right
    )

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
    prop56_statement = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    nu_prime = (
      prop56_statement
      .pi6_3_group_relation
      .rhs
      .generator
    )

    eta_2 = (
      isomorphism
      .composition
      .left
    )

    eta2_nu_prime = Composition(
      left=eta_2,
      right=nu_prime,
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=eta2_nu_prime,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.7 "
      "pi_6^2 eta_2 nu-prime"
    ),
    description=(
      "Use the independently derived "
      "finite-dimensional Toda "
      "Proposition 5.6 relation "
      "pi_6^3=Z/4{nu-prime} "
      "together with the independently "
      "derived Toda (5.2) composition "
      "isomorphism "
      "eta_2 composed with minus from "
      "pi_i^3 to pi_i^2. "
      "Transport the concrete generator "
      "nu-prime to "
      "eta_2 composed with nu-prime "
      "and derive "
      "pi_6^2=Z/4{eta_2 nu-prime}. "
      "No generic cyclic-generator "
      "transport framework is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp56FiniteDimensionalStatement
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


def toda_lemma57_concrete_delta_e_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
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

    return (
      window.source_term
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
      and window.middle_term
      == TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      )
      and window.target_term
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=3,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    return TodaProp42ExactnessStatement(
      window=window,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.7 "
      "concrete Delta-E exactness"
    ),
    description=(
      "Recognize the concrete Toda "
      "(4.4) exact sequence segment "
      "pi_8^5 -> pi_6^2 -> pi_7^3 "
      "with Delta followed by suspension E. "
      "This narrow bridge avoids changing "
      "the existing symbolic Proposition 4.2 "
      "Delta-E exactness rule."
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


def toda_lemma57_delta_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    eta2_nu_prime_zero = (
      premises[
        0
      ].conclusion
    )

    pi6_2_relation = (
      premises[
        1
      ].conclusion
    )

    exactness = (
      premises[
        2
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

    eta2_nu_prime = Composition(
      left=eta_2,
      right=nu_prime,
    )

    expected_zero = Relation(
      lhs=Suspension(
        expression=eta2_nu_prime,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      eta2_nu_prime_zero
      != expected_zero
    ):
      return False

    expected_pi6_2_relation = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=eta2_nu_prime,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi6_2_relation
      != expected_pi6_2_relation
    ):
      return False

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

    return (
      window.source_term
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
      and window.middle_term
      == TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      )
      and window.target_term
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=3,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        2
      ].conclusion
    )

    window = exactness.window

    return TodaDeltaSurjectiveStatement(
      map=TodaDeltaMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.7 "
      "Delta surjective"
    ),
    description=(
      "Phase 67 gives "
      "E(eta_2 composed with nu-prime)=0 "
      "and pi_6^2=Z/4 generated by "
      "eta_2 composed with nu-prime. "
      "Thus suspension E is zero on "
      "the concrete cyclic group pi_6^2. "
      "Exactness of "
      "pi_8^5 -> pi_6^2 -> pi_7^3 "
      "therefore makes Delta surjective."
    ),
    premise_patterns=(
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
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma57_delta_nu5_generator_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_surjective = (
      premises[
        0
      ].conclusion
    )

    pi6_2_relation = (
      premises[
        1
      ].conclusion
    )

    prop56_statement = (
      premises[
        2
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

    eta2_nu_prime = Composition(
      left=eta_2,
      right=nu_prime,
    )

    expected_pi6_2_relation = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=eta2_nu_prime,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi6_2_relation
      != expected_pi6_2_relation
    ):
      return False

    expected_delta_map = TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      ),
    )

    if (
      delta_surjective.map
      != expected_delta_map
    ):
      return False

    pi8_5_relation = (
      prop56_statement
      .pi8_5_group_relation
    )

    if (
      pi8_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi8_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi8_5_relation.rhs.order
      != 8
    ):
      return False

    nu_5 = (
      pi8_5_relation
      .rhs
      .generator
    )

    expected_nu_5 = (
      toda_nu_family_definition_statement(
        5
      ).element
    )

    return (
      nu_5
      == expected_nu_5
    )

  def build_conclusion(
    premises,
  ):
    delta_surjective = (
      premises[
        0
      ].conclusion
    )

    pi6_2_relation = (
      premises[
        1
      ].conclusion
    )

    prop56_statement = (
      premises[
        2
      ].conclusion
    )

    nu_5 = (
      prop56_statement
      .pi8_5_group_relation
      .rhs
      .generator
    )

    eta2_nu_prime = (
      pi6_2_relation
      .rhs
      .generator
    )

    return TodaDeltaImageUpToSignStatement(
      map=delta_surjective.map,
      element=nu_5,
      positive_value=eta2_nu_prime,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.7 "
      "Delta nu_5 generator"
    ),
    description=(
      "For the concrete surjective Delta "
      "from pi_8^5 to pi_6^2, "
      "Proposition 5.6 gives "
      "pi_8^5=Z/8{nu_5}, while "
      "Phase 67 gives "
      "pi_6^2=Z/4{eta_2 nu-prime}. "
      "The image of the canonical "
      "nu-family source generator "
      "therefore generates the target "
      "cyclic group. "
      "In Toda's up-to-sign convention, "
      "derive "
      "Delta(nu_5)=plus or minus "
      "(eta_2 composed with nu-prime). "
      "No generic cyclic-image solver "
      "or generic sign algebra is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaSurjectiveStatement
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
          TodaProp56FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_concrete_e_h_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
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

    return (
      window.source_term
      == TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      )
      and window.middle_term
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=3,
      )
      and window.target_term
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=5,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    return TodaProp42ExactnessStatement(
      window=window,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "concrete E-H exactness"
    ),
    description=(
      "Recognize the concrete Toda "
      "(4.4) exact sequence segment "
      "pi_6^2 -> pi_7^3 -> pi_7^5 "
      "with suspension E followed by "
      "the Hopf invariant H. "
      "This narrow bridge avoids "
      "adding integer scalar "
      "normalization to the existing "
      "symbolic Proposition 4.2 "
      "E-H exactness rule."
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


def toda_prop58_pi7_3_hopf_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    eta2_nu_prime_zero = (
      premises[
        0
      ].conclusion
    )

    pi6_2_relation = (
      premises[
        1
      ].conclusion
    )

    exactness = (
      premises[
        2
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

    eta2_nu_prime = Composition(
      left=eta_2,
      right=nu_prime,
    )

    expected_zero = Relation(
      lhs=Suspension(
        expression=eta2_nu_prime,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      eta2_nu_prime_zero
      != expected_zero
    ):
      return False

    expected_pi6_2_relation = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=eta2_nu_prime,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi6_2_relation
      != expected_pi6_2_relation
    ):
      return False

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

    return (
      window.source_term
      == TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      )
      and window.middle_term
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=3,
      )
      and window.target_term
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=5,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        2
      ].conclusion
    )

    window = exactness.window

    return TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_7^3 Hopf injective"
    ),
    description=(
      "Phase 67 gives "
      "pi_6^2=Z/4 generated by "
      "eta_2 composed with nu-prime "
      "and E(eta_2 composed with "
      "nu-prime)=0. "
      "Therefore suspension E is zero "
      "on this concrete cyclic group. "
      "Exactness of "
      "pi_6^2 -> pi_7^3 -> pi_7^5 "
      "then gives Ker(H)=Im(E)=0, "
      "so the Hopf invariant "
      "H:pi_7^3 to pi_7^5 "
      "is injective. "
      "No generic zero-map solver "
      "is introduced."
    ),
    premise_patterns=(
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
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_pi7_3_finite_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    equation57 = (
      premises[
        1
      ].conclusion
    )

    prop53 = (
      premises[
        2
      ].conclusion
    )

    pi7_3 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )

    pi7_5 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=5,
    )

    if (
      isomorphism.map
      != TodaHopfInvariantMap(
        source_group=pi7_3,
        target_group=pi7_5,
      )
    ):
      return False

    if not isinstance(
      equation57.lhs,
      MapApplication,
    ):
      return False

    if (
      equation57.lhs.map
      != EHP_H_MAP
    ):
      return False

    if not isinstance(
      equation57.lhs.expression,
      Composition,
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

    nu_prime_eta6 = Composition(
      left=nu_prime,
      right=eta_6,
    )

    eta5_squared = Composition(
      left=eta_5,
      right=eta_6,
    )

    if (
      equation57.lhs.expression
      != nu_prime_eta6
    ):
      return False

    if (
      equation57.rhs
      != eta5_squared
    ):
      return False

    higher_relation = (
      prop53
      .higher_eta_squared_group_relation
    )

    higher_range = (
      prop53
      .higher_range
    )

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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
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
      higher_relation
      .rhs
      .generator
      == eta_n_squared
    )

  def build_conclusion(
    premises,
  ):
    equation57 = (
      premises[
        1
      ].conclusion
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=(
          equation57
          .lhs
          .expression
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_7^3 finite cyclic"
    ),
    description=(
      "Use the independently derived "
      "Hopf isomorphism "
      "H:pi_7^3 to pi_7^5, "
      "Toda (5.7) "
      "H(nu-prime composed with eta_6)"
      "=eta_5 squared, "
      "and the symbolic finite-dimensional "
      "Proposition 5.3 result "
      "pi_(n+2)^n=Z/2 generated by "
      "eta_n squared for n at least 5. "
      "Specializing that existing "
      "higher branch to n=5 gives the "
      "target cyclic group of order two. "
      "Transport the concrete generator "
      "eta_5 squared back through the "
      "Hopf isomorphism to obtain "
      "pi_7^3=Z/2 generated by "
      "nu-prime composed with eta_6. "
      "No concrete Proposition 5.3 "
      "specialization statement or "
      "generic cyclic-group isomorphism "
      "transport framework is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantIsomorphismStatement
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
          TodaProp53FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_e_nu_prime_eta6_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi7_3_relation = (
      premises[
        0
      ].conclusion
    )

    prop51 = (
      premises[
        1
      ].conclusion
    )

    pi_7_3 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )

    if (
      pi7_3_relation.lhs
      != pi_7_3
    ):
      return False

    if not isinstance(
      pi7_3_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi7_3_relation.rhs.order
      != 2
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

    nu_prime_eta6 = Composition(
      left=nu_prime,
      right=eta_6,
    )

    if (
      pi7_3_relation
      .rhs
      .generator
      != nu_prime_eta6
    ):
      return False

    higher_relation = (
      prop51
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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
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
    pi7_3_relation = (
      premises[
        0
      ].conclusion
    )

    nu_prime_eta6 = (
      pi7_3_relation
      .rhs
      .generator
    )

    nu_prime = (
      nu_prime_eta6.left
    )

    eta_7 = HomotopyElement(
      name="η₇",
      dimension=7,
      source=8,
      target=7,
      generator=GeneratorSymbol(
        family="η",
        index=7,
      ),
    )

    return Relation(
      lhs=Suspension(
        expression=nu_prime_eta6,
      ),
      rhs=Composition(
        left=Suspension(
          expression=nu_prime,
        ),
        right=eta_7,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "E nu-prime eta_6 bridge"
    ),
    description=(
      "Use the independently derived "
      "group pi_7^3=Z/2 generated by "
      "nu-prime composed with eta_6 "
      "together with the independently "
      "derived Proposition 5.1 "
      "higher eta-family relation. "
      "For the concrete n=7 instance, "
      "suspension functoriality gives "
      "E(nu-prime composed with eta_6) "
      "=E nu-prime composed with eta_7. "
      "This is a narrow Proposition 5.8 "
      "bridge and does not introduce "
      "generic symbolic specialization "
      "or suspension normalization."
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


def toda_prop58_pi8_4_decomposition_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda56 = (
      premises[
        0
      ].conclusion
    )

    pi7_3_relation = (
      premises[
        1
      ].conclusion
    )

    prop51 = (
      premises[
        2
      ].conclusion
    )

    suspension_bridge = (
      premises[
        3
      ].conclusion
    )

    decomposition_statement = (
      toda56
      .decomposition_isomorphism
    )

    prop44_isomorphism = (
      decomposition_statement
      .prop44_isomorphism
    )

    decomposition_map = (
      prop44_isomorphism.map
    )

    if not isinstance(
      decomposition_map,
      TodaProp44DecompositionMap,
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
      target_group
      .group_dimension
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    if (
      target_group
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=4,
      )
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
      source_group.summands
      != (
        TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=i,
            right=-1,
          ),
          sphere_dimension=3,
        ),
        TodaPrimaryGroup(
          group_dimension=i,
          sphere_dimension=7,
        ),
      )
    ):
      return False

    nu_4 = HomotopyElement(
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
      decomposition_map.alpha
      != nu_4
    ):
      return False

    if (
      decomposition_map.formula
      != Sum(
        left=Suspension(
          expression=decomposition_map.beta,
        ),
        right=Composition(
          left=nu_4,
          right=decomposition_map.gamma,
        ),
      )
    ):
      return False

    pi_7_3 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )

    if (
      pi7_3_relation.lhs
      != pi_7_3
    ):
      return False

    if not isinstance(
      pi7_3_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi7_3_relation.rhs.order
      != 2
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

    nu_prime_eta6 = Composition(
      left=nu_prime,
      right=eta_6,
    )

    if (
      pi7_3_relation
      .rhs
      .generator
      != nu_prime_eta6
    ):
      return False

    higher_relation = (
      prop51
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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
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

    if (
      higher_relation
      .rhs
      .generator
      != eta_n
    ):
      return False

    eta_7 = HomotopyElement(
      name="η₇",
      dimension=7,
      source=8,
      target=7,
      generator=GeneratorSymbol(
        family="η",
        index=7,
      ),
    )

    expected_bridge = Relation(
      lhs=Suspension(
        expression=nu_prime_eta6,
      ),
      rhs=Composition(
        left=Suspension(
          expression=nu_prime,
        ),
        right=eta_7,
      ),
      relation_type=RelationType.EQUALITY,
    )

    return (
      suspension_bridge
      == expected_bridge
    )

  def build_conclusion(
    premises,
  ):
    toda56 = (
      premises[
        0
      ].conclusion
    )

    suspension_bridge = (
      premises[
        3
      ].conclusion
    )

    nu_4 = (
      toda56
      .lemma54_statement
      .nu4
    )

    eta_7 = (
      suspension_bridge
      .rhs
      .right
    )

    e_nu_prime_eta7 = (
      suspension_bridge.rhs
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=4,
      ),
      rhs=DirectSumGroup(
        summands=(
          FiniteCyclicGroup(
            order=2,
            generator=Composition(
              left=nu_4,
              right=eta_7,
            ),
          ),
          FiniteCyclicGroup(
            order=2,
            generator=e_nu_prime_eta7,
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_8^4 decomposition"
    ),
    description=(
      "Specialize the independently "
      "derived Toda (5.6) decomposition "
      "pi_(i-1)^3 direct sum pi_i^7 "
      "isomorphic to pi_i^4 at i=8. "
      "Use the independently derived "
      "pi_7^3=Z/2 generated by "
      "nu-prime composed with eta_6 "
      "and the Proposition 5.1 "
      "n=7 instance "
      "pi_8^7=Z/2 generated by eta_7. "
      "The first summand maps to "
      "E(nu-prime eta_6), identified "
      "by the concrete bridge with "
      "E nu-prime composed with eta_7. "
      "The second summand maps to "
      "nu_4 composed with eta_7. "
      "Therefore pi_8^4 is the direct "
      "sum of the two order-two cyclic "
      "groups generated by these "
      "elements. "
      "No generic direct-sum transport "
      "or theorem specialization "
      "framework is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda56Nu4DecompositionStatement
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
          TodaProp51FiniteDimensionalStatement
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


def toda_prop25_delta_eta9_composition_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda58 = (
      premises[
        0
      ].conclusion
    )

    delta_iota9 = (
      toda58
      .delta_nu_relation
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )

    if (
      delta_iota9.map
      != TodaDeltaMap(
        source_group=expected_source,
        target_group=expected_target,
      )
    ):
      return False

    iota_9 = HomotopyElement(
      name="ι_9",
      dimension=9,
      generator=GeneratorSymbol(
        family="ι",
        index=9,
      ),
    )

    if (
      delta_iota9.element
      != iota_9
    ):
      return False

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
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

    expected_positive_value = Sum(
      left=Multiple(
        coefficient=2,
        expression=nu_4,
      ),
      right=Multiple(
        coefficient=-1,
        expression=Suspension(
          expression=nu_prime,
        ),
      ),
    )

    return (
      delta_iota9
      .positive_value
      == expected_positive_value
    )

  def build_conclusion(
    premises,
  ):
    toda58 = (
      premises[
        0
      ].conclusion
    )

    delta_iota9 = (
      toda58
      .delta_nu_relation
    )

    eta_7 = HomotopyElement(
      name="η₇",
      dimension=7,
      source=8,
      target=7,
      generator=GeneratorSymbol(
        family="η",
        index=7,
      ),
    )

    eta_9 = HomotopyElement(
      name="η₉",
      dimension=9,
      source=10,
      target=9,
      generator=GeneratorSymbol(
        family="η",
        index=9,
      ),
    )

    return TodaDeltaImageUpToSignStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=9,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=4,
        ),
      ),
      element=eta_9,
      positive_value=Composition(
        left=(
          delta_iota9
          .positive_value
        ),
        right=eta_7,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 2.5 "
      "Delta eta_9 composition"
    ),
    description=(
      "Apply the concrete Proposition 2.5 "
      "composition formula to the "
      "independently derived Toda (5.8) "
      "relation "
      "Delta(iota_9)=plus or minus "
      "(2 nu_4-E nu-prime). "
      "For eta_9, the relevant right "
      "factor is eta_7, giving "
      "Delta(eta_9)=plus or minus "
      "((2 nu_4-E nu-prime) "
      "composed with eta_7). "
      "The expression is deliberately "
      "left undistributed. "
      "No generic Delta-composition, "
      "distributivity, or sign algebra "
      "framework is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda58EquationStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_delta_eta9_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_eta9 = (
      premises[
        0
      ].conclusion
    )

    pi8_4_relation = (
      premises[
        1
      ].conclusion
    )

    expected_delta_map = TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=9,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=4,
      ),
    )

    if (
      delta_eta9.map
      != expected_delta_map
    ):
      return False

    eta_9 = HomotopyElement(
      name="η₉",
      dimension=9,
      source=10,
      target=9,
      generator=GeneratorSymbol(
        family="η",
        index=9,
      ),
    )

    if (
      delta_eta9.element
      != eta_9
    ):
      return False

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
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

    eta_7 = HomotopyElement(
      name="η₇",
      dimension=7,
      source=8,
      target=7,
      generator=GeneratorSymbol(
        family="η",
        index=7,
      ),
    )

    expected_positive_value = Composition(
      left=Sum(
        left=Multiple(
          coefficient=2,
          expression=nu_4,
        ),
        right=Multiple(
          coefficient=-1,
          expression=Suspension(
            expression=nu_prime,
          ),
        ),
      ),
      right=eta_7,
    )

    if (
      delta_eta9.positive_value
      != expected_positive_value
    ):
      return False

    pi_8_4 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    )

    if (
      pi8_4_relation.lhs
      != pi_8_4
    ):
      return False

    if not isinstance(
      pi8_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi8_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    first_summand = (
      pi8_4_relation
      .rhs
      .summands[
        0
      ]
    )

    second_summand = (
      pi8_4_relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      first_summand,
      FiniteCyclicGroup,
    ):
      return False

    if not isinstance(
      second_summand,
      FiniteCyclicGroup,
    ):
      return False

    if (
      first_summand.order
      != 2
    ):
      return False

    if (
      second_summand.order
      != 2
    ):
      return False

    nu4_eta7 = Composition(
      left=nu_4,
      right=eta_7,
    )

    e_nu_prime_eta7 = Composition(
      left=Suspension(
        expression=nu_prime,
      ),
      right=eta_7,
    )

    if (
      first_summand.generator
      != nu4_eta7
    ):
      return False

    return (
      second_summand.generator
      == e_nu_prime_eta7
    )

  def build_conclusion(
    premises,
  ):
    pi8_4_relation = (
      premises[
        1
      ].conclusion
    )

    e_nu_prime_eta7 = (
      pi8_4_relation
      .rhs
      .summands[
        1
      ]
      .generator
    )

    eta_9 = (
      premises[
        0
      ].conclusion
      .element
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=eta_9,
      ),
      rhs=e_nu_prime_eta7,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "Delta eta_9 value"
    ),
    description=(
      "Use the Proposition 2.5 "
      "specialization "
      "Delta(eta_9)=plus or minus "
      "((2 nu_4-E nu-prime) eta_7) "
      "together with the independently "
      "derived decomposition "
      "pi_8^4="
      "Z/2{nu_4 eta_7} direct sum "
      "Z/2{E nu-prime eta_7}. "
      "The first summand has order two, "
      "so 2 nu_4 eta_7 is zero. "
      "The second summand also has "
      "order two, so negation and the "
      "remaining up-to-sign ambiguity "
      "do not change its generator. "
      "Therefore "
      "Delta(eta_9)=E nu-prime eta_7. "
      "This is a concrete Proposition 5.8 "
      "simplification and does not add "
      "generic distributivity, order-two "
      "sign elimination, or sign algebra."
    ),
    premise_patterns=(
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


def toda_prop58_pi9_5_concrete_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    delta_e_window = (
      TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=9,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=4,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=5,
        ),
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      )
    )

    e_h_window = (
      TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=4,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=5,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=9,
        ),
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      )
    )

    h_delta_window = (
      TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=5,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=9,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=7,
          sphere_dimension=4,
        ),
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
      )
    )

    return (
      window
      in (
        delta_e_window,
        e_h_window,
        h_delta_window,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_9^5 concrete exactness"
    ),
    description=(
      "Recognize only the three concrete "
      "EHP exact sequence windows needed "
      "for the Proposition 5.8 "
      "calculation of pi_9^5: "
      "pi_10^9 -> pi_8^4 -> pi_9^5, "
      "pi_8^4 -> pi_9^5 -> pi_9^9, "
      "and pi_9^5 -> pi_9^9 -> pi_7^4. "
      "No scalar normalization or "
      "general concrete EHP specialization "
      "framework is introduced."
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


def toda_prop58_pi9_9_delta_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda58 = (
      premises[
        0
      ].conclusion
    )

    prop56 = (
      premises[
        1
      ].conclusion
    )

    delta_relation = (
      toda58
      .delta_nu_relation
    )

    pi_9_9 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
    )

    pi_7_4 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )

    if (
      delta_relation.map
      != TodaDeltaMap(
        source_group=pi_9_9,
        target_group=pi_7_4,
      )
    ):
      return False

    iota_9 = HomotopyElement(
      name="ι_9",
      dimension=9,
      generator=GeneratorSymbol(
        family="ι",
        index=9,
      ),
    )

    if (
      delta_relation.element
      != iota_9
    ):
      return False

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
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

    expected_value = Sum(
      left=Multiple(
        coefficient=2,
        expression=nu_4,
      ),
      right=Multiple(
        coefficient=-1,
        expression=Suspension(
          expression=nu_prime,
        ),
      ),
    )

    if (
      delta_relation.positive_value
      != expected_value
    ):
      return False

    relation = (
      prop56
      .pi7_4_group_relation
    )

    if (
      relation.lhs
      != pi_7_4
    ):
      return False

    if not isinstance(
      relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        relation.rhs.summands
      )
      != 2
    ):
      return False

    free_summand = (
      relation
      .rhs
      .summands[
        0
      ]
    )

    torsion_summand = (
      relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      free_summand,
      FreeCyclicGroup,
    ):
      return False

    if (
      free_summand.generator
      != nu_4
    ):
      return False

    if not isinstance(
      torsion_summand,
      FiniteCyclicGroup,
    ):
      return False

    return (
      torsion_summand.order
      == 4
      and torsion_summand.generator
      == Suspension(
        expression=nu_prime,
      )
    )

  def build_conclusion(
    premises,
  ):
    delta_relation = (
      premises[
        0
      ].conclusion
      .delta_nu_relation
    )

    return TodaDeltaInjectiveStatement(
      map=delta_relation.map,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_9^9 Delta injective"
    ),
    description=(
      "Toda (5.8) gives "
      "Delta(iota_9)=plus or minus "
      "(2 nu_4-E nu-prime). "
      "Proposition 5.6 gives "
      "pi_7^4=Z{nu_4} direct sum "
      "Z/4{E nu-prime}. "
      "The image of the source generator "
      "has nonzero free component "
      "2 nu_4 and therefore infinite "
      "order. Hence the concrete Delta "
      "from pi_9^9 to pi_7^4 is "
      "injective. "
      "No generic infinite-order or "
      "direct-sum injectivity solver "
      "is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda58EquationStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp56FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_pi9_5_hopf_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    injective = (
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
      group_dimension=9,
      sphere_dimension=5,
    )

    expected_middle = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
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
      injective.map
      == TodaDeltaMap(
        source_group=expected_middle,
        target_group=expected_target,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[
        1
      ].conclusion
      .window
    )

    return TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_9^5 Hopf zero"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_9^5 -> pi_9^9 -> pi_7^4, "
      "injectivity of Delta makes "
      "Ker(Delta)=0. Exactness gives "
      "Im(H)=0, so the Hopf invariant "
      "H from pi_9^5 to pi_9^9 "
      "is zero."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_pi9_5_suspension_surjective_inference_rule():
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

    pi_8_4 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    )

    pi_9_5 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )

    pi_9_9 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
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
      != pi_8_4
    ):
      return False

    if (
      window.middle_term
      != pi_9_5
    ):
      return False

    if (
      window.target_term
      != pi_9_9
    ):
      return False

    return (
      hopf_zero.map
      == TodaHopfInvariantMap(
        source_group=pi_9_5,
        target_group=pi_9_9,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[
        1
      ].conclusion
      .window
    )

    return TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_9^5 suspension surjective"
    ),
    description=(
      "For the concrete exact sequence "
      "pi_8^4 -> pi_9^5 -> pi_9^9, "
      "the Hopf map is zero. "
      "Therefore Ker(H)=pi_9^5. "
      "Exactness gives Im(E)=pi_9^5, "
      "so suspension "
      "E:pi_8^4 to pi_9^5 "
      "is surjective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantZeroStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_e_nu4_eta7_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi8_4_relation = (
      premises[
        0
      ].conclusion
    )

    prop51 = (
      premises[
        1
      ].conclusion
    )

    nu5_definition = (
      premises[
        2
      ].conclusion
    )

    if (
      pi8_4_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=4,
      )
    ):
      return False

    if not isinstance(
      pi8_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi8_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
      ),
    )

    eta_7 = HomotopyElement(
      name="η₇",
      dimension=7,
      source=8,
      target=7,
      generator=GeneratorSymbol(
        family="η",
        index=7,
      ),
    )

    expected_first = FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=nu_4,
        right=eta_7,
      ),
    )

    if (
      pi8_4_relation
      .rhs
      .summands[
        0
      ]
      != expected_first
    ):
      return False

    higher_relation = (
      prop51
      .higher_eta_group_relation
    )

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
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
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

    if (
      higher_relation
      .rhs
      .generator
      != eta_n
    ):
      return False

    return (
      nu5_definition
      == toda_nu_family_definition_statement(
        5
      )
    )

  def build_conclusion(
    premises,
  ):
    pi8_4_relation = (
      premises[
        0
      ].conclusion
    )

    nu4_eta7 = (
      pi8_4_relation
      .rhs
      .summands[
        0
      ]
      .generator
    )

    nu_5 = (
      premises[
        2
      ].conclusion
      .element
    )

    eta_8 = HomotopyElement(
      name="η₈",
      dimension=8,
      source=9,
      target=8,
      generator=GeneratorSymbol(
        family="η",
        index=8,
      ),
    )

    return Relation(
      lhs=Suspension(
        expression=nu4_eta7,
      ),
      rhs=Composition(
        left=nu_5,
        right=eta_8,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "E nu_4 eta_7 bridge"
    ),
    description=(
      "Use the independently derived "
      "pi_8^4 decomposition, "
      "the Proposition 5.1 eta-family, "
      "and the concrete nu_5 definition "
      "nu_5=E nu_4. "
      "Suspension functoriality gives "
      "E(nu_4 composed with eta_7) "
      "=nu_5 composed with eta_8. "
      "This is a concrete Proposition 5.8 "
      "bridge and does not introduce a "
      "generic suspension-composition "
      "normalizer."
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
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_pi9_5_finite_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi8_4_relation = (
      premises[
        0
      ].conclusion
    )

    delta_eta9 = (
      premises[
        1
      ].conclusion
    )

    prop51 = (
      premises[
        2
      ].conclusion
    )

    exactness = (
      premises[
        3
      ].conclusion
    )

    surjective = (
      premises[
        4
      ].conclusion
    )

    suspension_bridge = (
      premises[
        5
      ].conclusion
    )

    pi_8_4 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    )

    pi_9_5 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )

    pi_10_9 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=9,
    )

    if (
      pi8_4_relation.lhs
      != pi_8_4
    ):
      return False

    if not isinstance(
      pi8_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi8_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    first = (
      pi8_4_relation
      .rhs
      .summands[
        0
      ]
    )

    second = (
      pi8_4_relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      first,
      FiniteCyclicGroup,
    ):
      return False

    if not isinstance(
      second,
      FiniteCyclicGroup,
    ):
      return False

    if (
      first.order
      != 2
      or second.order
      != 2
    ):
      return False

    eta_9 = HomotopyElement(
      name="η₉",
      dimension=9,
      source=10,
      target=9,
      generator=GeneratorSymbol(
        family="η",
        index=9,
      ),
    )

    if (
      delta_eta9
      != Relation(
        lhs=MapApplication(
          map=EHP_DELTA_MAP,
          expression=eta_9,
        ),
        rhs=second.generator,
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    higher_relation = (
      prop51
      .higher_eta_group_relation
    )

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
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
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

    if (
      higher_relation
      .rhs
      .generator
      != eta_n
    ):
      return False

    window = exactness.window

    if (
      window
      != TodaEHPExactnessWindow(
        source_term=pi_10_9,
        middle_term=pi_8_4,
        target_term=pi_9_5,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      )
    ):
      return False

    if (
      surjective.map
      != TodaSuspensionMap(
        source_group=pi_8_4,
        target_group=pi_9_5,
      )
    ):
      return False

    return (
      suspension_bridge.lhs
      == Suspension(
        expression=first.generator,
      )
      and isinstance(
        suspension_bridge.rhs,
        Composition,
      )
    )

  def build_conclusion(
    premises,
  ):
    suspension_bridge = (
      premises[
        5
      ].conclusion
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=(
          suspension_bridge.rhs
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_9^5 finite cyclic"
    ),
    description=(
      "Phase 68-4 gives "
      "pi_8^4 as the direct sum of "
      "two order-two cyclic summands. "
      "Phase 68-5 gives "
      "Delta(eta_9)=E nu-prime eta_7, "
      "which is exactly the second "
      "summand generator. "
      "Proposition 5.1 gives the "
      "order-two source pi_10^9 "
      "generated by eta_9, so exactness "
      "identifies Ker(E) with precisely "
      "the second summand. "
      "The independently derived "
      "surjectivity of E then makes "
      "pi_9^5 the quotient by that "
      "summand. The remaining generator "
      "nu_4 eta_7 suspends to "
      "nu_5 eta_8. Therefore "
      "pi_9^5=Z/2 generated by "
      "nu_5 composed with eta_8. "
      "No generic quotient solver or "
      "direct-sum kernel solver is added."
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
          TodaProp51FiniteDimensionalStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionSurjectiveStatement
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


def toda_prop58_eta3_nu4_hopf_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    lemma54 = (
      premises[
        0
      ].conclusion
    )

    nu_4 = HomotopyElement(
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
      lemma54.nu4
      != nu_4
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

    expected_hopf_relation = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=nu_4,
      ),
      rhs=iota_7,
      relation_type=RelationType.EQUALITY,
    )

    return (
      lemma54.hopf_relation
      == expected_hopf_relation
    )

  def build_conclusion(
    premises,
  ):
    lemma54 = (
      premises[
        0
      ].conclusion
    )

    nu_4 = lemma54.nu4

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
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=Composition(
          left=eta_3,
          right=nu_4,
        ),
      ),
      rhs=Composition(
        left=eta_5,
        right=eta_6,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "Hopf value of eta_3 nu_4"
    ),
    description=(
      "Use the independently derived "
      "Toda Lemma 5.4 relation "
      "H(nu_4)=iota_7. "
      "For the concrete composition "
      "eta_3 composed with nu_4, "
      "the Toda Proposition 2.2 "
      "Hopf-composition consequence gives "
      "H(eta_3 composed with nu_4) "
      "=eta_5 composed with eta_6, "
      "which is eta_5 squared. "
      "This rule records only the concrete "
      "Toda (5.9) prerequisite and does "
      "not introduce a generic Hopf "
      "composition normalizer."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Statement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_59_eta3_nu4_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    isomorphism = (
      premises[
        0
      ].conclusion
    )

    eta3_nu4_hopf = (
      premises[
        1
      ].conclusion
    )

    equation57 = (
      premises[
        2
      ].conclusion
    )

    pi_7_3 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )

    pi_7_5 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=5,
    )

    if (
      isomorphism.map
      != TodaHopfInvariantMap(
        source_group=pi_7_3,
        target_group=pi_7_5,
      )
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

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
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

    eta5_squared = Composition(
      left=eta_5,
      right=eta_6,
    )

    expected_eta3_nu4_hopf = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=Composition(
          left=eta_3,
          right=nu_4,
        ),
      ),
      rhs=eta5_squared,
      relation_type=RelationType.EQUALITY,
    )

    if (
      eta3_nu4_hopf
      != expected_eta3_nu4_hopf
    ):
      return False

    expected_equation57 = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=Composition(
          left=nu_prime,
          right=eta_6,
        ),
      ),
      rhs=eta5_squared,
      relation_type=RelationType.EQUALITY,
    )

    return (
      equation57
      == expected_equation57
    )

  def build_conclusion(
    premises,
  ):
    eta3_nu4_hopf = (
      premises[
        1
      ].conclusion
    )

    equation57 = (
      premises[
        2
      ].conclusion
    )

    return Relation(
      lhs=(
        eta3_nu4_hopf
        .lhs
        .expression
      ),
      rhs=(
        equation57
        .lhs
        .expression
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Equation 5.9 "
      "eta_3 nu_4"
    ),
    description=(
      "Phase 68-3 gives the independently "
      "derived Hopf isomorphism "
      "H:pi_7^3 to pi_7^5. "
      "The concrete Hopf calculation gives "
      "H(eta_3 composed with nu_4) "
      "=eta_5 squared, while Toda (5.7) "
      "gives "
      "H(nu-prime composed with eta_6) "
      "=eta_5 squared. "
      "Injectivity of the same Hopf map "
      "therefore identifies the two "
      "elements and gives Toda (5.9): "
      "eta_3 composed with nu_4 "
      "=nu-prime composed with eta_6. "
      "No generic equality reflection "
      "through injective maps is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantIsomorphismStatement
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


def toda_510_eta5_nu6_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda59 = (
      premises[
        0
      ].conclusion
    )

    nu6_definition = (
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

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
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

    expected_toda59 = Relation(
      lhs=Composition(
        left=eta_3,
        right=nu_4,
      ),
      rhs=Composition(
        left=nu_prime,
        right=eta_6,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      toda59
      != expected_toda59
    ):
      return False

    return (
      nu6_definition
      == toda_nu_family_definition_statement(
        6
      )
    )

  def build_conclusion(
    premises,
  ):
    nu6_definition = (
      premises[
        1
      ].conclusion
    )

    nu_6 = (
      nu6_definition.element
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

    eta_8 = HomotopyElement(
      name="η₈",
      dimension=8,
      source=9,
      target=8,
      generator=GeneratorSymbol(
        family="η",
        index=8,
      ),
    )

    return Relation(
      lhs=Composition(
        left=eta_5,
        right=nu_6,
      ),
      rhs=Composition(
        left=IteratedSuspension(
          expression=nu_prime,
          exponent=2,
        ),
        right=eta_8,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "eta_5 nu_6 bridge"
    ),
    description=(
      "Suspend Toda (5.9) twice. "
      "The independently derived relation "
      "eta_3 composed with nu_4 "
      "=nu-prime composed with eta_6 "
      "therefore gives "
      "eta_5 composed with nu_6 "
      "=E^2 nu-prime composed with eta_8. "
      "The concrete nu_6 family definition "
      "anchors the shifted nu-family term. "
      "No generic iterated suspension "
      "of composition normalizer is added."
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
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_510_eta5_nu6_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    bridge = (
      premises[
        0
      ].conclusion
    )

    double_nu5 = (
      premises[
        1
      ].conclusion
    )

    pi9_5_relation = (
      premises[
        2
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

    nu_5 = (
      toda_nu_family_definition_statement(
        5
      ).element
    )

    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
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

    eta_8 = HomotopyElement(
      name="η₈",
      dimension=8,
      source=9,
      target=8,
      generator=GeneratorSymbol(
        family="η",
        index=8,
      ),
    )

    e2_nu_prime = IteratedSuspension(
      expression=nu_prime,
      exponent=2,
    )

    expected_bridge = Relation(
      lhs=Composition(
        left=eta_5,
        right=nu_6,
      ),
      rhs=Composition(
        left=e2_nu_prime,
        right=eta_8,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      bridge
      != expected_bridge
    ):
      return False

    expected_double_nu5 = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=nu_5,
      ),
      rhs=e2_nu_prime,
      relation_type=RelationType.EQUALITY,
    )

    if (
      double_nu5
      != expected_double_nu5
    ):
      return False

    nu5_eta8 = Composition(
      left=nu_5,
      right=eta_8,
    )

    expected_pi9_5 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=nu5_eta8,
      ),
      relation_type=RelationType.EQUALITY,
    )

    return (
      pi9_5_relation
      == expected_pi9_5
    )

  def build_conclusion(
    premises,
  ):
    bridge = (
      premises[
        0
      ].conclusion
    )

    return Relation(
      lhs=bridge.lhs,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "eta_5 nu_6 zero"
    ),
    description=(
      "The concrete bridge gives "
      "eta_5 nu_6=E^2 nu-prime eta_8. "
      "The independently derived "
      "Toda (5.5) specialization gives "
      "2 nu_5=E^2 nu-prime. "
      "Hence eta_5 nu_6 equals "
      "2 nu_5 eta_8. "
      "Phase 68-6 gives "
      "pi_9^5=Z/2 generated by "
      "nu_5 eta_8, so twice this "
      "generator is zero. "
      "Therefore eta_5 nu_6=0. "
      "No generic composition linearity "
      "or cyclic-group annihilator "
      "solver is introduced."
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
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_510_higher_eta_nu_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    base_zero = (
      premises[
        0
      ].conclusion
    )

    toda55 = (
      premises[
        1
      ].conclusion
    )

    eta_definition = (
      premises[
        2
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

    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
    )

    expected_base_zero = Relation(
      lhs=Composition(
        left=eta_5,
        right=nu_6,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      base_zero
      != expected_base_zero
    ):
      return False

    symbolic_nu_definition = (
      toda55
      .nu_family_definition
    )

    n = (
      symbolic_nu_definition.index
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      toda55.n_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    if (
      symbolic_nu_definition
      != toda_nu_family_definition_statement(
        n
      )
    ):
      return False

    return (
      eta_definition
      == toda_eta_family_definition_statement(
        n
      )
    )

  def build_conclusion(
    premises,
  ):
    toda55 = (
      premises[
        1
      ].conclusion
    )

    eta_definition = (
      premises[
        2
      ].conclusion
    )

    n = (
      toda55
      .nu_family_definition
      .index
    )

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    n_plus_four = ScalarSum(
      left=n,
      right=4,
    )

    nu_n_plus_one = HomotopyElement(
      name="ν_(n+1)",
      dimension=n_plus_one,
      source=n_plus_four,
      target=n_plus_one,
      generator=GeneratorSymbol(
        family="ν",
        index=n_plus_one,
      ),
    )

    return Relation(
      lhs=Composition(
        left=eta_definition.element,
        right=nu_n_plus_one,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "higher eta nu zero"
    ),
    description=(
      "Suspend the independently derived "
      "base relation eta_5 nu_6=0 "
      "through the finite-dimensional "
      "eta and nu families. "
      "For symbolic n at least 5, "
      "E^(n-5)(eta_5 nu_6) "
      "is eta_n composed with "
      "nu_(n+1), hence "
      "eta_n composed with nu_(n+1)=0. "
      "The shifted nu_(n+1) expression "
      "is constructed locally, following "
      "the existing shifted eta-family "
      "representation pattern. "
      "No generic shifted-family "
      "constructor or zero suspension "
      "transport framework is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda55NuFamilyFiniteDimensionalStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_eta6_nu7_zero_specialization_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    higher_zero = (
      premises[
        0
      ].conclusion
    )

    toda55 = (
      premises[
        1
      ].conclusion
    )

    eta6_definition = (
      premises[
        2
      ].conclusion
    )

    nu7_definition = (
      premises[
        3
      ].conclusion
    )

    symbolic_nu_definition = (
      toda55
      .nu_family_definition
    )

    n = (
      symbolic_nu_definition
      .index
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      toda55.n_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
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

    nu_n_plus_one = HomotopyElement(
      name="ν_(n+1)",
      dimension=n_plus_one,
      source=ScalarSum(
        left=n,
        right=4,
      ),
      target=n_plus_one,
      generator=GeneratorSymbol(
        family="ν",
        index=n_plus_one,
      ),
    )

    expected_higher_zero = Relation(
      lhs=Composition(
        left=eta_n,
        right=nu_n_plus_one,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      higher_zero
      != expected_higher_zero
    ):
      return False

    if (
      eta6_definition
      != toda_eta_family_definition_statement(
        6
      )
    ):
      return False

    return (
      nu7_definition
      == toda_nu_family_definition_statement(
        7
      )
    )

  def build_conclusion(
    premises,
  ):
    eta_6 = (
      premises[
        2
      ].conclusion
      .element
    )

    nu_7 = (
      premises[
        3
      ].conclusion
      .element
    )

    return Relation(
      lhs=Composition(
        left=eta_6,
        right=nu_7,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "eta_6 nu_7 zero specialization"
    ),
    description=(
      "Specialize the independently "
      "derived symbolic relation "
      "eta_n composed with nu_(n+1)=0 "
      "for n at least 5 at n=6. "
      "The canonical eta_6 and nu_7 "
      "family definitions anchor the "
      "concrete generators. "
      "The result is "
      "eta_6 composed with nu_7=0. "
      "No generic symbolic theorem "
      "specialization framework is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda55NuFamilyFiniteDimensionalStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop31_nu6_eta9_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    eta6_nu7_zero = (
      premises[
        0
      ].conclusion
    )

    first_formula = (
      premises[
        1
      ].conclusion
    )

    second_formula = (
      premises[
        2
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

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
      ),
    )

    eta_6 = (
      toda_eta_family_definition_statement(
        6
      ).element
    )

    nu_7 = (
      toda_nu_family_definition_statement(
        7
      ).element
    )

    expected_zero = Relation(
      lhs=Composition(
        left=eta_6,
        right=nu_7,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      eta6_nu7_zero
      != expected_zero
    ):
      return False

    smash = (
      first_formula.lhs
    )

    if (
      second_formula.lhs
      != smash
    ):
      return False

    expected_first_composition = Composition(
      left=IteratedSuspension(
        expression=eta_2,
        exponent=4,
      ),
      right=IteratedSuspension(
        expression=nu_4,
        exponent=3,
      ),
    )

    expected_second_composition = Composition(
      left=IteratedSuspension(
        expression=nu_4,
        exponent=2,
      ),
      right=IteratedSuspension(
        expression=eta_2,
        exponent=7,
      ),
    )

    if not isinstance(
      first_formula.rhs,
      Multiple,
    ):
      return False

    if not isinstance(
      second_formula.rhs,
      Multiple,
    ):
      return False

    first_sign = (
      first_formula
      .rhs
      .coefficient
    )

    second_sign = (
      second_formula
      .rhs
      .coefficient
    )

    if (
      first_sign
      != ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=3,
          right=3,
        ),
      )
    ):
      return False

    if (
      second_sign
      != ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=2,
          right=3,
        ),
      )
    ):
      return False

    if (
      first_formula
      .rhs
      .expression
      != expected_first_composition
    ):
      return False

    return (
      second_formula
      .rhs
      .expression
      == expected_second_composition
    )

  def build_conclusion(
    premises,
  ):
    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
    )

    eta_9 = (
      toda_eta_family_definition_statement(
        9
      ).element
    )

    return Relation(
      lhs=Composition(
        left=nu_6,
        right=eta_9,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 3.1 "
      "nu_6 eta_9 zero consequence"
    ),
    description=(
      "Use the two independently derived "
      "Toda Proposition 3.1 "
      "Barratt-Hilton formulas for "
      "eta_2 smash nu_4. "
      "The first identifies the smash "
      "product up to its explicit sign "
      "with E^4 eta_2 composed with "
      "E^3 nu_4, namely eta_6 nu_7. "
      "The second identifies the same "
      "smash product up to its explicit "
      "sign with E^2 nu_4 composed with "
      "E^7 eta_2, namely nu_6 eta_9. "
      "Since the independently derived "
      "eta_6 nu_7 is zero, the common "
      "smash-product expression is zero "
      "and therefore nu_6 eta_9 is zero. "
      "The sign does not need to be "
      "normalized because either sign "
      "of zero is zero. "
      "No generic smash-product "
      "normalization, sign solver, or "
      "zero substitution framework "
      "is introduced."
    ),
    premise_patterns=(
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


def toda_prop58_higher_nu_eta_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    base_zero = (
      premises[
        0
      ].conclusion
    )

    toda55 = (
      premises[
        1
      ].conclusion
    )

    n_range = (
      premises[
        2
      ].conclusion
    )

    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
    )

    eta_9 = (
      toda_eta_family_definition_statement(
        9
      ).element
    )

    expected_base_zero = Relation(
      lhs=Composition(
        left=nu_6,
        right=eta_9,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      base_zero
      != expected_base_zero
    ):
      return False

    symbolic_nu_definition = (
      toda55
      .nu_family_definition
    )

    n = (
      symbolic_nu_definition
      .index
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      symbolic_nu_definition
      != toda_nu_family_definition_statement(
        n
      )
    ):
      return False

    if (
      toda55.n_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    return (
      n_range
      == ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    )

  def build_conclusion(
    premises,
  ):
    toda55 = (
      premises[
        1
      ].conclusion
    )

    n = (
      toda55
      .nu_family_definition
      .index
    )

    nu_n = (
      toda55
      .nu_family_definition
      .element
    )

    n_plus_three = ScalarSum(
      left=n,
      right=3,
    )

    eta_n_plus_three = HomotopyElement(
      name="η_(n+3)",
      dimension=n_plus_three,
      source=ScalarSum(
        left=n,
        right=4,
      ),
      target=n_plus_three,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_three,
      ),
    )

    return Relation(
      lhs=Composition(
        left=nu_n,
        right=eta_n_plus_three,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "higher nu eta zero"
    ),
    description=(
      "Suspend the independently derived "
      "base relation nu_6 eta_9=0 "
      "through the finite-dimensional "
      "nu and eta families. "
      "For symbolic n at least 6, "
      "E^(n-6)(nu_6 eta_9) "
      "is nu_n composed with eta_(n+3). "
      "Therefore "
      "nu_n composed with eta_(n+3)=0. "
      "The shifted eta_(n+3) element "
      "is constructed locally because "
      "the canonical eta-family definition "
      "accepts only integer or simple "
      "ScalarSymbol indices. "
      "No generic shifted-family "
      "constructor, symbolic-index "
      "normalizer, or zero transport "
      "framework is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda55NuFamilyFiniteDimensionalStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_pi10_6_concrete_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    return (
      window
      == TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=5,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=6,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=11,
        ),
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_10^6 concrete exactness"
    ),
    description=(
      "Recognize the concrete E-H "
      "exactness window "
      "pi_9^5 -> pi_10^6 -> pi_10^11 "
      "used in the final part of "
      "Toda Proposition 5.8. "
      "The structural window remains "
      "a GIVEN premise while exactness "
      "is derived as theorem knowledge. "
      "No generic concrete dimension "
      "normalizer is introduced."
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


def toda_prop58_pi10_6_suspension_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    zero_target = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    pi_9_5 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )

    pi_10_6 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=6,
    )

    pi_10_11 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=11,
    )

    if (
      zero_target
      != TodaPrimaryGroupZeroStatement(
        group=pi_10_11,
      )
    ):
      return False

    return (
      exactness.window
      == TodaEHPExactnessWindow(
        source_term=pi_9_5,
        middle_term=pi_10_6,
        target_term=pi_10_11,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=5,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=6,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_10^6 suspension surjective"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_9^5 -> pi_10^6 -> pi_10^11, "
      "the final group pi_10^11 is zero. "
      "Hence the Hopf map is zero and "
      "exactness makes suspension "
      "E:pi_9^5 to pi_10^6 surjective. "
      "No generic zero-target "
      "surjectivity solver is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop58_pi10_6_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi9_5_relation = (
      premises[
        0
      ].conclusion
    )

    surjective = (
      premises[
        1
      ].conclusion
    )

    nu6_eta9_zero = (
      premises[
        2
      ].conclusion
    )

    pi_9_5 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )

    pi_10_6 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=6,
    )

    if (
      pi9_5_relation.lhs
      != pi_9_5
    ):
      return False

    if not isinstance(
      pi9_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi9_5_relation.rhs.order
      != 2
    ):
      return False

    source_generator = (
      pi9_5_relation
      .rhs
      .generator
    )

    if not isinstance(
      source_generator,
      Composition,
    ):
      return False

    nu_5 = (
      toda_nu_family_definition_statement(
        5
      ).element
    )

    if (
      source_generator.left
      != nu_5
    ):
      return False

    eta_8 = (
      source_generator.right
    )

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    if (
      eta_8.dimension
      != 8
    ):
      return False

    if (
      eta_8.source
      != 9
    ):
      return False

    if (
      eta_8.target
      != 8
    ):
      return False

    if (
      eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    if (
      surjective.map
      != TodaSuspensionMap(
        source_group=pi_9_5,
        target_group=pi_10_6,
      )
    ):
      return False

    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
    )

    eta_9 = (
      toda_eta_family_definition_statement(
        9
      ).element
    )

    return (
      nu6_eta9_zero
      == Relation(
        lhs=Composition(
          left=nu_6,
          right=eta_9,
        ),
        rhs=Zero(),
        relation_type=RelationType.ZERO,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=6,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "pi_10^6 zero"
    ),
    description=(
      "Phase 68-6 gives "
      "pi_9^5=Z/2 generated by "
      "nu_5 composed with eta_8. "
      "The concrete EHP sequence gives "
      "surjectivity of suspension "
      "E:pi_9^5 to pi_10^6. "
      "Thus pi_10^6 is generated by "
      "the suspension of nu_5 eta_8, "
      "namely nu_6 eta_9. "
      "Phase 68-9 independently derives "
      "nu_6 eta_9=0. "
      "Therefore pi_10^6 is zero. "
      "The eta_8 factor is validated "
      "structurally from the derived "
      "Phase 68-6 generator rather than "
      "being reconstructed through the "
      "canonical eta-family helper, "
      "because the existing concrete "
      "representations use different "
      "display names for that same "
      "family member. "
      "No generic cyclic-image or "
      "zero-generator group solver "
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
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionSurjectiveStatement
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


def toda_prop58_higher_four_stem_zero_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_zero = (
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

    pi_10_6 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=6,
    )

    if (
      source_zero
      != TodaPrimaryGroupZeroStatement(
        group=pi_10_6,
      )
    ):
      return False

    suspension_map = (
      isomorphism.map
    )

    structural_source = TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=6,
        right=4,
      ),
      sphere_dimension=6,
    )

    if (
      suspension_map.source_group
      != structural_source
    ):
      return False

    target_group = (
      suspension_map.target_group
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

    if (
      target_group
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=4,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    if (
      suspension_map.exponent
      != ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=6,
        ),
      )
    ):
      return False

    return (
      higher_range
      == ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    )

  def build_conclusion(
    premises,
  ):
    target_group = (
      premises[
        1
      ].conclusion
      .map
      .target_group
    )

    return TodaPrimaryGroupZeroStatement(
      group=target_group,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "higher four-stem zero transport"
    ),
    description=(
      "Transport the independently "
      "derived zero group pi_10^6 "
      "through the independently derived "
      "Toda (4.5) stable-range "
      "iterated-suspension isomorphism "
      "E^(n-6):pi_10^6 to pi_(n+4)^n. "
      "For n at least 6 this gives "
      "pi_(n+4)^n=0. "
      "No generic isomorphism transport "
      "of zero groups is introduced."
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
          Toda45IsomorphismStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


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


@dataclass(frozen=True)
class TodaProp56FiniteDimensionalStatement:
  pi5_2_group_relation: Relation
  pi6_3_group_relation: Relation
  pi7_4_group_relation: Relation
  pi8_5_group_relation: Relation
  higher_nu_group_relation: Relation
  higher_range: ScalarGreaterEqualStatement
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


@dataclass(frozen=True)
class TodaProp58FiniteDimensionalStatement:
  pi6_2_group_relation: Relation
  pi7_3_group_relation: Relation
  pi8_4_group_relation: Relation
  pi9_5_group_relation: Relation
  higher_four_stem_zero: TodaPrimaryGroupZeroStatement
  higher_range: ScalarGreaterEqualStatement
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


@dataclass(frozen=True)
class TodaProp59FiniteDimensionalStatement:
  pi7_2_group_relation: Relation
  pi8_3_group_relation: Relation
  pi9_4_group_relation: Relation
  pi10_5_group_relation: Relation
  pi11_6_group_relation: Relation
  higher_five_stem_zero: TodaPrimaryGroupZeroStatement
  higher_range: ScalarGreaterEqualStatement
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


@dataclass(frozen=True)
class Toda512DeltaInjectivityStatement:
  n4_injectivity: TodaDeltaInjectiveStatement
  n5_injectivity: TodaDeltaInjectiveStatement
  n6_injectivity: TodaDeltaInjectiveStatement
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


def toda_512_delta_injectivity_literature_statements():
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
        label="Toda (5.12)",
        locator="Equation (5.12)",
        **toda_reference,
      ),
      statement=(
        "The Delta map "
        "from pi_(n+7)^(2n+1) "
        "to pi_(n+5)^n "
        "is injective for "
        "n=4, 5, 6."
      ),
    ),
  )


def toda_prop59_finite_dimensional_literature_statements():
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
        label="Toda Proposition 5.9",
        locator="Proposition 5.9",
        **toda_reference,
      ),
      statement=(
        "Finite-dimensional part: "
        "pi_7^2 is cyclic of order 2 "
        "generated by eta_2 composed "
        "with nu-prime composed with eta_6; "
        "pi_8^3 is cyclic of order 2 "
        "generated by nu-prime composed "
        "with eta_6 squared; "
        "pi_9^4 is the direct sum of "
        "Z/2 generated by nu_4 composed "
        "with eta_7 squared and Z/2 "
        "generated by E nu-prime composed "
        "with eta_7 squared; "
        "pi_10^5 is cyclic of order 2 "
        "generated by nu_5 composed "
        "with eta_8 squared; "
        "pi_11^6 is infinite cyclic "
        "generated by Delta(iota_13); "
        "and pi_(n+5)^n is zero "
        "for n at least 7."
      ),
    ),
  )


def toda_prop58_finite_dimensional_literature_statements():
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
        label="Toda Proposition 5.8",
        locator="Proposition 5.8",
        **toda_reference,
      ),
      statement=(
        "Finite-dimensional part: "
        "pi_6^2 is cyclic of order 4 "
        "generated by eta_2 composed "
        "with nu-prime; "
        "pi_7^3 is cyclic of order 2 "
        "generated by nu-prime composed "
        "with eta_6; "
        "pi_8^4 is the direct sum of "
        "Z/2 generated by nu_4 composed "
        "with eta_7 and Z/2 generated "
        "by E nu-prime composed with eta_7; "
        "pi_9^5 is cyclic of order 2 "
        "generated by nu_5 composed "
        "with eta_8; "
        "and pi_(n+4)^n is zero "
        "for n at least 6."
      ),
    ),
  )


def toda_prop58_finite_dimensional_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi6_2_relation = (
      premises[
        0
      ].conclusion
    )

    pi7_3_relation = (
      premises[
        1
      ].conclusion
    )

    pi8_4_relation = (
      premises[
        2
      ].conclusion
    )

    pi9_5_relation = (
      premises[
        3
      ].conclusion
    )

    higher_zero = (
      premises[
        4
      ].conclusion
    )

    higher_range = (
      premises[
        5
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

    expected_pi6_2 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=Composition(
          left=eta_2,
          right=nu_prime,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi6_2_relation
      != expected_pi6_2
    ):
      return False

    if (
      pi7_3_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=3,
      )
    ):
      return False

    if not isinstance(
      pi7_3_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi7_3_relation.rhs.order
      != 2
    ):
      return False

    pi7_3_generator = (
      pi7_3_relation
      .rhs
      .generator
    )

    if not isinstance(
      pi7_3_generator,
      Composition,
    ):
      return False

    if (
      pi7_3_generator.left
      != nu_prime
    ):
      return False

    eta_6 = (
      pi7_3_generator.right
    )

    if not isinstance(
      eta_6,
      HomotopyElement,
    ):
      return False

    if (
      eta_6.dimension
      != 6
      or eta_6.source
      != 7
      or eta_6.target
      != 6
      or eta_6.generator
      != GeneratorSymbol(
        family="η",
        index=6,
      )
    ):
      return False

    if (
      pi8_4_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=4,
      )
    ):
      return False

    if not isinstance(
      pi8_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi8_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    first_summand = (
      pi8_4_relation
      .rhs
      .summands[
        0
      ]
    )

    second_summand = (
      pi8_4_relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      first_summand,
      FiniteCyclicGroup,
    ):
      return False

    if not isinstance(
      second_summand,
      FiniteCyclicGroup,
    ):
      return False

    if (
      first_summand.order
      != 2
      or second_summand.order
      != 2
    ):
      return False

    first_generator = (
      first_summand.generator
    )

    second_generator = (
      second_summand.generator
    )

    if not isinstance(
      first_generator,
      Composition,
    ):
      return False

    if not isinstance(
      second_generator,
      Composition,
    ):
      return False

    nu_4 = HomotopyElement(
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
      first_generator.left
      != nu_4
    ):
      return False

    eta_7 = (
      first_generator.right
    )

    if not isinstance(
      eta_7,
      HomotopyElement,
    ):
      return False

    if (
      eta_7.dimension
      != 7
      or eta_7.source
      != 8
      or eta_7.target
      != 7
      or eta_7.generator
      != GeneratorSymbol(
        family="η",
        index=7,
      )
    ):
      return False

    if (
      second_generator.right
      != eta_7
    ):
      return False

    if (
      second_generator.left
      != Suspension(
        expression=nu_prime,
      )
    ):
      return False

    if (
      pi9_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi9_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi9_5_relation.rhs.order
      != 2
    ):
      return False

    pi9_5_generator = (
      pi9_5_relation
      .rhs
      .generator
    )

    if not isinstance(
      pi9_5_generator,
      Composition,
    ):
      return False

    nu_5 = (
      toda_nu_family_definition_statement(
        5
      ).element
    )

    if (
      pi9_5_generator.left
      != nu_5
    ):
      return False

    eta_8 = (
      pi9_5_generator.right
    )

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    if (
      eta_8.dimension
      != 8
      or eta_8.source
      != 9
      or eta_8.target
      != 8
      or eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    if not isinstance(
      higher_zero,
      TodaPrimaryGroupZeroStatement,
    ):
      return False

    higher_group = (
      higher_zero.group
    )

    if not isinstance(
      higher_group,
      TodaPrimaryGroup,
    ):
      return False

    n = (
      higher_group
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      higher_group
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=4,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    return (
      higher_range
      == ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    )

  def build_conclusion(
    premises,
  ):
    return (
      TodaProp58FiniteDimensionalStatement(
        pi6_2_group_relation=(
          premises[
            0
          ].conclusion
        ),
        pi7_3_group_relation=(
          premises[
            1
          ].conclusion
        ),
        pi8_4_group_relation=(
          premises[
            2
          ].conclusion
        ),
        pi9_5_group_relation=(
          premises[
            3
          ].conclusion
        ),
        higher_four_stem_zero=(
          premises[
            4
          ].conclusion
        ),
        higher_range=(
          premises[
            5
          ].conclusion
        ),
        literature_statements=(
          toda_prop58_finite_dimensional_literature_statements()
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.8 "
      "finite-dimensional integration"
    ),
    description=(
      "Integrate the five independently "
      "derived finite-dimensional "
      "conclusions of Toda Proposition 5.8: "
      "pi_6^2=Z/4{eta_2 nu-prime}, "
      "pi_7^3=Z/2{nu-prime eta_6}, "
      "pi_8^4=Z/2{nu_4 eta_7} direct sum "
      "Z/2{E nu-prime eta_7}, "
      "pi_9^5=Z/2{nu_5 eta_8}, "
      "and pi_(n+4)^n=0 for n at least 6. "
      "All mathematical group conclusions "
      "must already be derived. "
      "The applicability range n>=6 "
      "remains an explicit GIVEN premise. "
      "The aggregate introduces no new "
      "group calculation or stable "
      "homotopy conclusion."
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
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_eq510_concrete_delta_e_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    return (
      window
      == TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=11,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=5,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=6,
        ),
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Equation (5.10) "
      "concrete Delta-E exactness"
    ),
    description=(
      "Recognize the concrete Toda "
      "Proposition 4.2 Delta-E exactness "
      "window pi_11^11 -> pi_9^5 -> "
      "pi_10^6 used immediately before "
      "Toda Equation (5.10). "
      "The structural window remains a "
      "GIVEN premise while exactness is "
      "derived as theorem knowledge. "
      "No generic concrete-dimension "
      "normalizer is introduced."
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


def toda_eq510_delta_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    zero_target = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    pi_11_11 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=11,
    )

    pi_9_5 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )

    pi_10_6 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=6,
    )

    if (
      zero_target
      != TodaPrimaryGroupZeroStatement(
        group=pi_10_6,
      )
    ):
      return False

    return (
      exactness.window
      == TodaEHPExactnessWindow(
        source_term=pi_11_11,
        middle_term=pi_9_5,
        target_term=pi_10_6,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[
        1
      ].conclusion.window
    )

    return TodaDeltaSurjectiveStatement(
      map=TodaDeltaMap(
        source_group=(
          window.source_term
        ),
        target_group=(
          window.middle_term
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Equation (5.10) "
      "Delta surjective prerequisite"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_11^11 -> pi_9^5 -> pi_10^6, "
      "Phase 68 has already derived "
      "pi_10^6=0. Therefore suspension "
      "E:pi_9^5 to pi_10^6 is the zero "
      "map, so exactness gives "
      "Im(Delta)=pi_9^5 and hence "
      "Delta:pi_11^11 to pi_9^5 is "
      "surjective. No generic exactness "
      "or zero-target solver is added."
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
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_eq510_delta_iota11_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_surjective = (
      premises[
        0
      ].conclusion
    )

    pi11_11_relation = (
      premises[
        1
      ].conclusion
    )

    pi9_5_relation = (
      premises[
        2
      ].conclusion
    )

    pi11_11 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=11,
    )

    pi9_5 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )

    if (
      delta_surjective.map
      != TodaDeltaMap(
        source_group=pi11_11,
        target_group=pi9_5,
      )
    ):
      return False

    if (
      pi11_11_relation.lhs
      != pi11_11
    ):
      return False

    if not isinstance(
      pi11_11_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    iota_11 = (
      pi11_11_relation
      .rhs
      .generator
    )

    if not isinstance(
      iota_11,
      HomotopyElement,
    ):
      return False

    if (
      iota_11.dimension
      != 11
    ):
      return False

    if (
      iota_11.generator
      != GeneratorSymbol(
        family="ι",
        index=11,
      )
    ):
      return False

    if (
      pi9_5_relation.lhs
      != pi9_5
    ):
      return False

    if not isinstance(
      pi9_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi9_5_relation.rhs.order
      != 2
    ):
      return False

    target_generator = (
      pi9_5_relation
      .rhs
      .generator
    )

    if not isinstance(
      target_generator,
      Composition,
    ):
      return False

    nu_5 = (
      toda_nu_family_definition_statement(
        5
      ).element
    )

    if (
      target_generator.left
      != nu_5
    ):
      return False

    eta_8 = (
      target_generator.right
    )

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    if (
      eta_8.dimension
      != 8
    ):
      return False

    if (
      eta_8.source
      != 9
    ):
      return False

    if (
      eta_8.target
      != 8
    ):
      return False

    return (
      eta_8.generator
      == GeneratorSymbol(
        family="η",
        index=8,
      )
    )

  def build_conclusion(
    premises,
  ):
    pi11_11_relation = (
      premises[
        1
      ].conclusion
    )

    pi9_5_relation = (
      premises[
        2
      ].conclusion
    )

    iota_11 = (
      pi11_11_relation
      .rhs
      .generator
    )

    nu5_eta8 = (
      pi9_5_relation
      .rhs
      .generator
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=iota_11,
      ),
      rhs=nu5_eta8,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Equation (5.10) "
      "Delta iota_11"
    ),
    description=(
      "For the derived surjective Delta "
      "from pi_11^11 to pi_9^5, "
      "use the foundational source "
      "pi_11^11=Z generated by iota_11 "
      "and the independently derived "
      "Phase 68 result "
      "pi_9^5=Z/2 generated by "
      "nu_5 composed with eta_8. "
      "Surjectivity forces the image "
      "of the source generator to be "
      "the unique nonzero element of "
      "the order-two target. Therefore "
      "Delta(iota_11)=nu_5 eta_8. "
      "The target has order two, so the "
      "possible sign is immaterial. "
      "No generic cyclic-image solver "
      "or generic sign algebra is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaSurjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
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


def toda_prop59_pi7_2_eta2_nu_prime_eta6_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi7_3_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    expected_pi7_3 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )

    if (
      pi7_3_relation.lhs
      != expected_pi7_3
    ):
      return False

    if not isinstance(
      pi7_3_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi7_3_relation.rhs.order
      != 2
    ):
      return False

    nu_prime_eta6 = (
      pi7_3_relation
      .rhs
      .generator
    )

    if not isinstance(
      nu_prime_eta6,
      Composition,
    ):
      return False

    nu_prime = (
      nu_prime_eta6.left
    )

    eta_6 = (
      nu_prime_eta6.right
    )

    if not isinstance(
      nu_prime,
      HomotopyElement,
    ):
      return False

    if (
      nu_prime.dimension
      != 3
    ):
      return False

    if (
      nu_prime.source
      != 6
    ):
      return False

    if (
      nu_prime.target
      != 3
    ):
      return False

    if (
      nu_prime.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    if not isinstance(
      eta_6,
      HomotopyElement,
    ):
      return False

    if (
      eta_6.dimension
      != 6
    ):
      return False

    if (
      eta_6.source
      != 7
    ):
      return False

    if (
      eta_6.target
      != 6
    ):
      return False

    if (
      eta_6.generator
      != GeneratorSymbol(
        family="η",
        index=6,
      )
    ):
      return False

    source_group = (
      isomorphism
      .source_group
    )

    target_group = (
      isomorphism
      .target_group
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
      isomorphism
      .composition
    )

    if not isinstance(
      composition,
      Composition,
    ):
      return False

    eta_2 = (
      composition.left
    )

    if not isinstance(
      eta_2,
      HomotopyElement,
    ):
      return False

    if (
      eta_2.dimension
      != 2
    ):
      return False

    if (
      eta_2.source
      != 3
    ):
      return False

    if (
      eta_2.target
      != 2
    ):
      return False

    if (
      eta_2.generator
      != GeneratorSymbol(
        family="η",
        index=2,
      )
    ):
      return False

    gamma = (
      composition.right
    )

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

    return (
      gamma.target
      == 3
    )

  def build_conclusion(
    premises,
  ):
    pi7_3_relation = (
      premises[
        0
      ].conclusion
    )

    isomorphism = (
      premises[
        1
      ].conclusion
    )

    nu_prime_eta6 = (
      pi7_3_relation
      .rhs
      .generator
    )

    eta_2 = (
      isomorphism
      .composition
      .left
    )

    eta2_nu_prime_eta6 = (
      Composition(
        left=eta_2,
        right=nu_prime_eta6,
      )
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta2_nu_prime_eta6,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_7^2 eta_2 nu-prime eta_6"
    ),
    description=(
      "Use the independently derived "
      "Toda Proposition 5.8 relation "
      "pi_7^3=Z/2 generated by "
      "nu-prime composed with eta_6 "
      "together with the independently "
      "derived Toda (5.2) composition "
      "isomorphism "
      "eta_2 composed with minus from "
      "pi_i^3 to pi_i^2. "
      "Transport the concrete order-two "
      "generator nu-prime composed with "
      "eta_6 to eta_2 composed with "
      "nu-prime composed with eta_6 and "
      "derive pi_7^2=Z/2 generated by "
      "eta_2 composed with "
      "nu-prime composed with eta_6. "
      "No generic cyclic-generator "
      "transport framework is added."
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


@dataclass(frozen=True)
class TodaProp59DeltaKernelStatement:
  map: TodaDeltaMap
  kernel_group: FiniteCyclicGroup


def toda_prop59_pi7_2_suspension_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi7_2_relation = (
      premises[
        0
      ].conclusion
    )

    eta2_nu_prime_zero = (
      premises[
        1
      ].conclusion
    )

    if (
      pi7_2_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=2,
      )
    ):
      return False

    if not isinstance(
      pi7_2_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi7_2_relation.rhs.order
      != 2
    ):
      return False

    generator = (
      pi7_2_relation
      .rhs
      .generator
    )

    if not isinstance(
      generator,
      Composition,
    ):
      return False

    eta_2 = (
      generator.left
    )

    nu_prime_eta6 = (
      generator.right
    )

    if not isinstance(
      eta_2,
      HomotopyElement,
    ):
      return False

    if (
      eta_2.dimension
      != 2
    ):
      return False

    if (
      eta_2.source
      != 3
    ):
      return False

    if (
      eta_2.target
      != 2
    ):
      return False

    if (
      eta_2.generator
      != GeneratorSymbol(
        family="η",
        index=2,
      )
    ):
      return False

    if not isinstance(
      nu_prime_eta6,
      Composition,
    ):
      return False

    nu_prime = (
      nu_prime_eta6.left
    )

    eta_6 = (
      nu_prime_eta6.right
    )

    if not isinstance(
      nu_prime,
      HomotopyElement,
    ):
      return False

    if (
      nu_prime.dimension
      != 3
    ):
      return False

    if (
      nu_prime.source
      != 6
    ):
      return False

    if (
      nu_prime.target
      != 3
    ):
      return False

    if (
      nu_prime.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    if not isinstance(
      eta_6,
      HomotopyElement,
    ):
      return False

    if (
      eta_6.dimension
      != 6
    ):
      return False

    if (
      eta_6.source
      != 7
    ):
      return False

    if (
      eta_6.target
      != 6
    ):
      return False

    if (
      eta_6.generator
      != GeneratorSymbol(
        family="η",
        index=6,
      )
    ):
      return False

    expected_eta2_nu_prime_zero = Relation(
      lhs=Suspension(
        expression=Composition(
          left=eta_2,
          right=nu_prime,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      eta2_nu_prime_zero
      == expected_eta2_nu_prime_zero
    )

  def build_conclusion(
    premises,
  ):
    pi7_2_relation = (
      premises[
        0
      ].conclusion
    )

    return Relation(
      lhs=Suspension(
        expression=(
          pi7_2_relation
          .rhs
          .generator
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_7^2 suspension zero"
    ),
    description=(
      "Use the independently derived "
      "pi_7^2=Z/2 generated by "
      "eta_2 composed with "
      "nu-prime composed with eta_6 "
      "together with the Phase 67 "
      "relation "
      "E(eta_2 composed with nu-prime)=0. "
      "For this concrete composition, "
      "suspension of the generator "
      "eta_2 nu-prime eta_6 is zero. "
      "No generic suspension-composition "
      "normalizer or zero-map solver "
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


def toda_prop59_concrete_e_h_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
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

    return (
      window.source_term
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=2,
      )
      and window.middle_term
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=3,
      )
      and window.target_term
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "concrete E-H exactness"
    ),
    description=(
      "Recognize the concrete Toda "
      "Proposition 4.2 exact sequence "
      "segment "
      "pi_7^2 -> pi_8^3 -> pi_8^5 "
      "with suspension E followed by "
      "the Hopf invariant H. "
      "No generic symbolic index "
      "normalization is added."
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


def toda_prop59_pi8_3_hopf_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    suspension_zero = (
      premises[
        0
      ].conclusion
    )

    pi7_2_relation = (
      premises[
        1
      ].conclusion
    )

    exactness = (
      premises[
        2
      ].conclusion
    )

    if (
      pi7_2_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=2,
      )
    ):
      return False

    if not isinstance(
      pi7_2_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi7_2_relation.rhs.order
      != 2
    ):
      return False

    expected_zero = Relation(
      lhs=Suspension(
        expression=(
          pi7_2_relation
          .rhs
          .generator
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      suspension_zero
      != expected_zero
    ):
      return False

    window = (
      exactness.window
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

    return (
      window.source_term
      == TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=2,
      )
      and window.middle_term
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=3,
      )
      and window.target_term
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        2
      ].conclusion
    )

    window = exactness.window

    return TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_8^3 Hopf injective"
    ),
    description=(
      "The Phase 70-2 group pi_7^2 "
      "is cyclic and its generator "
      "suspends to zero. "
      "Therefore E is zero on pi_7^2. "
      "Exactness of "
      "pi_7^2 -> pi_8^3 -> pi_8^5 "
      "gives Ker(H)=Im(E)=0, "
      "so H:pi_8^3 to pi_8^5 "
      "is injective. "
      "No generic zero-map solver "
      "is introduced."
    ),
    premise_patterns=(
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
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_concrete_h_delta_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
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

    return (
      window.source_term
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=3,
      )
      and window.middle_term
      == TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
      and window.target_term
      == TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "concrete H-Delta exactness"
    ),
    description=(
      "Recognize the concrete Toda "
      "Proposition 4.2 exact sequence "
      "segment "
      "pi_8^3 -> pi_8^5 -> pi_6^2 "
      "with the Hopf invariant H "
      "followed by Delta. "
      "No generic symbolic index "
      "normalization is added."
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


def toda_prop59_delta_nu5_kernel_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_relation = (
      premises[
        0
      ].conclusion
    )

    pi8_5_relation = (
      premises[
        1
      ].conclusion
    )

    pi6_2_relation = (
      premises[
        2
      ].conclusion
    )

    expected_delta_map = TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      ),
    )

    if (
      delta_relation.map
      != expected_delta_map
    ):
      return False

    if (
      pi8_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi8_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi8_5_relation.rhs.order
      != 8
    ):
      return False

    nu_5 = (
      pi8_5_relation
      .rhs
      .generator
    )

    if (
      nu_5
      != toda_nu_family_definition_statement(
        5
      ).element
    ):
      return False

    if (
      delta_relation.element
      != nu_5
    ):
      return False

    if (
      pi6_2_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=2,
      )
    ):
      return False

    if not isinstance(
      pi6_2_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi6_2_relation.rhs.order
      != 4
    ):
      return False

    return (
      delta_relation.positive_value
      == (
        pi6_2_relation
        .rhs
        .generator
      )
    )

  def build_conclusion(
    premises,
  ):
    delta_relation = (
      premises[
        0
      ].conclusion
    )

    pi8_5_relation = (
      premises[
        1
      ].conclusion
    )

    nu_5 = (
      pi8_5_relation
      .rhs
      .generator
    )

    return TodaProp59DeltaKernelStatement(
      map=delta_relation.map,
      kernel_group=FiniteCyclicGroup(
        order=2,
        generator=Multiple(
          coefficient=4,
          expression=nu_5,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "Delta nu_5 kernel"
    ),
    description=(
      "Use "
      "pi_8^5=Z/8{nu_5}, "
      "pi_6^2=Z/4{eta_2 nu-prime}, "
      "and "
      "Delta(nu_5)=plus or minus "
      "eta_2 nu-prime. "
      "For this concrete cyclic map, "
      "the Delta kernel is the "
      "order-two subgroup generated "
      "by 4 nu_5. "
      "No generic finite-cyclic "
      "kernel solver is introduced."
    ),
    premise_patterns=(
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


def toda_prop59_nu_prime_eta6_squared_hopf_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    equation57 = (
      premises[
        0
      ].conclusion
    )

    toda55_statement = (
      premises[
        1
      ].conclusion
    )

    pi8_5_relation = (
      premises[
        2
      ].conclusion
    )

    eta7_definition = (
      premises[
        3
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

    expected_equation57 = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=Composition(
          left=nu_prime,
          right=eta_6,
        ),
      ),
      rhs=Composition(
        left=eta_5,
        right=eta_6,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      equation57
      != expected_equation57
    ):
      return False

    definition = (
      toda55_statement
      .nu_family_definition
    )

    n = definition.index

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      toda55_statement.n_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    if (
      definition
      != toda_nu_family_definition_statement(
        n
      )
    ):
      return False

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    n_plus_two = ScalarSum(
      left=n,
      right=2,
    )

    n_plus_three = ScalarSum(
      left=n,
      right=3,
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
      source=n_plus_three,
      target=n_plus_two,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_two,
      ),
    )

    expected_quadruple_relation = Relation(
      lhs=Multiple(
        coefficient=4,
        expression=definition.element,
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

    if (
      toda55_statement
      .quadruple_nu_relation
      != expected_quadruple_relation
    ):
      return False

    if (
      pi8_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi8_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi8_5_relation.rhs.order
      != 8
    ):
      return False

    if (
      pi8_5_relation
      .rhs
      .generator
      != toda_nu_family_definition_statement(
        5
      ).element
    ):
      return False

    if (
      eta7_definition.index
      != 7
    ):
      return False

    eta7_element = (
      eta7_definition.element
    )

    if not isinstance(
      eta7_element,
      HomotopyElement,
    ):
      return False

    if (
      eta7_element.dimension
      != 7
    ):
      return False

    if (
      eta7_element.source
      != 8
    ):
      return False

    if (
      eta7_element.target
      != 7
    ):
      return False

    return (
      eta7_element.generator
      == GeneratorSymbol(
        family="η",
        index=7,
      )
    )

  def build_conclusion(
    premises,
  ):
    equation57 = (
      premises[
        0
      ].conclusion
    )

    pi8_5_relation = (
      premises[
        2
      ].conclusion
    )

    nu_prime_eta6 = (
      equation57
      .lhs
      .expression
    )

    nu_prime = (
      nu_prime_eta6.left
    )

    eta_6 = (
      nu_prime_eta6.right
    )

    eta_7 = HomotopyElement(
      name="η₇",
      dimension=7,
      source=8,
      target=7,
      generator=GeneratorSymbol(
        family="η",
        index=7,
      ),
    )

    nu_prime_eta6_squared = (
      Composition(
        left=nu_prime,
        right=Composition(
          left=eta_6,
          right=eta_7,
        ),
      )
    )

    nu_5 = (
      pi8_5_relation
      .rhs
      .generator
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=nu_prime_eta6_squared,
      ),
      rhs=Multiple(
        coefficient=4,
        expression=nu_5,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "nu-prime eta_6 squared Hopf value"
    ),
    description=(
      "Use the independently derived "
      "Toda Equation (5.7) relation "
      "H(nu-prime eta_6)=eta_5 squared, "
      "the finite-dimensional Toda (5.5) "
      "relation "
      "4 nu_n=eta_n eta_(n+1) eta_(n+2), "
      "and the concrete canonical "
      "nu_5 generator of pi_8^5. "
      "Specializing n=5 and applying "
      "the concrete Proposition 2.2 "
      "composition consequence gives "
      "H(nu-prime eta_6 squared)=4 nu_5. "
      "No generic Hopf-composition "
      "normalizer or theorem "
      "specialization engine is added."
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
          Toda55NuFamilyFiniteDimensionalStatement
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
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi8_3_finite_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_injective = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    delta_kernel = (
      premises[
        2
      ].conclusion
    )

    hopf_relation = (
      premises[
        3
      ].conclusion
    )

    pi8_3 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=3,
    )

    pi8_5 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )

    pi6_2 = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=2,
    )

    expected_hopf_map = (
      TodaHopfInvariantMap(
        source_group=pi8_3,
        target_group=pi8_5,
      )
    )

    if (
      hopf_injective.map
      != expected_hopf_map
    ):
      return False

    window = exactness.window

    if (
      window.source_term
      != pi8_3
    ):
      return False

    if (
      window.middle_term
      != pi8_5
    ):
      return False

    if (
      window.target_term
      != pi6_2
    ):
      return False

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

    expected_delta_map = TodaDeltaMap(
      source_group=pi8_5,
      target_group=pi6_2,
    )

    if (
      delta_kernel.map
      != expected_delta_map
    ):
      return False

    if (
      delta_kernel.kernel_group.order
      != 2
    ):
      return False

    if (
      hopf_relation.lhs.map
      != EHP_H_MAP
    ):
      return False

    if (
      hopf_relation.rhs
      != (
        delta_kernel
        .kernel_group
        .generator
      )
    ):
      return False

    candidate = (
      hopf_relation
      .lhs
      .expression
    )

    if not isinstance(
      candidate,
      Composition,
    ):
      return False

    nu_prime = (
      candidate.left
    )

    eta6_squared = (
      candidate.right
    )

    if not isinstance(
      nu_prime,
      HomotopyElement,
    ):
      return False

    if (
      nu_prime.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    if not isinstance(
      eta6_squared,
      Composition,
    ):
      return False

    eta_6 = (
      eta6_squared.left
    )

    eta_7 = (
      eta6_squared.right
    )

    if (
      eta_6.generator
      != GeneratorSymbol(
        family="η",
        index=6,
      )
    ):
      return False

    return (
      eta_7.generator
      == GeneratorSymbol(
        family="η",
        index=7,
      )
    )

  def build_conclusion(
    premises,
  ):
    hopf_relation = (
      premises[
        3
      ].conclusion
    )

    candidate = (
      hopf_relation
      .lhs
      .expression
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=candidate,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_8^3 finite cyclic"
    ),
    description=(
      "The Hopf invariant "
      "H:pi_8^3 to pi_8^5 is injective. "
      "Exactness gives "
      "Im(H)=Ker(Delta). "
      "The concrete Delta kernel is "
      "Z/2 generated by 4 nu_5, and "
      "H(nu-prime eta_6 squared)=4 nu_5. "
      "Therefore "
      "pi_8^3=Z/2 generated by "
      "nu-prime eta_6 squared. "
      "No generic first-isomorphism "
      "or cyclic-kernel solver is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp59DeltaKernelStatement
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


def toda_prop59_e_nu_prime_eta6_squared_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi8_3_relation = (
      premises[
        0
      ].conclusion
    )

    prop53 = (
      premises[
        1
      ].conclusion
    )

    if (
      pi8_3_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=3,
      )
    ):
      return False

    if not isinstance(
      pi8_3_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi8_3_relation.rhs.order
      != 2
    ):
      return False

    generator = (
      pi8_3_relation
      .rhs
      .generator
    )

    if not isinstance(
      generator,
      Composition,
    ):
      return False

    nu_prime = (
      generator.left
    )

    eta6_squared = (
      generator.right
    )

    if not isinstance(
      nu_prime,
      HomotopyElement,
    ):
      return False

    if (
      nu_prime.dimension
      != 3
      or nu_prime.source
      != 6
      or nu_prime.target
      != 3
      or nu_prime.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    if not isinstance(
      eta6_squared,
      Composition,
    ):
      return False

    eta_6 = (
      eta6_squared.left
    )

    eta_7 = (
      eta6_squared.right
    )

    if not isinstance(
      eta_6,
      HomotopyElement,
    ):
      return False

    if (
      eta_6.dimension
      != 6
      or eta_6.source
      != 7
      or eta_6.target
      != 6
      or eta_6.generator
      != GeneratorSymbol(
        family="η",
        index=6,
      )
    ):
      return False

    if not isinstance(
      eta_7,
      HomotopyElement,
    ):
      return False

    if (
      eta_7.dimension
      != 7
      or eta_7.source
      != 8
      or eta_7.target
      != 7
      or eta_7.generator
      != GeneratorSymbol(
        family="η",
        index=7,
      )
    ):
      return False

    higher_relation = (
      prop53
      .higher_eta_squared_group_relation
    )

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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    if (
      prop53.higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    eta_n_squared = (
      higher_relation
      .rhs
      .generator
    )

    if not isinstance(
      eta_n_squared,
      Composition,
    ):
      return False

    eta_n = (
      eta_n_squared.left
    )

    eta_n_plus_one = (
      eta_n_squared.right
    )

    if not isinstance(
      eta_n,
      HomotopyElement,
    ):
      return False

    if not isinstance(
      eta_n_plus_one,
      HomotopyElement,
    ):
      return False

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    n_plus_two = ScalarSum(
      left=n,
      right=2,
    )

    if (
      eta_n
      != HomotopyElement(
        name="η_n",
        dimension=n,
        source=n_plus_one,
        target=n,
        generator=GeneratorSymbol(
          family="η",
          index=n,
        ),
      )
    ):
      return False

    return (
      eta_n_plus_one
      == HomotopyElement(
        name="η_(n+1)",
        dimension=n_plus_one,
        source=n_plus_two,
        target=n_plus_one,
        generator=GeneratorSymbol(
          family="η",
          index=n_plus_one,
        ),
      )
    )

  def build_conclusion(
    premises,
  ):
    pi8_3_relation = (
      premises[
        0
      ].conclusion
    )

    generator = (
      pi8_3_relation
      .rhs
      .generator
    )

    nu_prime = (
      generator.left
    )

    eta_7 = (
      generator
      .right
      .right
    )

    eta_8 = HomotopyElement(
      name="η₈",
      dimension=8,
      source=9,
      target=8,
      generator=GeneratorSymbol(
        family="η",
        index=8,
      ),
    )

    eta7_squared = Composition(
      left=eta_7,
      right=eta_8,
    )

    return Relation(
      lhs=Suspension(
        expression=generator,
      ),
      rhs=Composition(
        left=Suspension(
          expression=nu_prime,
        ),
        right=eta7_squared,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "E nu-prime eta_6 squared bridge"
    ),
    description=(
      "Use the independently derived "
      "pi_8^3=Z/2 generated by "
      "nu-prime composed with eta_6 squared "
      "and the independently derived "
      "Proposition 5.3 higher eta-square "
      "family. For the concrete n=7 "
      "instance, suspension functoriality "
      "gives "
      "E(nu-prime eta_6 squared) "
      "=E nu-prime eta_7 squared. "
      "The eta-square expression remains "
      "right-associated. "
      "No generic suspension-composition "
      "normalizer or theorem "
      "specialization engine is added."
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
          TodaProp53FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi9_4_decomposition_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda56 = (
      premises[
        0
      ].conclusion
    )

    pi8_3_relation = (
      premises[
        1
      ].conclusion
    )

    prop53 = (
      premises[
        2
      ].conclusion
    )

    suspension_bridge = (
      premises[
        3
      ].conclusion
    )

    decomposition_statement = (
      toda56
      .decomposition_isomorphism
    )

    prop44_isomorphism = (
      decomposition_statement
      .prop44_isomorphism
    )

    decomposition_map = (
      prop44_isomorphism.map
    )

    if not isinstance(
      decomposition_map,
      TodaProp44DecompositionMap,
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
      target_group
      .group_dimension
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    if (
      target_group
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=4,
      )
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
      source_group.summands
      != (
        TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=i,
            right=-1,
          ),
          sphere_dimension=3,
        ),
        TodaPrimaryGroup(
          group_dimension=i,
          sphere_dimension=7,
        ),
      )
    ):
      return False

    nu_4 = HomotopyElement(
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
      decomposition_map.alpha
      != nu_4
    ):
      return False

    if (
      decomposition_map.formula
      != Sum(
        left=Suspension(
          expression=decomposition_map.beta,
        ),
        right=Composition(
          left=nu_4,
          right=decomposition_map.gamma,
        ),
      )
    ):
      return False

    if (
      pi8_3_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=3,
      )
    ):
      return False

    if not isinstance(
      pi8_3_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi8_3_relation.rhs.order
      != 2
    ):
      return False

    nu_prime_eta6_squared = (
      pi8_3_relation
      .rhs
      .generator
    )

    if not isinstance(
      nu_prime_eta6_squared,
      Composition,
    ):
      return False

    nu_prime = (
      nu_prime_eta6_squared.left
    )

    eta6_squared = (
      nu_prime_eta6_squared.right
    )

    if not isinstance(
      nu_prime,
      HomotopyElement,
    ):
      return False

    if (
      nu_prime.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    if not isinstance(
      eta6_squared,
      Composition,
    ):
      return False

    eta_7 = (
      eta6_squared.right
    )

    eta_8 = HomotopyElement(
      name="η₈",
      dimension=8,
      source=9,
      target=8,
      generator=GeneratorSymbol(
        family="η",
        index=8,
      ),
    )

    eta7_squared = Composition(
      left=eta_7,
      right=eta_8,
    )

    higher_relation = (
      prop53
      .higher_eta_squared_group_relation
    )

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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    if (
      prop53.higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    if (
      suspension_bridge
      != Relation(
        lhs=Suspension(
          expression=nu_prime_eta6_squared,
        ),
        rhs=Composition(
          left=Suspension(
            expression=nu_prime,
          ),
          right=eta7_squared,
        ),
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    eta_n_squared = (
      higher_relation
      .rhs
      .generator
    )

    if not isinstance(
      eta_n_squared,
      Composition,
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    toda56 = (
      premises[
        0
      ].conclusion
    )

    pi8_3_relation = (
      premises[
        1
      ].conclusion
    )

    suspension_bridge = (
      premises[
        3
      ].conclusion
    )

    nu_4 = (
      toda56
      .lemma54_statement
      .nu4
    )

    nu_prime_eta6_squared = (
      pi8_3_relation
      .rhs
      .generator
    )

    eta_7 = (
      nu_prime_eta6_squared
      .right
      .right
    )

    eta_8 = HomotopyElement(
      name="η₈",
      dimension=8,
      source=9,
      target=8,
      generator=GeneratorSymbol(
        family="η",
        index=8,
      ),
    )

    eta7_squared = Composition(
      left=eta_7,
      right=eta_8,
    )

    nu4_eta7_squared = Composition(
      left=nu_4,
      right=eta7_squared,
    )

    e_nu_prime_eta7_squared = (
      suspension_bridge.rhs
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=4,
      ),
      rhs=DirectSumGroup(
        summands=(
          FiniteCyclicGroup(
            order=2,
            generator=nu4_eta7_squared,
          ),
          FiniteCyclicGroup(
            order=2,
            generator=e_nu_prime_eta7_squared,
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_9^4 decomposition"
    ),
    description=(
      "Specialize the independently "
      "derived Toda (5.6) decomposition "
      "pi_(i-1)^3 direct sum pi_i^7 "
      "isomorphic to pi_i^4 at i=9. "
      "Use the independently derived "
      "pi_8^3=Z/2 generated by "
      "nu-prime eta_6 squared and "
      "the Proposition 5.3 n=7 "
      "eta-square family instance. "
      "The first Toda (5.6) summand "
      "maps to "
      "E(nu-prime eta_6 squared), "
      "identified by the concrete bridge "
      "with E nu-prime eta_7 squared. "
      "The second summand maps to "
      "nu_4 eta_7 squared. "
      "Therefore pi_9^4 is the direct "
      "sum of two order-two cyclic groups "
      "generated by "
      "nu_4 eta_7 squared and "
      "E nu-prime eta_7 squared. "
      "No generic direct-sum transport "
      "or symbolic specialization "
      "framework is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda56Nu4DecompositionStatement
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
          TodaProp53FiniteDimensionalStatement
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


def toda_prop59_delta_eta9_squared_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_eta9 = (
      premises[
        0
      ].conclusion
    )

    pi9_4_relation = (
      premises[
        1
      ].conclusion
    )

    eta_9 = HomotopyElement(
      name="η₉",
      dimension=9,
      source=10,
      target=9,
      generator=GeneratorSymbol(
        family="η",
        index=9,
      ),
    )

    if (
      delta_eta9.lhs
      != MapApplication(
        map=EHP_DELTA_MAP,
        expression=eta_9,
      )
    ):
      return False

    e_nu_prime_eta7 = (
      delta_eta9.rhs
    )

    if not isinstance(
      e_nu_prime_eta7,
      Composition,
    ):
      return False

    e_nu_prime = (
      e_nu_prime_eta7.left
    )

    eta_7 = (
      e_nu_prime_eta7.right
    )

    if not isinstance(
      e_nu_prime,
      Suspension,
    ):
      return False

    nu_prime = (
      e_nu_prime.expression
    )

    if not isinstance(
      nu_prime,
      HomotopyElement,
    ):
      return False

    if (
      nu_prime.dimension
      != 3
      or nu_prime.source
      != 6
      or nu_prime.target
      != 3
      or nu_prime.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    if not isinstance(
      eta_7,
      HomotopyElement,
    ):
      return False

    if (
      eta_7.dimension
      != 7
      or eta_7.source
      != 8
      or eta_7.target
      != 7
      or eta_7.generator
      != GeneratorSymbol(
        family="η",
        index=7,
      )
    ):
      return False

    if (
      pi9_4_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=4,
      )
    ):
      return False

    if not isinstance(
      pi9_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi9_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    first = (
      pi9_4_relation
      .rhs
      .summands[
        0
      ]
    )

    second = (
      pi9_4_relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      first,
      FiniteCyclicGroup,
    ):
      return False

    if not isinstance(
      second,
      FiniteCyclicGroup,
    ):
      return False

    if (
      first.order
      != 2
      or second.order
      != 2
    ):
      return False

    e_nu_prime_eta7_squared = (
      second.generator
    )

    if not isinstance(
      e_nu_prime_eta7_squared,
      Composition,
    ):
      return False

    if (
      e_nu_prime_eta7_squared.left
      != e_nu_prime
    ):
      return False

    eta7_squared = (
      e_nu_prime_eta7_squared.right
    )

    if not isinstance(
      eta7_squared,
      Composition,
    ):
      return False

    if (
      eta7_squared.left
      != eta_7
    ):
      return False

    eta_8 = (
      eta7_squared.right
    )

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    return (
      eta_8.dimension
      == 8
      and eta_8.source
      == 9
      and eta_8.target
      == 8
      and eta_8.generator
      == GeneratorSymbol(
        family="η",
        index=8,
      )
    )

  def build_conclusion(
    premises,
  ):
    delta_eta9 = (
      premises[
        0
      ].conclusion
    )

    pi9_4_relation = (
      premises[
        1
      ].conclusion
    )

    eta_9 = (
      delta_eta9
      .lhs
      .expression
    )

    eta_10 = HomotopyElement(
      name="η₁₀",
      dimension=10,
      source=11,
      target=10,
      generator=GeneratorSymbol(
        family="η",
        index=10,
      ),
    )

    eta9_squared = Composition(
      left=eta_9,
      right=eta_10,
    )

    target_generator = (
      pi9_4_relation
      .rhs
      .summands[
        1
      ]
      .generator
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=eta9_squared,
      ),
      rhs=target_generator,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "Delta eta_9 squared"
    ),
    description=(
      "Use the independently derived "
      "Delta(eta_9)=E nu-prime eta_7 "
      "and the independently derived "
      "pi_9^4 decomposition whose second "
      "order-two generator is "
      "E nu-prime eta_7 squared. "
      "For the concrete Proposition 2.5 "
      "composition instance "
      "eta_9 squared=eta_9 eta_10, "
      "derive "
      "Delta(eta_9 squared) "
      "=E nu-prime eta_7 squared. "
      "The target generator is reused "
      "directly from the pi_9^4 branch. "
      "No generic Delta-composition or "
      "associativity normalizer is added."
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


def toda_512_n4_delta_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_eta9_squared = (
      premises[
        0
      ].conclusion
    )

    pi9_4_relation = (
      premises[
        1
      ].conclusion
    )

    prop53 = (
      premises[
        2
      ].conclusion
    )

    pi11_9 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=9,
    )

    pi9_4 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=4,
    )

    eta_9 = HomotopyElement(
      name="η₉",
      dimension=9,
      source=10,
      target=9,
      generator=GeneratorSymbol(
        family="η",
        index=9,
      ),
    )

    eta_10 = HomotopyElement(
      name="η₁₀",
      dimension=10,
      source=11,
      target=10,
      generator=GeneratorSymbol(
        family="η",
        index=10,
      ),
    )

    eta9_squared = Composition(
      left=eta_9,
      right=eta_10,
    )

    if (
      delta_eta9_squared
      != Relation(
        lhs=MapApplication(
          map=EHP_DELTA_MAP,
          expression=eta9_squared,
        ),
        rhs=delta_eta9_squared.rhs,
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    higher_relation = (
      prop53
      .higher_eta_squared_group_relation
    )

    higher_range = (
      prop53
      .higher_range
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

    if (
      higher_range.left
      != n
      or higher_range.right
      != 5
    ):
      return False

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
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

    if (
      higher_relation
      .rhs
      .generator
      != eta_n_squared
    ):
      return False

    if (
      pi9_4_relation.lhs
      != pi9_4
    ):
      return False

    if not isinstance(
      pi9_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi9_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    first = (
      pi9_4_relation
      .rhs
      .summands[
        0
      ]
    )

    second = (
      pi9_4_relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      first,
      FiniteCyclicGroup,
    ):
      return False

    if not isinstance(
      second,
      FiniteCyclicGroup,
    ):
      return False

    if (
      first.order
      != 2
      or second.order
      != 2
    ):
      return False

    if (
      delta_eta9_squared.rhs
      != second.generator
    ):
      return False

    return (
      pi11_9
      == TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=9,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=9,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=4,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda (5.12) "
      "n=4 Delta injective"
    ),
    description=(
      "Toda Proposition 5.3 gives "
      "pi_(n+2)^n=Z/2 generated by "
      "eta_n squared for n at least 5, "
      "so the n=9 specialization gives "
      "pi_11^9=Z/2 generated by "
      "eta_9 squared. "
      "Phase 70 gives "
      "Delta(eta_9 squared) "
      "=E nu-prime eta_7 squared, "
      "which is exactly the second "
      "order-two summand generator of "
      "pi_9^4. "
      "Therefore the concrete Delta map "
      "from pi_11^9 to pi_9^4 is "
      "injective. "
      "No generic cyclic-map "
      "injectivity solver or theorem "
      "specialization framework is added."
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
          TodaProp53FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_512_n5_delta_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_eta11 = (
      premises[
        0
      ].conclusion
    )

    pi10_5_relation = (
      premises[
        1
      ].conclusion
    )

    prop51 = (
      premises[
        2
      ].conclusion
    )

    if not isinstance(
      delta_eta11.lhs,
      MapApplication,
    ):
      return False

    if (
      delta_eta11.lhs.map
      != EHP_DELTA_MAP
    ):
      return False

    eta_11 = (
      delta_eta11
      .lhs
      .expression
    )

    if not isinstance(
      eta_11,
      HomotopyElement,
    ):
      return False

    if (
      eta_11.dimension
      != 11
      or eta_11.source
      != 12
      or eta_11.target
      != 11
      or eta_11.generator
      != GeneratorSymbol(
        family="η",
        index=11,
      )
    ):
      return False

    if (
      pi10_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi10_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi10_5_relation.rhs.order
      != 2
    ):
      return False

    if (
      delta_eta11.rhs
      != pi10_5_relation
      .rhs
      .generator
    ):
      return False

    higher_relation = (
      prop51
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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
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
    return TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=11,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=5,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda (5.12) "
      "n=5 Delta injective"
    ),
    description=(
      "The independently derived "
      "Proposition 5.1 higher eta-family "
      "gives pi_(n+1)^n cyclic of order 2 "
      "generated by eta_n, whose n=11 "
      "instance is pi_12^11 generated "
      "by eta_11. Phase 70 independently "
      "derives pi_10^5 cyclic of order 2 "
      "generated by nu_5 eta_8 squared "
      "and Delta(eta_11) equal to that "
      "same generator. Therefore the "
      "concrete Delta map from pi_12^11 "
      "to pi_10^5 is injective. "
      "No generic cyclic-map injectivity "
      "solver or theorem-specialization "
      "framework is introduced."
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
          TodaProp51FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_512_n6_delta_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi13_13_relation = (
      premises[
        0
      ].conclusion
    )

    pi11_6_relation = (
      premises[
        1
      ].conclusion
    )

    pi13_13 = TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=13,
    )

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    if (
      pi13_13_relation.lhs
      != pi13_13
    ):
      return False

    if not isinstance(
      pi13_13_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    iota_13 = (
      pi13_13_relation
      .rhs
      .generator
    )

    if not isinstance(
      iota_13,
      HomotopyElement,
    ):
      return False

    if (
      iota_13.dimension
      != 13
      or iota_13.generator
      != GeneratorSymbol(
        family="ι",
        index=13,
      )
    ):
      return False

    if (
      pi11_6_relation.lhs
      != pi11_6
    ):
      return False

    if not isinstance(
      pi11_6_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    expected_target_generator = (
      MapApplication(
        map=EHP_DELTA_MAP,
        expression=iota_13,
      )
    )

    return (
      pi11_6_relation
      .rhs
      .generator
      == expected_target_generator
    )

  def build_conclusion(
    premises,
  ):
    return TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=13,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda (5.12) "
      "n=6 Delta injective"
    ),
    description=(
      "Use the foundational free cyclic "
      "group pi_13^13 generated by "
      "iota_13 and the independently "
      "derived free cyclic group "
      "pi_11^6 generated by "
      "Delta(iota_13). Since Delta sends "
      "the source free generator to the "
      "target free generator, the "
      "concrete Delta map from pi_13^13 "
      "to pi_11^6 is injective. "
      "No generic free-cyclic generator "
      "injectivity solver is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
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


def toda_512_delta_injectivity_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    n4_injectivity = (
      premises[
        0
      ].conclusion
    )

    n5_injectivity = (
      premises[
        1
      ].conclusion
    )

    n6_injectivity = (
      premises[
        2
      ].conclusion
    )

    expected_n4 = (
      TodaDeltaInjectiveStatement(
        map=TodaDeltaMap(
          source_group=TodaPrimaryGroup(
            group_dimension=11,
            sphere_dimension=9,
          ),
          target_group=TodaPrimaryGroup(
            group_dimension=9,
            sphere_dimension=4,
          ),
        )
      )
    )

    expected_n5 = (
      TodaDeltaInjectiveStatement(
        map=TodaDeltaMap(
          source_group=TodaPrimaryGroup(
            group_dimension=12,
            sphere_dimension=11,
          ),
          target_group=TodaPrimaryGroup(
            group_dimension=10,
            sphere_dimension=5,
          ),
        )
      )
    )

    expected_n6 = (
      TodaDeltaInjectiveStatement(
        map=TodaDeltaMap(
          source_group=TodaPrimaryGroup(
            group_dimension=13,
            sphere_dimension=13,
          ),
          target_group=TodaPrimaryGroup(
            group_dimension=11,
            sphere_dimension=6,
          ),
        )
      )
    )

    return (
      n4_injectivity
      == expected_n4
      and n5_injectivity
      == expected_n5
      and n6_injectivity
      == expected_n6
    )

  def build_conclusion(
    premises,
  ):
    return Toda512DeltaInjectivityStatement(
      n4_injectivity=(
        premises[
          0
        ].conclusion
      ),
      n5_injectivity=(
        premises[
          1
        ].conclusion
      ),
      n6_injectivity=(
        premises[
          2
        ].conclusion
      ),
      literature_statements=(
        toda_512_delta_injectivity_literature_statements()
      ),
    )

  return InferenceRule(
    name=(
      "Toda (5.12) "
      "three-case Delta injectivity "
      "integration"
    ),
    description=(
      "Integrate the independently "
      "derived Toda (5.12) Delta "
      "injectivity cases n=4, n=5, "
      "and n=6 into a single "
      "literature-aware statement. "
      "All three concrete injectivity "
      "results must already be "
      "ProofRule.INFERENCE. "
      "No generic range-valued map "
      "property theorem or Delta "
      "injectivity framework is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaInjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi10_9_delta_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_eta9 = (
      premises[
        0
      ].conclusion
    )

    pi8_4_relation = (
      premises[
        1
      ].conclusion
    )

    prop51 = (
      premises[
        2
      ].conclusion
    )

    pi10_9 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=9,
    )

    pi8_4 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    )

    eta_9 = HomotopyElement(
      name="η₉",
      dimension=9,
      source=10,
      target=9,
      generator=GeneratorSymbol(
        family="η",
        index=9,
      ),
    )

    if (
      delta_eta9
      != Relation(
        lhs=MapApplication(
          map=EHP_DELTA_MAP,
          expression=eta_9,
        ),
        rhs=delta_eta9.rhs,
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    higher_eta_relation = (
      prop51
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

    if (
      higher_eta_relation.rhs.order
      != 2
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
      higher_eta_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    eta_n = (
      higher_eta_relation
      .rhs
      .generator
    )

    if not isinstance(
      eta_n,
      HomotopyElement,
    ):
      return False

    if (
      eta_n.dimension
      != n
      or eta_n.target
      != n
      or eta_n.source
      != ScalarSum(
        left=n,
        right=1,
      )
      or eta_n.generator
      != GeneratorSymbol(
        family="η",
        index=n,
      )
    ):
      return False

    if (
      pi8_4_relation.lhs
      != pi8_4
    ):
      return False

    if not isinstance(
      pi8_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi8_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    first = (
      pi8_4_relation
      .rhs
      .summands[
        0
      ]
    )

    second = (
      pi8_4_relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      first,
      FiniteCyclicGroup,
    ):
      return False

    if not isinstance(
      second,
      FiniteCyclicGroup,
    ):
      return False

    if (
      first.order
      != 2
      or second.order
      != 2
    ):
      return False

    return (
      delta_eta9.rhs
      == second.generator
    )

  def build_conclusion(
    premises,
  ):
    return TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=9,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=8,
          sphere_dimension=4,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_10^9 Delta injective"
    ),
    description=(
      "Proposition 5.1 gives the "
      "order-two eta-family source "
      "pi_10^9=Z/2 generated by eta_9. "
      "Phase 68 gives "
      "Delta(eta_9)=E nu-prime eta_7, "
      "which is exactly the second "
      "order-two summand generator of "
      "pi_8^4. "
      "Therefore the concrete Delta map "
      "from pi_10^9 to pi_8^4 is "
      "injective. "
      "No generic cyclic-map "
      "injectivity solver is added."
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
          TodaProp51FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi10_5_concrete_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    e_h_window = TodaEHPExactnessWindow(
      source_term=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=4,
      ),
      middle_term=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      target_term=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=9,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )

    h_delta_window = TodaEHPExactnessWindow(
      source_term=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      middle_term=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=9,
      ),
      target_term=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=4,
      ),
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    )

    return (
      window
      in (
        e_h_window,
        h_delta_window,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_10^5 concrete exactness"
    ),
    description=(
      "Recognize only the two concrete "
      "Toda Proposition 4.2 exactness "
      "windows required for the "
      "Proposition 5.9 pi_10^5 branch: "
      "pi_9^4 -> pi_10^5 -> pi_10^9 "
      "and "
      "pi_10^5 -> pi_10^9 -> pi_8^4. "
      "No generic concrete EHP "
      "specialization framework is added."
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


def toda_prop59_pi10_5_hopf_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_injective = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    pi10_5 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
    )

    pi10_9 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=9,
    )

    pi8_4 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=4,
    )

    window = (
      exactness.window
    )

    if (
      window
      != TodaEHPExactnessWindow(
        source_term=pi10_5,
        middle_term=pi10_9,
        target_term=pi8_4,
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
      )
    ):
      return False

    return (
      delta_injective.map
      == TodaDeltaMap(
        source_group=pi10_9,
        target_group=pi8_4,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[
        1
      ].conclusion
      .window
    )

    return TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_10^5 Hopf zero"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_10^5 -> pi_10^9 -> pi_8^4, "
      "the Delta map is injective. "
      "Hence Ker(Delta)=0. "
      "Exactness gives Im(H)=0, "
      "so H:pi_10^5 to pi_10^9 "
      "is the zero map."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi10_5_suspension_surjective_inference_rule():
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

    pi9_4 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=4,
    )

    pi10_5 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
    )

    pi10_9 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=9,
    )

    window = (
      exactness.window
    )

    if (
      window
      != TodaEHPExactnessWindow(
        source_term=pi9_4,
        middle_term=pi10_5,
        target_term=pi10_9,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      )
    ):
      return False

    return (
      hopf_zero.map
      == TodaHopfInvariantMap(
        source_group=pi10_5,
        target_group=pi10_9,
      )
    )

  def build_conclusion(
    premises,
  ):
    window = (
      premises[
        1
      ].conclusion
      .window
    )

    return TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_10^5 suspension surjective"
    ),
    description=(
      "For the concrete exact sequence "
      "pi_9^4 -> pi_10^5 -> pi_10^9, "
      "the Hopf invariant is zero. "
      "Therefore Ker(H)=pi_10^5. "
      "Exactness gives Im(E)=pi_10^5, "
      "so suspension "
      "E:pi_9^4 to pi_10^5 "
      "is surjective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantZeroStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi10_5_delta_e_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    return (
      window
      == TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=9,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=4,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=5,
        ),
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_10^5 Delta-E exactness"
    ),
    description=(
      "Recognize the concrete Toda "
      "Proposition 4.2 exactness window "
      "pi_11^9 -> pi_9^4 -> pi_10^5 "
      "with Delta followed by suspension E. "
      "This is the precise Delta-E window "
      "required for the Proposition 5.9 "
      "pi_10^5 calculation. "
      "No generic symbolic EHP "
      "specialization is introduced."
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


def toda_prop59_e_nu4_eta7_squared_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi9_4_relation = (
      premises[
        0
      ].conclusion
    )

    phase68_bridge = (
      premises[
        1
      ].conclusion
    )

    if (
      pi9_4_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=4,
      )
    ):
      return False

    if not isinstance(
      pi9_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi9_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    first = (
      pi9_4_relation
      .rhs
      .summands[
        0
      ]
    )

    if not isinstance(
      first,
      FiniteCyclicGroup,
    ):
      return False

    if (
      first.order
      != 2
    ):
      return False

    nu4_eta7_squared = (
      first.generator
    )

    if not isinstance(
      nu4_eta7_squared,
      Composition,
    ):
      return False

    nu_4 = (
      nu4_eta7_squared.left
    )

    eta7_squared = (
      nu4_eta7_squared.right
    )

    if not isinstance(
      nu_4,
      HomotopyElement,
    ):
      return False

    if (
      nu_4.dimension
      != 4
      or nu_4.source
      != 7
      or nu_4.target
      != 4
      or nu_4.generator
      != GeneratorSymbol(
        family="ν",
        index=4,
      )
    ):
      return False

    if not isinstance(
      eta7_squared,
      Composition,
    ):
      return False

    eta_7 = (
      eta7_squared.left
    )

    eta_8 = (
      eta7_squared.right
    )

    if not isinstance(
      eta_7,
      HomotopyElement,
    ):
      return False

    if (
      eta_7.dimension
      != 7
      or eta_7.source
      != 8
      or eta_7.target
      != 7
      or eta_7.generator
      != GeneratorSymbol(
        family="η",
        index=7,
      )
    ):
      return False

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    if (
      eta_8.dimension
      != 8
      or eta_8.source
      != 9
      or eta_8.target
      != 8
      or eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    expected_phase68_lhs = Suspension(
      expression=Composition(
        left=nu_4,
        right=eta_7,
      ),
    )

    if (
      phase68_bridge.lhs
      != expected_phase68_lhs
    ):
      return False

    if not isinstance(
      phase68_bridge.rhs,
      Composition,
    ):
      return False

    nu_5 = (
      phase68_bridge
      .rhs
      .left
    )

    bridge_eta_8 = (
      phase68_bridge
      .rhs
      .right
    )

    if not isinstance(
      nu_5,
      HomotopyElement,
    ):
      return False

    if (
      nu_5.dimension
      != 5
      or nu_5.source
      != 8
      or nu_5.target
      != 5
      or nu_5.generator
      != GeneratorSymbol(
        family="ν",
        index=5,
      )
    ):
      return False

    return (
      bridge_eta_8
      == eta_8
    )

  def build_conclusion(
    premises,
  ):
    pi9_4_relation = (
      premises[
        0
      ].conclusion
    )

    phase68_bridge = (
      premises[
        1
      ].conclusion
    )

    first_generator = (
      pi9_4_relation
      .rhs
      .summands[
        0
      ]
      .generator
    )

    nu_5 = (
      phase68_bridge
      .rhs
      .left
    )

    eta_8 = (
      phase68_bridge
      .rhs
      .right
    )

    eta_9 = HomotopyElement(
      name="η₉",
      dimension=9,
      source=10,
      target=9,
      generator=GeneratorSymbol(
        family="η",
        index=9,
      ),
    )

    eta8_squared = Composition(
      left=eta_8,
      right=eta_9,
    )

    nu5_eta8_squared = Composition(
      left=nu_5,
      right=eta8_squared,
    )

    return Relation(
      lhs=Suspension(
        expression=first_generator,
      ),
      rhs=nu5_eta8_squared,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "E nu_4 eta_7 squared bridge"
    ),
    description=(
      "Use the independently derived "
      "pi_9^4 first summand "
      "nu_4 eta_7 squared together with "
      "the Phase 68 bridge "
      "E(nu_4 eta_7)=nu_5 eta_8. "
      "For the concrete additional "
      "eta factor, derive "
      "E(nu_4 eta_7 squared) "
      "=nu_5 eta_8 squared. "
      "The existing nu_5 and eta_8 "
      "objects are reused from the "
      "Phase 68 bridge. "
      "No generic suspension-composition "
      "normalizer is introduced."
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


def toda_prop59_pi10_5_finite_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi9_4_relation = (
      premises[
        0
      ].conclusion
    )

    delta_eta9_squared = (
      premises[
        1
      ].conclusion
    )

    prop53 = (
      premises[
        2
      ].conclusion
    )

    exactness = (
      premises[
        3
      ].conclusion
    )

    surjective = (
      premises[
        4
      ].conclusion
    )

    suspension_bridge = (
      premises[
        5
      ].conclusion
    )

    pi11_9 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=9,
    )

    pi9_4 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=4,
    )

    pi10_5 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
    )

    if (
      pi9_4_relation.lhs
      != pi9_4
    ):
      return False

    if not isinstance(
      pi9_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi9_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    first = (
      pi9_4_relation
      .rhs
      .summands[
        0
      ]
    )

    second = (
      pi9_4_relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      first,
      FiniteCyclicGroup,
    ):
      return False

    if not isinstance(
      second,
      FiniteCyclicGroup,
    ):
      return False

    if (
      first.order
      != 2
      or second.order
      != 2
    ):
      return False

    higher_relation = (
      prop53
      .higher_eta_squared_group_relation
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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    if (
      prop53.higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    eta_n_squared = (
      higher_relation
      .rhs
      .generator
    )

    if not isinstance(
      eta_n_squared,
      Composition,
    ):
      return False

    eta_n = (
      eta_n_squared.left
    )

    eta_n_plus_one = (
      eta_n_squared.right
    )

    if not isinstance(
      eta_n,
      HomotopyElement,
    ):
      return False

    if not isinstance(
      eta_n_plus_one,
      HomotopyElement,
    ):
      return False

    if (
      eta_n.generator
      != GeneratorSymbol(
        family="η",
        index=n,
      )
    ):
      return False

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    if (
      eta_n_plus_one.generator
      != GeneratorSymbol(
        family="η",
        index=n_plus_one,
      )
    ):
      return False

    window = (
      exactness.window
    )

    if (
      window
      != TodaEHPExactnessWindow(
        source_term=pi11_9,
        middle_term=pi9_4,
        target_term=pi10_5,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      )
    ):
      return False

    if (
      surjective.map
      != TodaSuspensionMap(
        source_group=pi9_4,
        target_group=pi10_5,
      )
    ):
      return False

    if not isinstance(
      delta_eta9_squared.lhs,
      MapApplication,
    ):
      return False

    if (
      delta_eta9_squared.lhs.map
      != EHP_DELTA_MAP
    ):
      return False

    eta9_squared = (
      delta_eta9_squared
      .lhs
      .expression
    )

    if not isinstance(
      eta9_squared,
      Composition,
    ):
      return False

    eta_9 = (
      eta9_squared.left
    )

    eta_10 = (
      eta9_squared.right
    )

    if not isinstance(
      eta_9,
      HomotopyElement,
    ):
      return False

    if not isinstance(
      eta_10,
      HomotopyElement,
    ):
      return False

    if (
      eta_9.dimension
      != 9
      or eta_9.source
      != 10
      or eta_9.target
      != 9
      or eta_9.generator
      != GeneratorSymbol(
        family="η",
        index=9,
      )
    ):
      return False

    if (
      eta_10.dimension
      != 10
      or eta_10.source
      != 11
      or eta_10.target
      != 10
      or eta_10.generator
      != GeneratorSymbol(
        family="η",
        index=10,
      )
    ):
      return False

    if (
      delta_eta9_squared.rhs
      != second.generator
    ):
      return False

    if (
      suspension_bridge.lhs
      != Suspension(
        expression=first.generator,
      )
    ):
      return False

    if not isinstance(
      suspension_bridge.rhs,
      Composition,
    ):
      return False

    nu_5 = (
      suspension_bridge
      .rhs
      .left
    )

    eta8_squared = (
      suspension_bridge
      .rhs
      .right
    )

    if not isinstance(
      nu_5,
      HomotopyElement,
    ):
      return False

    if (
      nu_5.dimension
      != 5
      or nu_5.source
      != 8
      or nu_5.target
      != 5
      or nu_5.generator
      != GeneratorSymbol(
        family="ν",
        index=5,
      )
    ):
      return False

    if not isinstance(
      eta8_squared,
      Composition,
    ):
      return False

    eta_8 = (
      eta8_squared.left
    )

    bridge_eta_9 = (
      eta8_squared.right
    )

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    if (
      eta_8.dimension
      != 8
      or eta_8.source
      != 9
      or eta_8.target
      != 8
      or eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    return (
      bridge_eta_9
      == eta_9
    )

  def build_conclusion(
    premises,
  ):
    suspension_bridge = (
      premises[
        5
      ].conclusion
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=(
          suspension_bridge.rhs
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_10^5 finite cyclic"
    ),
    description=(
      "Phase 70-4 gives "
      "pi_9^4 as the direct sum of "
      "two order-two cyclic summands. "
      "Phase 70-5 gives "
      "Delta(eta_9 squared) "
      "=E nu-prime eta_7 squared, "
      "which is exactly the second "
      "summand generator. "
      "Proposition 5.3 gives the "
      "order-two source "
      "pi_11^9 generated by "
      "eta_9 squared, so exactness "
      "identifies Ker(E) with precisely "
      "the second summand. "
      "The independently derived "
      "surjectivity of E then makes "
      "pi_10^5 the quotient by that "
      "summand. "
      "The remaining first generator "
      "nu_4 eta_7 squared suspends to "
      "nu_5 eta_8 squared. "
      "Therefore "
      "pi_10^5=Z/2 generated by "
      "nu_5 eta_8 squared. "
      "No generic quotient solver, "
      "direct-sum kernel solver, or "
      "cyclic-image solver is added."
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
          TodaProp53FiniteDimensionalStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaSuspensionSurjectiveStatement
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


def toda_prop59_e_nu5_eta8_squared_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi10_5_relation = (
      premises[
        0
      ].conclusion
    )

    nu6_eta9_zero = (
      premises[
        1
      ].conclusion
    )

    if (
      pi10_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi10_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi10_5_relation.rhs.order
      != 2
    ):
      return False

    nu5_eta8_squared = (
      pi10_5_relation
      .rhs
      .generator
    )

    if not isinstance(
      nu5_eta8_squared,
      Composition,
    ):
      return False

    nu_5 = (
      nu5_eta8_squared.left
    )

    eta8_squared = (
      nu5_eta8_squared.right
    )

    if not isinstance(
      nu_5,
      HomotopyElement,
    ):
      return False

    if (
      nu_5.dimension
      != 5
      or nu_5.source
      != 8
      or nu_5.target
      != 5
      or nu_5.generator
      != GeneratorSymbol(
        family="ν",
        index=5,
      )
    ):
      return False

    if not isinstance(
      eta8_squared,
      Composition,
    ):
      return False

    eta_8 = (
      eta8_squared.left
    )

    eta_9 = (
      eta8_squared.right
    )

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    if (
      eta_8.dimension
      != 8
      or eta_8.source
      != 9
      or eta_8.target
      != 8
      or eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    if not isinstance(
      eta_9,
      HomotopyElement,
    ):
      return False

    if (
      eta_9.dimension
      != 9
      or eta_9.source
      != 10
      or eta_9.target
      != 9
      or eta_9.generator
      != GeneratorSymbol(
        family="η",
        index=9,
      )
    ):
      return False

    if (
      nu6_eta9_zero.relation_type
      != RelationType.ZERO
    ):
      return False

    if (
      nu6_eta9_zero.rhs
      != Zero()
    ):
      return False

    if not isinstance(
      nu6_eta9_zero.lhs,
      Composition,
    ):
      return False

    nu_6 = (
      nu6_eta9_zero
      .lhs
      .left
    )

    zero_eta_9 = (
      nu6_eta9_zero
      .lhs
      .right
    )

    if not isinstance(
      nu_6,
      HomotopyElement,
    ):
      return False

    if (
      nu_6.dimension
      != 6
      or nu_6.source
      != 9
      or nu_6.target
      != 6
      or nu_6.generator
      != GeneratorSymbol(
        family="ν",
        index=6,
      )
    ):
      return False

    if not isinstance(
      zero_eta_9,
      HomotopyElement,
    ):
      return False

    return (
      zero_eta_9.dimension
      == eta_9.dimension
      and zero_eta_9.source
      == eta_9.source
      and zero_eta_9.target
      == eta_9.target
      and zero_eta_9.generator
      == eta_9.generator
    )

  def build_conclusion(
    premises,
  ):
    pi10_5_relation = (
      premises[
        0
      ].conclusion
    )

    return Relation(
      lhs=Suspension(
        expression=(
          pi10_5_relation
          .rhs
          .generator
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "E nu_5 eta_8 squared zero"
    ),
    description=(
      "Use the independently derived "
      "pi_10^5=Z/2 generated by "
      "nu_5 eta_8 squared and the "
      "independently derived concrete "
      "Phase 68 relation nu_6 eta_9=0. "
      "For this concrete suspension, "
      "E(nu_5 eta_8 squared) "
      "is nu_6 eta_9 eta_10 and therefore "
      "vanishes because nu_6 eta_9=0. "
      "The eta_9 factors are matched by "
      "their homotopy typing and canonical "
      "generator symbol rather than by "
      "display-name-sensitive structural "
      "equality. "
      "No generic suspension-composition, "
      "associativity, or zero-substitution "
      "framework is introduced."
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
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi11_6_concrete_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    e_h_window = TodaEHPExactnessWindow(
      source_term=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      ),
      middle_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
      target_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    )

    h_delta_window = TodaEHPExactnessWindow(
      source_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
      middle_term=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=11,
      ),
      target_term=TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=5,
      ),
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    )

    return (
      window
      in (
        e_h_window,
        h_delta_window,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_11^6 concrete exactness"
    ),
    description=(
      "Recognize only the two concrete "
      "Toda Proposition 4.2 exactness "
      "windows required for the "
      "Proposition 5.9 pi_11^6 branch: "
      "pi_10^5 -> pi_11^6 -> pi_11^11 "
      "and "
      "pi_11^6 -> pi_11^11 -> pi_9^5. "
      "No generic concrete EHP "
      "specialization framework is added."
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


def toda_prop59_pi11_6_hopf_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    suspension_zero = (
      premises[
        0
      ].conclusion
    )

    pi10_5_relation = (
      premises[
        1
      ].conclusion
    )

    exactness = (
      premises[
        2
      ].conclusion
    )

    pi10_5 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
    )

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    pi11_11 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=11,
    )

    if (
      pi10_5_relation.lhs
      != pi10_5
    ):
      return False

    if not isinstance(
      pi10_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi10_5_relation.rhs.order
      != 2
    ):
      return False

    generator = (
      pi10_5_relation
      .rhs
      .generator
    )

    if (
      suspension_zero
      != Relation(
        lhs=Suspension(
          expression=generator,
        ),
        rhs=Zero(),
        relation_type=RelationType.ZERO,
      )
    ):
      return False

    return (
      exactness.window
      == TodaEHPExactnessWindow(
        source_term=pi10_5,
        middle_term=pi11_6,
        target_term=pi11_11,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      )
    )

  def build_conclusion(
    premises,
  ):
    exactness = (
      premises[
        2
      ].conclusion
    )

    window = (
      exactness.window
    )

    return TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=window.middle_term,
        target_group=window.target_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_11^6 Hopf injective"
    ),
    description=(
      "Phase 70-7 gives that suspension "
      "vanishes on the generator of "
      "pi_10^5, hence "
      "E:pi_10^5 to pi_11^6 "
      "is the zero map. "
      "Exactness of "
      "pi_10^5 -> pi_11^6 -> pi_11^11 "
      "therefore gives Ker(H)=0. "
      "Thus H:pi_11^6 to pi_11^11 "
      "is injective."
    ),
    premise_patterns=(
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
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi11_11_delta_kernel_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi11_11_relation = (
      premises[
        0
      ].conclusion
    )

    pi9_5_relation = (
      premises[
        1
      ].conclusion
    )

    delta_iota11 = (
      premises[
        2
      ].conclusion
    )

    pi11_11 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=11,
    )

    pi9_5 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )

    if (
      pi11_11_relation.lhs
      != pi11_11
    ):
      return False

    if not isinstance(
      pi11_11_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    iota_11 = (
      pi11_11_relation
      .rhs
      .generator
    )

    if not isinstance(
      iota_11,
      HomotopyElement,
    ):
      return False

    if (
      iota_11.dimension
      != 11
      or iota_11.generator
      != GeneratorSymbol(
        family="ι",
        index=11,
      )
    ):
      return False

    if (
      pi9_5_relation.lhs
      != pi9_5
    ):
      return False

    if not isinstance(
      pi9_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi9_5_relation.rhs.order
      != 2
    ):
      return False

    target_generator = (
      pi9_5_relation
      .rhs
      .generator
    )

    expected_delta_iota11 = Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=iota_11,
      ),
      rhs=target_generator,
      relation_type=RelationType.EQUALITY,
    )

    return (
      delta_iota11
      == expected_delta_iota11
    )

  def build_conclusion(
    premises,
  ):
    pi11_11_relation = (
      premises[
        0
      ].conclusion
    )

    iota_11 = (
      pi11_11_relation
      .rhs
      .generator
    )

    return TodaDeltaKernelFreeCyclicStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=11,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=5,
        ),
      ),
      kernel_group=FreeCyclicGroup(
        generator=Multiple(
          coefficient=2,
          expression=iota_11,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_11^11 Delta kernel"
    ),
    description=(
      "Use the foundational "
      "pi_11^11=Z generated by iota_11, "
      "the independently derived "
      "pi_9^5=Z/2 generated by "
      "nu_5 eta_8, and the independently "
      "derived Toda (5.10) equality "
      "Delta(iota_11)=nu_5 eta_8. "
      "The resulting concrete Delta map "
      "has kernel freely generated by "
      "2 iota_11. "
      "No generic free-to-finite cyclic "
      "kernel solver is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
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
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_delta_iota13_hopf_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi13_13_relation = (
      premises[
        0
      ].conclusion
    )

    if (
      pi13_13_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=13,
        sphere_dimension=13,
      )
    ):
      return False

    if not isinstance(
      pi13_13_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    iota_13 = (
      pi13_13_relation
      .rhs
      .generator
    )

    if not isinstance(
      iota_13,
      HomotopyElement,
    ):
      return False

    return (
      iota_13.dimension
      == 13
      and iota_13.generator
      == GeneratorSymbol(
        family="ι",
        index=13,
      )
    )

  def build_conclusion(
    premises,
  ):
    pi13_13_relation = (
      premises[
        0
      ].conclusion
    )

    iota_13 = (
      pi13_13_relation
      .rhs
      .generator
    )

    iota_11 = HomotopyElement(
      name="ι_11",
      dimension=11,
      generator=GeneratorSymbol(
        family="ι",
        index=11,
      ),
    )

    delta_iota13 = MapApplication(
      map=EHP_DELTA_MAP,
      expression=iota_13,
    )

    return (
      TodaProp27HopfInvariantUpToSignStatement(
        argument=delta_iota13,
        positive_value=Multiple(
          coefficient=2,
          expression=iota_11,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "Delta iota_13 Hopf value"
    ),
    description=(
      "Apply the concrete Toda "
      "Proposition 2.7 consequence "
      "needed in Proposition 5.9: "
      "H(Delta(iota_13)) "
      "equals plus or minus 2 iota_11. "
      "The source identity generator "
      "iota_13 is required to come from "
      "the foundational free cyclic "
      "group pi_13^13. "
      "The existing up-to-sign Hopf "
      "statement representation is reused. "
      "No generic Proposition 2.7 "
      "quantification framework is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi11_6_free_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_injective = (
      premises[
        0
      ].conclusion
    )

    h_delta_exactness = (
      premises[
        1
      ].conclusion
    )

    delta_kernel = (
      premises[
        2
      ].conclusion
    )

    hopf_value = (
      premises[
        3
      ].conclusion
    )

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    pi11_11 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=11,
    )

    pi9_5 = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )

    expected_hopf_map = TodaHopfInvariantMap(
      source_group=pi11_6,
      target_group=pi11_11,
    )

    if (
      hopf_injective.map
      != expected_hopf_map
    ):
      return False

    expected_window = TodaEHPExactnessWindow(
      source_term=pi11_6,
      middle_term=pi11_11,
      target_term=pi9_5,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    )

    if (
      h_delta_exactness.window
      != expected_window
    ):
      return False

    expected_delta_map = TodaDeltaMap(
      source_group=pi11_11,
      target_group=pi9_5,
    )

    if (
      delta_kernel.map
      != expected_delta_map
    ):
      return False

    kernel_group = (
      delta_kernel.kernel_group
    )

    if not isinstance(
      kernel_group,
      FreeCyclicGroup,
    ):
      return False

    kernel_generator = (
      kernel_group.generator
    )

    if not isinstance(
      kernel_generator,
      Multiple,
    ):
      return False

    if (
      kernel_generator.coefficient
      != 2
    ):
      return False

    iota_11 = (
      kernel_generator.expression
    )

    if not isinstance(
      iota_11,
      HomotopyElement,
    ):
      return False

    if (
      iota_11.dimension
      != 11
      or iota_11.generator
      != GeneratorSymbol(
        family="ι",
        index=11,
      )
    ):
      return False

    if (
      hopf_value.positive_value
      != kernel_generator
    ):
      return False

    delta_iota13 = (
      hopf_value.argument
    )

    if not isinstance(
      delta_iota13,
      MapApplication,
    ):
      return False

    if (
      delta_iota13.map
      != EHP_DELTA_MAP
    ):
      return False

    iota_13 = (
      delta_iota13.expression
    )

    if not isinstance(
      iota_13,
      HomotopyElement,
    ):
      return False

    return (
      iota_13.dimension
      == 13
      and iota_13.generator
      == GeneratorSymbol(
        family="ι",
        index=13,
      )
    )

  def build_conclusion(
    premises,
  ):
    hopf_value = (
      premises[
        3
      ].conclusion
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      ),
      rhs=FreeCyclicGroup(
        generator=(
          hopf_value.argument
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_11^6 free cyclic"
    ),
    description=(
      "The concrete E-H exactness branch "
      "makes "
      "H:pi_11^6 to pi_11^11 injective. "
      "Concrete H-Delta exactness gives "
      "Im(H)=Ker(Delta). "
      "The latter kernel is freely "
      "generated by 2 iota_11. "
      "Toda Proposition 2.7 gives "
      "H(Delta(iota_13)) "
      "=plus or minus 2 iota_11. "
      "Therefore Delta(iota_13) generates "
      "pi_11^6 freely. "
      "No generic free-group preimage, "
      "kernel-image, or generator "
      "transport solver is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaKernelFreeCyclicStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp27HopfInvariantUpToSignStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi12_7_concrete_exactness_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    window = (
      premises[
        0
      ].conclusion
    )

    delta_e_window = (
      TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=13,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=7,
        ),
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      )
    )

    e_h_window = (
      TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=7,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=12,
          sphere_dimension=13,
        ),
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      )
    )

    return (
      window
      in (
        delta_e_window,
        e_h_window,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp42ExactnessStatement(
      window=(
        premises[
          0
        ].conclusion
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_12^7 concrete exactness"
    ),
    description=(
      "Recognize only the two concrete "
      "Toda Proposition 4.2 exactness "
      "windows required for the "
      "Proposition 5.9 pi_12^7 branch: "
      "pi_13^13 -> pi_11^6 -> pi_12^7 "
      "with Delta followed by E, and "
      "pi_11^6 -> pi_12^7 -> pi_12^13 "
      "with E followed by H. "
      "No generic concrete EHP "
      "specialization framework is added."
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


def toda_prop59_pi13_13_delta_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi13_13_relation = (
      premises[
        0
      ].conclusion
    )

    pi11_6_relation = (
      premises[
        1
      ].conclusion
    )

    pi13_13 = TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=13,
    )

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    if (
      pi13_13_relation.lhs
      != pi13_13
    ):
      return False

    if not isinstance(
      pi13_13_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    iota_13 = (
      pi13_13_relation
      .rhs
      .generator
    )

    if not isinstance(
      iota_13,
      HomotopyElement,
    ):
      return False

    if (
      iota_13.dimension
      != 13
      or iota_13.generator
      != GeneratorSymbol(
        family="ι",
        index=13,
      )
    ):
      return False

    if (
      pi11_6_relation.lhs
      != pi11_6
    ):
      return False

    if not isinstance(
      pi11_6_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    expected_generator = MapApplication(
      map=EHP_DELTA_MAP,
      expression=iota_13,
    )

    return (
      pi11_6_relation
      .rhs
      .generator
      == expected_generator
    )

  def build_conclusion(
    premises,
  ):
    return TodaDeltaSurjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=13,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_13^13 Delta surjective"
    ),
    description=(
      "Use the foundational free cyclic "
      "group pi_13^13 generated by "
      "iota_13 and the independently "
      "derived "
      "pi_11^6=Z generated by "
      "Delta(iota_13). "
      "Since the source generator maps "
      "to the target generator, the "
      "concrete Delta map "
      "pi_13^13 to pi_11^6 "
      "is surjective. "
      "No generic free-cyclic generator "
      "surjectivity solver is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
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


def toda_prop59_pi12_7_suspension_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    zero_target = (
      premises[
        0
      ].conclusion
    )

    exactness = (
      premises[
        1
      ].conclusion
    )

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    pi12_7 = TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=7,
    )

    pi12_13 = TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=13,
    )

    if (
      zero_target
      != TodaPrimaryGroupZeroStatement(
        group=pi12_13,
      )
    ):
      return False

    return (
      exactness.window
      == TodaEHPExactnessWindow(
        source_term=pi11_6,
        middle_term=pi12_7,
        target_term=pi12_13,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
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

    window = (
      exactness.window
    )

    return TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=window.source_term,
        target_group=window.middle_term,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_12^7 suspension surjective"
    ),
    description=(
      "Use the foundational zero group "
      "pi_12^13=0 and exactness of "
      "pi_11^6 -> pi_12^7 -> pi_12^13. "
      "Since the Hopf target is zero, "
      "Ker(H)=pi_12^7. "
      "Exactness therefore gives "
      "Im(E)=pi_12^7, so "
      "E:pi_11^6 to pi_12^7 "
      "is surjective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_pi12_7_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_surjective = (
      premises[
        0
      ].conclusion
    )

    delta_e_exactness = (
      premises[
        1
      ].conclusion
    )

    suspension_surjective = (
      premises[
        2
      ].conclusion
    )

    pi13_13 = TodaPrimaryGroup(
      group_dimension=13,
      sphere_dimension=13,
    )

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    pi12_7 = TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=7,
    )

    if (
      delta_surjective.map
      != TodaDeltaMap(
        source_group=pi13_13,
        target_group=pi11_6,
      )
    ):
      return False

    if (
      delta_e_exactness.window
      != TodaEHPExactnessWindow(
        source_term=pi13_13,
        middle_term=pi11_6,
        target_term=pi12_7,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
      )
    ):
      return False

    return (
      suspension_surjective.map
      == TodaSuspensionMap(
        source_group=pi11_6,
        target_group=pi12_7,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=12,
        sphere_dimension=7,
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "pi_12^7 zero"
    ),
    description=(
      "The concrete Delta map "
      "pi_13^13 to pi_11^6 "
      "is surjective. "
      "By Delta-E exactness this makes "
      "E:pi_11^6 to pi_12^7 "
      "the zero map. "
      "Independently, the concrete "
      "E-H exactness branch and "
      "pi_12^13=0 make the same "
      "suspension map surjective. "
      "A zero map that is surjective "
      "has zero target, hence "
      "pi_12^7=0. "
      "No generic zero-map or "
      "trivial-target solver is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaSurjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
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


def toda_prop59_higher_five_stem_zero_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    source_zero = (
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

    pi12_7 = TodaPrimaryGroup(
      group_dimension=12,
      sphere_dimension=7,
    )

    if (
      source_zero
      != TodaPrimaryGroupZeroStatement(
        group=pi12_7,
      )
    ):
      return False

    suspension_map = (
      isomorphism.map
    )

    structural_source = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=7,
          right=5,
        ),
        sphere_dimension=7,
      )
    )

    if (
      suspension_map.source_group
      != structural_source
    ):
      return False

    target_group = (
      suspension_map.target_group
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

    if (
      target_group
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=5,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    if (
      suspension_map.exponent
      != ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=7,
        ),
      )
    ):
      return False

    return (
      higher_range
      == ScalarGreaterEqualStatement(
        left=n,
        right=7,
      )
    )

  def build_conclusion(
    premises,
  ):
    target_group = (
      premises[
        1
      ].conclusion
      .map
      .target_group
    )

    return TodaPrimaryGroupZeroStatement(
      group=target_group,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "higher five-stem zero transport"
    ),
    description=(
      "Transport the independently "
      "derived zero group pi_12^7 "
      "through the independently derived "
      "Toda (4.5) stable-range "
      "iterated-suspension isomorphism "
      "E^(n-7):pi_12^7 to pi_(n+5)^n. "
      "For n at least 7 this gives "
      "pi_(n+5)^n=0. "
      "No generic isomorphism transport "
      "of zero groups is introduced."
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
          Toda45IsomorphismStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop59_delta_eta11_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_iota11 = (
      premises[
        0
      ].conclusion
    )

    pi10_5_relation = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      delta_iota11.lhs,
      MapApplication,
    ):
      return False

    if (
      delta_iota11.lhs.map
      != EHP_DELTA_MAP
    ):
      return False

    iota_11 = (
      delta_iota11
      .lhs
      .expression
    )

    if not isinstance(
      iota_11,
      HomotopyElement,
    ):
      return False

    if (
      iota_11.dimension
      != 11
      or iota_11.generator
      != GeneratorSymbol(
        family="ι",
        index=11,
      )
    ):
      return False

    nu5_eta8 = (
      delta_iota11.rhs
    )

    if not isinstance(
      nu5_eta8,
      Composition,
    ):
      return False

    nu_5 = (
      nu5_eta8.left
    )

    eta_8 = (
      nu5_eta8.right
    )

    if not isinstance(
      nu_5,
      HomotopyElement,
    ):
      return False

    if (
      nu_5.dimension
      != 5
      or nu_5.source
      != 8
      or nu_5.target
      != 5
      or nu_5.generator
      != GeneratorSymbol(
        family="ν",
        index=5,
      )
    ):
      return False

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    if (
      eta_8.dimension
      != 8
      or eta_8.source
      != 9
      or eta_8.target
      != 8
      or eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    if (
      pi10_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi10_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi10_5_relation.rhs.order
      != 2
    ):
      return False

    nu5_eta8_squared = (
      pi10_5_relation
      .rhs
      .generator
    )

    if not isinstance(
      nu5_eta8_squared,
      Composition,
    ):
      return False

    if (
      nu5_eta8_squared.left
      != nu_5
    ):
      return False

    eta8_squared = (
      nu5_eta8_squared.right
    )

    if not isinstance(
      eta8_squared,
      Composition,
    ):
      return False

    if (
      eta8_squared.left
      != eta_8
    ):
      return False

    eta_9 = (
      eta8_squared.right
    )

    if not isinstance(
      eta_9,
      HomotopyElement,
    ):
      return False

    return (
      eta_9.dimension
      == 9
      and eta_9.source
      == 10
      and eta_9.target
      == 9
      and eta_9.generator
      == GeneratorSymbol(
        family="η",
        index=9,
      )
    )

  def build_conclusion(
    premises,
  ):
    pi10_5_relation = (
      premises[
        1
      ].conclusion
    )

    eta_11 = HomotopyElement(
      name="η₁₁",
      dimension=11,
      source=12,
      target=11,
      generator=GeneratorSymbol(
        family="η",
        index=11,
      ),
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_DELTA_MAP,
        expression=eta_11,
      ),
      rhs=(
        pi10_5_relation
        .rhs
        .generator
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "Delta eta_11"
    ),
    description=(
      "Use the independently derived "
      "Toda Equation (5.10) relation "
      "Delta(iota_11)=nu_5 eta_8 and "
      "the independently derived "
      "pi_10^5 generator "
      "nu_5 eta_8 squared. "
      "For the concrete Proposition 2.5 "
      "composition instance defining "
      "eta_11, derive "
      "Delta(eta_11)=nu_5 eta_8 squared. "
      "The target generator object is "
      "reused directly from the "
      "Phase 70-6 group conclusion. "
      "No generic Delta-composition or "
      "associativity normalizer is added."
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


def toda_prop59_finite_dimensional_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi7_2_relation = (
      premises[
        0
      ].conclusion
    )

    pi8_3_relation = (
      premises[
        1
      ].conclusion
    )

    pi9_4_relation = (
      premises[
        2
      ].conclusion
    )

    pi10_5_relation = (
      premises[
        3
      ].conclusion
    )

    pi11_6_relation = (
      premises[
        4
      ].conclusion
    )

    higher_zero = (
      premises[
        5
      ].conclusion
    )

    higher_range = (
      premises[
        6
      ].conclusion
    )

    if (
      pi7_2_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=2,
      )
    ):
      return False

    if not isinstance(
      pi7_2_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi7_2_relation.rhs.order
      != 2
    ):
      return False

    pi7_2_generator = (
      pi7_2_relation
      .rhs
      .generator
    )

    if not isinstance(
      pi7_2_generator,
      Composition,
    ):
      return False

    eta_2 = (
      pi7_2_generator.left
    )

    nu_prime_eta6 = (
      pi7_2_generator.right
    )

    if not isinstance(
      eta_2,
      HomotopyElement,
    ):
      return False

    if (
      eta_2.dimension
      != 2
      or eta_2.source
      != 3
      or eta_2.target
      != 2
      or eta_2.generator
      != GeneratorSymbol(
        family="η",
        index=2,
      )
    ):
      return False

    if not isinstance(
      nu_prime_eta6,
      Composition,
    ):
      return False

    nu_prime = (
      nu_prime_eta6.left
    )

    eta_6 = (
      nu_prime_eta6.right
    )

    if not isinstance(
      nu_prime,
      HomotopyElement,
    ):
      return False

    if (
      nu_prime.dimension
      != 3
      or nu_prime.source
      != 6
      or nu_prime.target
      != 3
      or nu_prime.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    if not isinstance(
      eta_6,
      HomotopyElement,
    ):
      return False

    if (
      eta_6.dimension
      != 6
      or eta_6.source
      != 7
      or eta_6.target
      != 6
      or eta_6.generator
      != GeneratorSymbol(
        family="η",
        index=6,
      )
    ):
      return False

    if (
      pi8_3_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=3,
      )
    ):
      return False

    if not isinstance(
      pi8_3_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi8_3_relation.rhs.order
      != 2
    ):
      return False

    pi8_3_generator = (
      pi8_3_relation
      .rhs
      .generator
    )

    if not isinstance(
      pi8_3_generator,
      Composition,
    ):
      return False

    if (
      pi8_3_generator.left.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    eta6_squared = (
      pi8_3_generator.right
    )

    if not isinstance(
      eta6_squared,
      Composition,
    ):
      return False

    pi8_eta_6 = (
      eta6_squared.left
    )

    pi8_eta_7 = (
      eta6_squared.right
    )

    if not isinstance(
      pi8_eta_6,
      HomotopyElement,
    ):
      return False

    if not isinstance(
      pi8_eta_7,
      HomotopyElement,
    ):
      return False

    if (
      pi8_eta_6.dimension
      != 6
      or pi8_eta_6.source
      != 7
      or pi8_eta_6.target
      != 6
      or pi8_eta_6.generator
      != GeneratorSymbol(
        family="η",
        index=6,
      )
    ):
      return False

    if (
      pi8_eta_7.dimension
      != 7
      or pi8_eta_7.source
      != 8
      or pi8_eta_7.target
      != 7
      or pi8_eta_7.generator
      != GeneratorSymbol(
        family="η",
        index=7,
      )
    ):
      return False

    if (
      pi9_4_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=4,
      )
    ):
      return False

    if not isinstance(
      pi9_4_relation.rhs,
      DirectSumGroup,
    ):
      return False

    if (
      len(
        pi9_4_relation
        .rhs
        .summands
      )
      != 2
    ):
      return False

    pi9_first = (
      pi9_4_relation
      .rhs
      .summands[
        0
      ]
    )

    pi9_second = (
      pi9_4_relation
      .rhs
      .summands[
        1
      ]
    )

    if not isinstance(
      pi9_first,
      FiniteCyclicGroup,
    ):
      return False

    if not isinstance(
      pi9_second,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi9_first.order
      != 2
      or pi9_second.order
      != 2
    ):
      return False

    nu4_eta7_squared = (
      pi9_first.generator
    )

    if not isinstance(
      nu4_eta7_squared,
      Composition,
    ):
      return False

    nu_4 = (
      nu4_eta7_squared.left
    )

    eta7_squared = (
      nu4_eta7_squared.right
    )

    if not isinstance(
      nu_4,
      HomotopyElement,
    ):
      return False

    if (
      nu_4.dimension
      != 4
      or nu_4.source
      != 7
      or nu_4.target
      != 4
      or nu_4.generator
      != GeneratorSymbol(
        family="ν",
        index=4,
      )
    ):
      return False

    if not isinstance(
      eta7_squared,
      Composition,
    ):
      return False

    eta_7 = (
      eta7_squared.left
    )

    eta_8 = (
      eta7_squared.right
    )

    if not isinstance(
      eta_7,
      HomotopyElement,
    ):
      return False

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    if (
      eta_7.dimension
      != 7
      or eta_7.source
      != 8
      or eta_7.target
      != 7
      or eta_7.generator
      != GeneratorSymbol(
        family="η",
        index=7,
      )
    ):
      return False

    if (
      eta_8.dimension
      != 8
      or eta_8.source
      != 9
      or eta_8.target
      != 8
      or eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    e_nu_prime_eta7_squared = (
      pi9_second.generator
    )

    if not isinstance(
      e_nu_prime_eta7_squared,
      Composition,
    ):
      return False

    if not isinstance(
      e_nu_prime_eta7_squared.left,
      Suspension,
    ):
      return False

    suspended_nu_prime = (
      e_nu_prime_eta7_squared
      .left
      .expression
    )

    if not isinstance(
      suspended_nu_prime,
      HomotopyElement,
    ):
      return False

    if (
      suspended_nu_prime.generator
      != GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    ):
      return False

    second_eta7_squared = (
      e_nu_prime_eta7_squared.right
    )

    if not isinstance(
      second_eta7_squared,
      Composition,
    ):
      return False

    second_eta_7 = (
      second_eta7_squared.left
    )

    second_eta_8 = (
      second_eta7_squared.right
    )

    if not isinstance(
      second_eta_7,
      HomotopyElement,
    ):
      return False

    if not isinstance(
      second_eta_8,
      HomotopyElement,
    ):
      return False

    if (
      second_eta_7.generator
      != GeneratorSymbol(
        family="η",
        index=7,
      )
      or second_eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    if (
      pi10_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi10_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi10_5_relation.rhs.order
      != 2
    ):
      return False

    nu5_eta8_squared = (
      pi10_5_relation
      .rhs
      .generator
    )

    if not isinstance(
      nu5_eta8_squared,
      Composition,
    ):
      return False

    nu_5 = (
      nu5_eta8_squared.left
    )

    eta8_squared = (
      nu5_eta8_squared.right
    )

    if not isinstance(
      nu_5,
      HomotopyElement,
    ):
      return False

    if (
      nu_5.dimension
      != 5
      or nu_5.source
      != 8
      or nu_5.target
      != 5
      or nu_5.generator
      != GeneratorSymbol(
        family="ν",
        index=5,
      )
    ):
      return False

    if not isinstance(
      eta8_squared,
      Composition,
    ):
      return False

    pi10_eta_8 = (
      eta8_squared.left
    )

    pi10_eta_9 = (
      eta8_squared.right
    )

    if not isinstance(
      pi10_eta_8,
      HomotopyElement,
    ):
      return False

    if not isinstance(
      pi10_eta_9,
      HomotopyElement,
    ):
      return False

    if (
      pi10_eta_8.dimension
      != 8
      or pi10_eta_8.source
      != 9
      or pi10_eta_8.target
      != 8
      or pi10_eta_8.generator
      != GeneratorSymbol(
        family="η",
        index=8,
      )
    ):
      return False

    if (
      pi10_eta_9.dimension
      != 9
      or pi10_eta_9.source
      != 10
      or pi10_eta_9.target
      != 9
      or pi10_eta_9.generator
      != GeneratorSymbol(
        family="η",
        index=9,
      )
    ):
      return False

    if (
      pi11_6_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=6,
      )
    ):
      return False

    if not isinstance(
      pi11_6_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    delta_iota13 = (
      pi11_6_relation
      .rhs
      .generator
    )

    if not isinstance(
      delta_iota13,
      MapApplication,
    ):
      return False

    if (
      delta_iota13.map
      != EHP_DELTA_MAP
    ):
      return False

    iota_13 = (
      delta_iota13.expression
    )

    if not isinstance(
      iota_13,
      HomotopyElement,
    ):
      return False

    if (
      iota_13.dimension
      != 13
      or iota_13.generator
      != GeneratorSymbol(
        family="ι",
        index=13,
      )
    ):
      return False

    if not isinstance(
      higher_zero,
      TodaPrimaryGroupZeroStatement,
    ):
      return False

    higher_group = (
      higher_zero.group
    )

    if not isinstance(
      higher_group,
      TodaPrimaryGroup,
    ):
      return False

    n = (
      higher_group
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      higher_group
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=5,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    return (
      higher_range
      == ScalarGreaterEqualStatement(
        left=n,
        right=7,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaProp59FiniteDimensionalStatement(
      pi7_2_group_relation=(
        premises[
          0
        ].conclusion
      ),
      pi8_3_group_relation=(
        premises[
          1
        ].conclusion
      ),
      pi9_4_group_relation=(
        premises[
          2
        ].conclusion
      ),
      pi10_5_group_relation=(
        premises[
          3
        ].conclusion
      ),
      pi11_6_group_relation=(
        premises[
          4
        ].conclusion
      ),
      higher_five_stem_zero=(
        premises[
          5
        ].conclusion
      ),
      higher_range=(
        premises[
          6
        ].conclusion
      ),
      literature_statements=(
        toda_prop59_finite_dimensional_literature_statements()
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.9 "
      "finite-dimensional integration"
    ),
    description=(
      "Integrate the six independently "
      "derived finite-dimensional "
      "Proposition 5.9 branches: "
      "pi_7^2, pi_8^3, pi_9^4, "
      "pi_10^5, pi_11^6, and the "
      "higher five-stem vanishing "
      "pi_(n+5)^n=0 for n at least 7. "
      "All mathematical branches must be "
      "derived by inference; only the "
      "symbolic higher range remains "
      "a structural given premise. "
      "No new homotopy-group calculation, "
      "stable stem assumption, or "
      "generic aggregation framework "
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
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaPrimaryGroupZeroStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


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
class TodaNuFamilyDefinitionStatement:
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


@dataclass(frozen=True)
class TodaIteratedSuspensionInjectiveStatement:
  map: TodaIteratedSuspensionMap


@dataclass(frozen=True)
class TodaProp56Pi8_5QuotientStatement:
  ambient_group: TodaPrimaryGroup
  subobject_map: TodaIteratedSuspensionMap
  quotient_order: int


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


def toda_prop56_pi5_2_eta2_cube_inference_rule():
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

    pi_5_3 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
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

    eta_3_squared = Composition(
      left=eta_3,
      right=eta_4,
    )

    if (
      source_relation.rhs.generator
      != eta_3_squared
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

    eta_3_squared = (
      source_relation
      .rhs
      .generator
    )

    eta_2_cube = Composition(
      left=eta_2,
      right=eta_3_squared,
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_2_cube,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "pi_5^2 eta_2 cube"
    ),
    description=(
      "Use the derived Toda (5.2) "
      "composition isomorphism "
      "eta_2 composed with minus from "
      "pi_i^3 to pi_i^2 together with "
      "the independently derived "
      "Proposition 5.3 relation "
      "pi_5^3=Z/2{eta_3 squared}. "
      "Transport eta_3 squared to "
      "eta_2 composed with eta_3 "
      "squared and derive "
      "pi_5^2=Z/2{eta_2 cubed}."
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


def toda_57_nu_prime_eta6_hopf_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_relation = (
      premises[
        0
      ].conclusion
    )

    eta5_definition = (
      premises[
        1
      ].conclusion
    )

    eta6_definition = (
      premises[
        2
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

    canonical_eta_5 = HomotopyElement(
      name="η₅",
      dimension=5,
      source=6,
      target=5,
      generator=GeneratorSymbol(
        family="η",
        index=5,
      ),
    )

    expected_hopf_relation = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=nu_prime,
      ),
      rhs=canonical_eta_5,
      relation_type=RelationType.EQUALITY,
    )

    if (
      hopf_relation
      != expected_hopf_relation
    ):
      return False

    if (
      eta5_definition.index
      != 5
    ):
      return False

    if (
      eta6_definition.index
      != 6
    ):
      return False

    eta5_definition_element = (
      eta5_definition.element
    )

    if not isinstance(
      eta5_definition_element,
      HomotopyElement,
    ):
      return False

    if (
      eta5_definition_element.dimension
      != 5
    ):
      return False

    if (
      eta5_definition_element.source
      != 6
    ):
      return False

    if (
      eta5_definition_element.target
      != 5
    ):
      return False

    if (
      eta5_definition_element.generator
      != GeneratorSymbol(
        family="η",
        index=5,
      )
    ):
      return False

    eta6_definition_element = (
      eta6_definition.element
    )

    if not isinstance(
      eta6_definition_element,
      HomotopyElement,
    ):
      return False

    if (
      eta6_definition_element.dimension
      != 6
    ):
      return False

    if (
      eta6_definition_element.source
      != 7
    ):
      return False

    if (
      eta6_definition_element.target
      != 6
    ):
      return False

    if (
      eta6_definition_element.generator
      != GeneratorSymbol(
        family="η",
        index=6,
      )
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
      eta5_definition.iterated_suspension
      != IteratedSuspension(
        expression=eta_2,
        exponent=3,
      )
    ):
      return False

    if (
      eta6_definition.iterated_suspension
      != IteratedSuspension(
        expression=eta_2,
        exponent=4,
      )
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    hopf_relation = (
      premises[
        0
      ].conclusion
    )

    nu_prime = (
      hopf_relation
      .lhs
      .expression
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

    eta_5_squared = Composition(
      left=eta_5,
      right=eta_6,
    )

    return Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=Composition(
          left=nu_prime,
          right=eta_6,
        ),
      ),
      rhs=eta_5_squared,
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Equation 5.7 "
      "nu-prime eta_6 Hopf value"
    ),
    description=(
      "Use the independently derived "
      "relation H(nu-prime)=eta_5 "
      "and the concrete eta-family "
      "definitions at indices 5 and 6. "
      "Accept the existing eta-family "
      "constructor names structurally "
      "through dimension and generator "
      "identity, then construct the "
      "canonical Toda notation eta_5 "
      "and eta_6 locally. "
      "The Proposition 2.2 composition "
      "formula gives "
      "H(nu-prime composed with eta_6)"
      "=eta_5 composed with eta_6, "
      "which is eta_5 squared."
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
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaEtaFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_eta3_cube_order_two_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi5_2_relation = (
      premises[
        0
      ].conclusion
    )

    suspension_injective = (
      premises[
        1
      ].conclusion
    )

    pi_5_2 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=2,
    )

    pi_6_3 = TodaPrimaryGroup(
      group_dimension=6,
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

    eta_2_cube = Composition(
      left=eta_2,
      right=Composition(
        left=eta_3,
        right=eta_4,
      ),
    )

    if (
      pi5_2_relation
      != Relation(
        lhs=pi_5_2,
        rhs=FiniteCyclicGroup(
          order=2,
          generator=eta_2_cube,
        ),
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    return (
      suspension_injective.map
      == TodaSuspensionMap(
        source_group=pi_5_2,
        target_group=pi_6_3,
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

    eta_3_cube = Composition(
      left=eta_3,
      right=Composition(
        left=eta_4,
        right=eta_5,
      ),
    )

    return Relation(
      lhs=eta_3_cube,
      rhs=2,
      relation_type=RelationType.ORDER,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "eta_3 cube order two"
    ),
    description=(
      "Phase 65-2 gives "
      "pi_5^2=Z/2{eta_2 cubed}. "
      "Phase 65-3 gives injectivity "
      "of suspension E from pi_5^2 "
      "to pi_6^3. Suspension sends "
      "eta_2 cubed to eta_3 cubed, "
      "so eta_3 cubed has exact "
      "order two."
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
          TodaSuspensionInjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_nu_prime_order_four_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    eta3_cube_order = (
      premises[
        0
      ].conclusion
    )

    double_relation = (
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

    eta_3_cube = Composition(
      left=eta_3,
      right=Composition(
        left=eta_4,
        right=eta_5,
      ),
    )

    if (
      eta3_cube_order
      != Relation(
        lhs=eta_3_cube,
        rhs=2,
        relation_type=RelationType.ORDER,
      )
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

    return (
      double_relation
      == Relation(
        lhs=Multiple(
          coefficient=2,
          expression=nu_prime,
        ),
        rhs=eta_3_cube,
        relation_type=RelationType.EQUALITY,
      )
    )

  def build_conclusion(
    premises,
  ):
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

    return Relation(
      lhs=nu_prime,
      rhs=4,
      relation_type=RelationType.ORDER,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "nu-prime order four"
    ),
    description=(
      "The derived element eta_3 cubed "
      "has exact order two and "
      "Phase 58 gives "
      "2 nu-prime=eta_3 cubed. "
      "Therefore 2 nu-prime is nonzero "
      "and has order two, while "
      "4 nu-prime is zero. Hence "
      "nu-prime has exact order four."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ORDER
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


def toda_prop56_pi6_3_finite_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    nu_prime_order = (
      premises[
        0
      ].conclusion
    )

    membership = (
      premises[
        1
      ].conclusion
    )

    pi5_2_relation = (
      premises[
        2
      ].conclusion
    )

    suspension_injective = (
      premises[
        3
      ].conclusion
    )

    exactness = (
      premises[
        4
      ].conclusion
    )

    hopf_surjective = (
      premises[
        5
      ].conclusion
    )

    pi6_5_relation = (
      premises[
        6
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
      nu_prime_order
      != Relation(
        lhs=nu_prime,
        rhs=4,
        relation_type=RelationType.ORDER,
      )
    ):
      return False

    if (
      membership.element
      != nu_prime
    ):
      return False

    if (
      membership.group_dimension
      != 6
    ):
      return False

    if (
      membership.sphere_dimension
      != 3
    ):
      return False

    pi_5_2 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=2,
    )

    pi_6_3 = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )

    pi_6_5 = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=5,
    )

    if (
      pi5_2_relation.lhs
      != pi_5_2
    ):
      return False

    if not isinstance(
      pi5_2_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi5_2_relation.rhs.order
      != 2
    ):
      return False

    if (
      suspension_injective.map
      != TodaSuspensionMap(
        source_group=pi_5_2,
        target_group=pi_6_3,
      )
    ):
      return False

    window = exactness.window

    if (
      window.source_term
      != pi_5_2
    ):
      return False

    if (
      window.middle_term
      != pi_6_3
    ):
      return False

    if (
      window.target_term
      != pi_6_5
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

    if (
      hopf_surjective.map
      != TodaHopfInvariantMap(
        source_group=pi_6_3,
        target_group=pi_6_5,
      )
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

    return (
      pi6_5_relation
      == Relation(
        lhs=pi_6_5,
        rhs=FiniteCyclicGroup(
          order=2,
          generator=eta_5,
        ),
        relation_type=RelationType.EQUALITY,
      )
    )

  def build_conclusion(
    premises,
  ):
    nu_prime = (
      premises[
        0
      ].conclusion.lhs
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=nu_prime,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "pi_6^3 finite cyclic"
    ),
    description=(
      "Use the E-H exact sequence "
      "pi_5^2 -> pi_6^3 -> pi_6^5. "
      "The source is cyclic of order "
      "two and E is injective, so "
      "Ker(H)=Im(E) has order two. "
      "H is surjective and pi_6^5 "
      "is cyclic of order two, so "
      "pi_6^3 has order four. "
      "The element nu-prime belongs "
      "to pi_6^3 and has exact order "
      "four, hence it generates the "
      "whole group."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ORDER
        ),
      ),
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
        statement_type=(
          TodaSuspensionInjectiveStatement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaHopfInvariantSurjectiveStatement
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


def toda_prop56_pi7_4_decomposition_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda56_statement = (
      premises[
        0
      ].conclusion
    )

    pi6_3_relation = (
      premises[
        1
      ].conclusion
    )

    pi7_7_relation = (
      premises[
        2
      ].conclusion
    )

    decomposition_isomorphism = (
      toda56_statement
      .decomposition_isomorphism
    )

    prop44_isomorphism = (
      decomposition_isomorphism
      .prop44_isomorphism
    )

    decomposition_map = (
      prop44_isomorphism.map
    )

    if not isinstance(
      decomposition_map,
      TodaProp44DecompositionMap,
    ):
      return False

    source_group = (
      decomposition_map.source_group
    )

    target_group = (
      decomposition_map.target_group
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

    if not isinstance(
      target_group,
      TodaPrimaryGroup,
    ):
      return False

    i = (
      target_group
      .group_dimension
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    if (
      target_group
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=4,
      )
    ):
      return False

    if (
      source_group.summands[
        0
      ]
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=-1,
        ),
        sphere_dimension=3,
      )
    ):
      return False

    if (
      source_group.summands[
        1
      ]
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=7,
      )
    ):
      return False

    nu_4 = HomotopyElement(
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
      decomposition_map.alpha
      != nu_4
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=nu_4,
        right=(
          decomposition_map.gamma
        ),
      ),
    )

    if (
      decomposition_map.formula
      != expected_formula
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
      pi6_3_relation
      != Relation(
        lhs=TodaPrimaryGroup(
          group_dimension=6,
          sphere_dimension=3,
        ),
        rhs=FiniteCyclicGroup(
          order=4,
          generator=nu_prime,
        ),
        relation_type=RelationType.EQUALITY,
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

    return (
      pi7_7_relation
      == Relation(
        lhs=TodaPrimaryGroup(
          group_dimension=7,
          sphere_dimension=7,
        ),
        rhs=FreeCyclicGroup(
          generator=iota_7,
        ),
        relation_type=RelationType.EQUALITY,
      )
    )

  def build_conclusion(
    premises,
  ):
    toda56_statement = (
      premises[
        0
      ].conclusion
    )

    decomposition_isomorphism = (
      toda56_statement
      .decomposition_isomorphism
    )

    decomposition_map = (
      decomposition_isomorphism
      .prop44_isomorphism
      .map
    )

    nu_4 = (
      decomposition_map.alpha
    )

    nu_prime = (
      premises[
        1
      ].conclusion
      .rhs
      .generator
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=4,
      ),
      rhs=DirectSumGroup(
        summands=(
          FreeCyclicGroup(
            generator=nu_4,
          ),
          FiniteCyclicGroup(
            order=4,
            generator=Suspension(
              expression=nu_prime,
            ),
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "pi_7^4 decomposition"
    ),
    description=(
      "Specialize the derived Toda "
      "(5.6) decomposition "
      "pi_(i-1)^3 direct sum pi_i^7 "
      "isomorphic to pi_i^4 at i=7. "
      "Use pi_6^3=Z/4{nu-prime} and "
      "pi_7^7=Z{iota_7}. "
      "The first generator maps to "
      "E nu-prime and the identity "
      "generator maps by composition "
      "with nu_4 to nu_4. Therefore "
      "pi_7^4 is Z{nu_4} direct sum "
      "Z/4{E nu-prime}."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda56Nu4DecompositionStatement
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
        proof_rule=ProofRule.GIVEN,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_pi8_5_quotient_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda56_statement = (
      premises[
        0
      ].conclusion
    )

    decomposition_isomorphism = (
      toda56_statement
      .decomposition_isomorphism
    )

    prop44_isomorphism = (
      decomposition_isomorphism
      .prop44_isomorphism
    )

    decomposition_map = (
      prop44_isomorphism.map
    )

    if not isinstance(
      decomposition_map,
      TodaProp44DecompositionMap,
    ):
      return False

    if not isinstance(
      decomposition_map.target_group,
      TodaPrimaryGroup,
    ):
      return False

    i = (
      decomposition_map
      .target_group
      .group_dimension
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    if (
      decomposition_map.target_group
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=4,
      )
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

    if (
      source_group.summands[
        0
      ]
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=-1,
        ),
        sphere_dimension=3,
      )
    ):
      return False

    if (
      source_group.summands[
        1
      ]
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=7,
      )
    ):
      return False

    nu_4 = HomotopyElement(
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
      decomposition_map.alpha
      != nu_4
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=nu_4,
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
    pi_6_3 = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )

    pi_8_5 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )

    e2_map = TodaIteratedSuspensionMap(
      exponent=2,
      source_group=pi_6_3,
      target_group=pi_8_5,
    )

    return TodaProp56Pi8_5QuotientStatement(
      ambient_group=pi_8_5,
      subobject_map=e2_map,
      quotient_order=2,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "pi_8^5 quotient by E^2 pi_6^3"
    ),
    description=(
      "Use the derived Toda (5.6) "
      "nu_4 decomposition result and "
      "the concrete consequence recorded "
      "in the proof of Proposition 5.6: "
      "pi_8^5 modulo E^2 pi_6^3 "
      "is cyclic of order two."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda56Nu4DecompositionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_pi6_3_e2_injective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda56_statement = (
      premises[
        0
      ].conclusion
    )

    decomposition_isomorphism = (
      toda56_statement
      .decomposition_isomorphism
    )

    prop44_isomorphism = (
      decomposition_isomorphism
      .prop44_isomorphism
    )

    decomposition_map = (
      prop44_isomorphism.map
    )

    if not isinstance(
      decomposition_map,
      TodaProp44DecompositionMap,
    ):
      return False

    if not isinstance(
      decomposition_map.target_group,
      TodaPrimaryGroup,
    ):
      return False

    i = (
      decomposition_map
      .target_group
      .group_dimension
    )

    if not isinstance(
      i,
      ScalarSymbol,
    ):
      return False

    if (
      decomposition_map.target_group
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=4,
      )
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

    if (
      source_group.summands[
        0
      ]
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=i,
          right=-1,
        ),
        sphere_dimension=3,
      )
    ):
      return False

    if (
      source_group.summands[
        1
      ]
      != TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=7,
      )
    ):
      return False

    nu_4 = HomotopyElement(
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
      decomposition_map.alpha
      != nu_4
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=nu_4,
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
    return (
      TodaIteratedSuspensionInjectiveStatement(
        map=TodaIteratedSuspensionMap(
          exponent=2,
          source_group=TodaPrimaryGroup(
            group_dimension=6,
            sphere_dimension=3,
          ),
          target_group=TodaPrimaryGroup(
            group_dimension=8,
            sphere_dimension=5,
          ),
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "E^2 pi_6^3 injective"
    ),
    description=(
      "Use the derived Toda (5.6) "
      "nu_4 decomposition result and "
      "the concrete Proposition 5.6 "
      "proof consequence that "
      "E^2 from pi_6^3 to pi_8^5 "
      "is an isomorphism into, hence "
      "injective."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda56Nu4DecompositionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_nu5_double_relation_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    toda55_statement = (
      premises[
        0
      ].conclusion
    )

    nu5_definition = (
      premises[
        1
      ].conclusion
    )

    symbolic_definition = (
      toda55_statement
      .nu_family_definition
    )

    n = symbolic_definition.index

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      toda55_statement.n_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    if (
      symbolic_definition
      != toda_nu_family_definition_statement(
        n
      )
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

    expected_symbolic_double = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=(
          symbolic_definition.element
        ),
      ),
      rhs=IteratedSuspension(
        expression=nu_prime,
        exponent=ScalarSum(
          left=n,
          right=ScalarProduct(
            left=-1,
            right=3,
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      toda55_statement.double_nu_relation
      != expected_symbolic_double
    ):
      return False

    return (
      nu5_definition
      == toda_nu_family_definition_statement(
        5
      )
    )

  def build_conclusion(
    premises,
  ):
    nu5_definition = (
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

    return Relation(
      lhs=Multiple(
        coefficient=2,
        expression=(
          nu5_definition.element
        ),
      ),
      rhs=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "nu_5 double relation"
    ),
    description=(
      "Specialize the independently "
      "derived finite-dimensional "
      "Toda (5.5) nu-family aggregate "
      "to n=5. Together with the "
      "concrete nu_5 family definition, "
      "derive "
      "2 nu_5=E^2 nu-prime. "
      "No generic symbolic theorem "
      "instantiation engine is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda55NuFamilyFiniteDimensionalStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_e2_nu_prime_order_four_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi6_3_relation = (
      premises[
        0
      ].conclusion
    )

    e2_injective = (
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

    pi_6_3 = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )

    pi_8_5 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )

    if (
      pi6_3_relation
      != Relation(
        lhs=pi_6_3,
        rhs=FiniteCyclicGroup(
          order=4,
          generator=nu_prime,
        ),
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    return (
      e2_injective.map
      == TodaIteratedSuspensionMap(
        exponent=2,
        source_group=pi_6_3,
        target_group=pi_8_5,
      )
    )

  def build_conclusion(
    premises,
  ):
    nu_prime = (
      premises[
        0
      ].conclusion
      .rhs
      .generator
    )

    return Relation(
      lhs=IteratedSuspension(
        expression=nu_prime,
        exponent=2,
      ),
      rhs=4,
      relation_type=RelationType.ORDER,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "E^2 nu-prime order four"
    ),
    description=(
      "Phase 65-4 gives "
      "pi_6^3=Z/4{nu-prime}. "
      "Phase 65-6 gives injectivity "
      "of E^2 from pi_6^3 to pi_8^5. "
      "An injective map preserves the "
      "exact order of this concrete "
      "generator, so E^2 nu-prime "
      "has order four. "
      "No generic injective-map "
      "order transport rule is added."
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
          TodaIteratedSuspensionInjectiveStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_nu5_order_eight_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    double_relation = (
      premises[
        0
      ].conclusion
    )

    e2_order = (
      premises[
        1
      ].conclusion
    )

    nu5_definition = (
      premises[
        2
      ].conclusion
    )

    if (
      nu5_definition
      != toda_nu_family_definition_statement(
        5
      )
    ):
      return False

    nu_5 = (
      nu5_definition.element
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

    e2_nu_prime = IteratedSuspension(
      expression=nu_prime,
      exponent=2,
    )

    if (
      double_relation
      != Relation(
        lhs=Multiple(
          coefficient=2,
          expression=nu_5,
        ),
        rhs=e2_nu_prime,
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    return (
      e2_order
      == Relation(
        lhs=e2_nu_prime,
        rhs=4,
        relation_type=RelationType.ORDER,
      )
    )

  def build_conclusion(
    premises,
  ):
    nu5_definition = (
      premises[
        2
      ].conclusion
    )

    return Relation(
      lhs=nu5_definition.element,
      rhs=8,
      relation_type=RelationType.ORDER,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "nu_5 order eight"
    ),
    description=(
      "The concrete Toda (5.5) "
      "specialization gives "
      "2 nu_5=E^2 nu-prime, and "
      "E^2 nu-prime has exact order "
      "four. Therefore twice nu_5 "
      "has order four, so nu_5 has "
      "exact order eight."
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
          RelationType.ORDER
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_pi8_5_finite_cyclic_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    nu5_order = (
      premises[
        0
      ].conclusion
    )

    nu5_definition = (
      premises[
        1
      ].conclusion
    )

    pi6_3_relation = (
      premises[
        2
      ].conclusion
    )

    e2_injective = (
      premises[
        3
      ].conclusion
    )

    quotient_statement = (
      premises[
        4
      ].conclusion
    )

    if (
      nu5_definition
      != toda_nu_family_definition_statement(
        5
      )
    ):
      return False

    nu_5 = (
      nu5_definition.element
    )

    if (
      nu5_order
      != Relation(
        lhs=nu_5,
        rhs=8,
        relation_type=RelationType.ORDER,
      )
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

    pi_6_3 = TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )

    pi_8_5 = TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    )

    if (
      pi6_3_relation
      != Relation(
        lhs=pi_6_3,
        rhs=FiniteCyclicGroup(
          order=4,
          generator=nu_prime,
        ),
        relation_type=RelationType.EQUALITY,
      )
    ):
      return False

    e2_map = TodaIteratedSuspensionMap(
      exponent=2,
      source_group=pi_6_3,
      target_group=pi_8_5,
    )

    if (
      e2_injective.map
      != e2_map
    ):
      return False

    return (
      quotient_statement
      == TodaProp56Pi8_5QuotientStatement(
        ambient_group=pi_8_5,
        subobject_map=e2_map,
        quotient_order=2,
      )
    )

  def build_conclusion(
    premises,
  ):
    nu_5 = (
      premises[
        1
      ].conclusion.element
    )

    return Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=8,
        generator=nu_5,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "pi_8^5 finite cyclic"
    ),
    description=(
      "Phase 65-4 gives "
      "pi_6^3=Z/4{nu-prime}. "
      "Phase 65-6 gives an injective "
      "E^2 map into pi_8^5 and an "
      "order-two quotient "
      "pi_8^5/E^2 pi_6^3. "
      "Hence E^2 pi_6^3 has order "
      "four and pi_8^5 has order "
      "eight. Since nu_5 belongs to "
      "the concrete nu-family target "
      "pi_8^5 and has exact order "
      "eight, it generates the whole "
      "group."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.ORDER
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
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
          TodaIteratedSuspensionInjectiveStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp56Pi8_5QuotientStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_nu5_stable_transport_inference_rule():
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

    nu_5 = HomotopyElement(
      name="ν_5",
      dimension=5,
      source=8,
      target=5,
      generator=GeneratorSymbol(
        family="ν",
        index=5,
      ),
    )

    expected_source_relation = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=8,
        generator=nu_5,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      source_relation
      != expected_source_relation
    ):
      return False

    suspension_map = (
      isomorphism.map
    )

    expected_structural_source = (
      TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=5,
          right=3,
        ),
        sphere_dimension=5,
      )
    )

    if (
      suspension_map.source_group
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
      higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    ):
      return False

    if (
      target_group
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=3,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    expected_exponent = ScalarSum(
      left=n,
      right=ScalarProduct(
        left=-1,
        right=5,
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
      "Toda Proposition 5.6 "
      "nu_5 stable transport"
    ),
    description=(
      "For symbolic n at least 6, "
      "transport the independently "
      "derived group "
      "pi_8^5=Z/8{nu_5} through "
      "the Toda (4.5) iterated "
      "suspension isomorphism "
      "E^(n-5) from pi_8^5 to "
      "pi_(n+3)^n. "
      "The transported target is "
      "cyclic of order eight generated "
      "by E^(n-5) nu_5. "
      "No generic finite-cyclic "
      "transport rule is introduced."
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
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_higher_nu_family_bridge_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    nu5_definition = (
      premises[
        0
      ].conclusion
    )

    nu_n_definition = (
      premises[
        1
      ].conclusion
    )

    higher_range = (
      premises[
        2
      ].conclusion
    )

    if (
      nu5_definition
      != toda_nu_family_definition_statement(
        5
      )
    ):
      return False

    n = (
      nu_n_definition.index
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      nu_n_definition
      != toda_nu_family_definition_statement(
        n
      )
    ):
      return False

    if (
      higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    ):
      return False

    nu_4 = HomotopyElement(
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
      nu5_definition.iterated_suspension
      != IteratedSuspension(
        expression=nu_4,
        exponent=1,
      )
    ):
      return False

    return (
      nu_n_definition.iterated_suspension
      == IteratedSuspension(
        expression=nu_4,
        exponent=ScalarSum(
          left=n,
          right=-4,
        ),
      )
    )

  def build_conclusion(
    premises,
  ):
    nu5_definition = (
      premises[
        0
      ].conclusion
    )

    nu_n_definition = (
      premises[
        1
      ].conclusion
    )

    n = (
      nu_n_definition.index
    )

    return Relation(
      lhs=IteratedSuspension(
        expression=(
          nu5_definition.element
        ),
        exponent=ScalarSum(
          left=n,
          right=ScalarProduct(
            left=-1,
            right=5,
          ),
        ),
      ),
      rhs=(
        nu_n_definition.element
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "higher nu-family bridge"
    ),
    description=(
      "For symbolic n at least 6, "
      "the concrete definition "
      "nu_5=E nu_4 and the symbolic "
      "nu-family definition "
      "nu_n=E^(n-4) nu_4 give the "
      "Toda-specific bridge "
      "E^(n-5) nu_5=nu_n. "
      "No generic iterated-suspension "
      "exponent normalization is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_higher_nu_finite_cyclic_generator_inference_rule():
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

    higher_range = (
      premises[
        2
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
      != 8
    ):
      return False

    n = (
      transported_relation
      .lhs
      .sphere_dimension
    )

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    ):
      return False

    if (
      transported_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=3,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    if (
      transported_relation
      .rhs
      .generator
      != generator_bridge.lhs
    ):
      return False

    expected_definition = (
      toda_nu_family_definition_statement(
        n
      )
    )

    return (
      generator_bridge.rhs
      == expected_definition.element
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
        order=8,
        generator=generator_bridge.rhs,
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "higher nu finite-cyclic "
      "generator bridge"
    ),
    description=(
      "Replace the transported "
      "generator E^(n-5) nu_5 "
      "in the independently derived "
      "order-eight cyclic group "
      "pi_(n+3)^n by the symbolic "
      "nu-family generator nu_n, "
      "using the independently derived "
      "Toda-specific family bridge."
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
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_pi7_3_hopf_surjective_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    equation57 = (
      premises[
        0
      ].conclusion
    )

    prop53 = (
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

    eta_5_squared = Composition(
      left=eta_5,
      right=eta_6,
    )

    expected_equation57 = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=Composition(
          left=nu_prime,
          right=eta_6,
        ),
      ),
      rhs=eta_5_squared,
      relation_type=RelationType.EQUALITY,
    )

    if (
      equation57
      != expected_equation57
    ):
      return False

    higher_relation = (
      prop53
      .higher_eta_squared_group_relation
    )

    higher_range = (
      prop53.higher_range
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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
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

    eta_n_plus_one = HomotopyElement(
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

    return (
      higher_relation
      .rhs
      .generator
      == Composition(
        left=eta_n,
        right=eta_n_plus_one,
      )
    )

  def build_conclusion(
    premises,
  ):
    return TodaHopfInvariantSurjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=TodaPrimaryGroup(
          group_dimension=7,
          sphere_dimension=3,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=7,
          sphere_dimension=5,
        ),
      ),
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "pi_7^3 Hopf surjective"
    ),
    description=(
      "Equation (5.7) gives an element "
      "nu-prime composed with eta_6 "
      "whose Hopf invariant is "
      "eta_5 squared. Proposition 5.3 "
      "gives pi_7^5=Z/2{eta_5 squared}. "
      "Therefore H from pi_7^3 to "
      "pi_7^5 is surjective."
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
          TodaProp53FiniteDimensionalStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_prop56_pi7_5_delta_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_surjective = (
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

    pi_7_3 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=3,
    )

    pi_7_5 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=5,
    )

    pi_5_2 = TodaPrimaryGroup(
      group_dimension=5,
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
      != pi_7_3
    ):
      return False

    if (
      window.middle_term
      != pi_7_5
    ):
      return False

    if (
      window.target_term
      != pi_5_2
    ):
      return False

    return (
      hopf_surjective.map
      == TodaHopfInvariantMap(
        source_group=pi_7_3,
        target_group=pi_7_5,
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
      "Toda Proposition 5.6 "
      "pi_7^5 Delta zero"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_7^3 -> pi_7^5 -> pi_5^2, "
      "surjectivity of H makes Im(H) "
      "all of pi_7^5. Exactness gives "
      "Ker(Delta)=pi_7^5, so Delta "
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


def toda_prop56_pi5_2_suspension_injective_inference_rule():
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

    pi_7_5 = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=5,
    )

    pi_5_2 = TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=2,
    )

    pi_6_3 = TodaPrimaryGroup(
      group_dimension=6,
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
      != pi_7_5
    ):
      return False

    if (
      window.middle_term
      != pi_5_2
    ):
      return False

    if (
      window.target_term
      != pi_6_3
    ):
      return False

    return (
      delta_zero.map
      == TodaDeltaMap(
        source_group=pi_7_5,
        target_group=pi_5_2,
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
      "Toda Proposition 5.6 "
      "pi_5^2 suspension injective"
    ),
    description=(
      "In the concrete exact sequence "
      "pi_7^5 -> pi_5^2 -> pi_6^3, "
      "Delta zero gives Im(Delta)=0. "
      "Exactness therefore gives "
      "Ker(E)=0, so suspension "
      "E:pi_5^2 to pi_6^3 is injective."
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
class TodaLemma510BracketModuloStatement:
  element: Expression
  bracket: TodaBracket
  ambient_group: TodaPrimaryGroup
  modulus: int


@dataclass(frozen=True)
class TodaLemma510HopfBracketContainsStatement:
  bracket: TodaBracket
  value: Expression


@dataclass(frozen=True)
class TodaLemma510BracketPlusSuspensionImageStatement:
  element: Expression
  bracket: TodaBracket
  suspension_map: TodaSuspensionMap


@dataclass(frozen=True)
class TodaLemma510SuspensionImageInDoubleStatement:
  suspension_map: TodaSuspensionMap
  ambient_group: TodaPrimaryGroup
  modulus: int


@dataclass(frozen=True)
class TodaLemma510Nu6OrdinaryCompositionReductionStatement:
  left_element: Expression
  ordinary_right_group: HomotopyGroup
  two_primary_right_group: TodaPrimaryGroup


@dataclass(frozen=True)
class TodaLemma510Nu6OrdinaryCompositionZeroStatement:
  left_element: Expression
  ordinary_right_group: HomotopyGroup


@dataclass(frozen=True)
class TodaLemma510OrdinaryIndeterminacyDoubleStatement:
  bracket: TodaBracket
  ambient_group: HomotopyGroup
  modulus: int


def toda_lemma510_nu6_ordinary_composition_reduction_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop56 = (
      premises[
        0
      ].conclusion
    )

    finite_group = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      prop56,
      TodaProp56FiniteDimensionalStatement,
    ):
      return False

    if not isinstance(
      finite_group,
      FiniteHomotopyGroupStatement,
    ):
      return False

    if (
      finite_group.group
      != HomotopyGroup(
        group_dimension=11,
        sphere_dimension=9,
      )
    ):
      return False

    higher_relation = (
      prop56
      .higher_nu_group_relation
    )

    higher_range = (
      prop56
      .higher_range
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
      != 8
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
      higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    ):
      return False

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=3,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    nu_n = (
      higher_relation
      .rhs
      .generator
    )

    if not isinstance(
      nu_n,
      HomotopyElement,
    ):
      return False

    return (
      nu_n.generator
      == GeneratorSymbol(
        family="ν",
        index=n,
      )
    )

  def build_conclusion(
    premises,
  ):
    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
    )

    return (
      TodaLemma510Nu6OrdinaryCompositionReductionStatement(
        left_element=nu_6,
        ordinary_right_group=HomotopyGroup(
          group_dimension=11,
          sphere_dimension=9,
        ),
        two_primary_right_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=9,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "nu_6 ordinary composition "
      "primary reduction"
    ),
    description=(
      "Use Toda Proposition 5.6 to "
      "recognize nu_6 as a 2-primary "
      "element and Serre (4.2) to know "
      "that pi_11(S^9) is finite. "
      "By the primary-composition "
      "principle reflected in Toda "
      "Lemma 4.3 / (4.7), odd-primary "
      "summands of pi_11(S^9) vanish "
      "after left composition by nu_6. "
      "Therefore "
      "nu_6 composed with pi_11(S^9) "
      "equals nu_6 composed with its "
      "2-primary component pi_11^9. "
      "This is a composition-level "
      "statement, not an equality "
      "pi_11(S^9)=pi_11^9."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp56FiniteDimensionalStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          FiniteHomotopyGroupStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma510_nu6_ordinary_composition_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    reduction = (
      premises[
        0
      ].conclusion
    )

    prop53 = (
      premises[
        1
      ].conclusion
    )

    nu6_eta9_zero = (
      premises[
        2
      ].conclusion
    )

    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
    )

    if (
      reduction
      != TodaLemma510Nu6OrdinaryCompositionReductionStatement(
        left_element=nu_6,
        ordinary_right_group=HomotopyGroup(
          group_dimension=11,
          sphere_dimension=9,
        ),
        two_primary_right_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=9,
        ),
      )
    ):
      return False

    higher_relation = (
      prop53
      .higher_eta_squared_group_relation
    )

    higher_range = (
      prop53
      .higher_range
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

    if (
      higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=2,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    eta_n_squared = (
      higher_relation
      .rhs
      .generator
    )

    if not isinstance(
      eta_n_squared,
      Composition,
    ):
      return False

    if (
      nu6_eta9_zero.relation_type
      != RelationType.ZERO
    ):
      return False

    if (
      nu6_eta9_zero.rhs
      != Zero()
    ):
      return False

    if not isinstance(
      nu6_eta9_zero.lhs,
      Composition,
    ):
      return False

    zero_nu = (
      nu6_eta9_zero
      .lhs
      .left
    )

    zero_eta = (
      nu6_eta9_zero
      .lhs
      .right
    )

    if (
      zero_nu
      != nu_6
    ):
      return False

    if not isinstance(
      zero_eta,
      HomotopyElement,
    ):
      return False

    return (
      zero_eta.generator
      == GeneratorSymbol(
        family="η",
        index=9,
      )
    )

  def build_conclusion(
    premises,
  ):
    reduction = (
      premises[
        0
      ].conclusion
    )

    return (
      TodaLemma510Nu6OrdinaryCompositionZeroStatement(
        left_element=(
          reduction.left_element
        ),
        ordinary_right_group=(
          reduction.ordinary_right_group
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "nu_6 ordinary composition zero"
    ),
    description=(
      "Use Proposition 5.3 at n=9: "
      "pi_11^9 is Z/2 generated by "
      "eta_9 squared. "
      "The independently derived "
      "Phase 68 relation nu_6 eta_9=0 "
      "therefore kills the generator "
      "eta_9 squared. "
      "Together with the ordinary-to-"
      "2-primary composition reduction, "
      "derive "
      "nu_6 composed with pi_11(S^9)=0."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma510Nu6OrdinaryCompositionReductionStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp53FiniteDimensionalStatement
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


def toda_lemma510_eta9_two_iota10_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop51 = (
      premises[
        0
      ].conclusion
    )

    higher_relation = (
      prop51
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

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=1,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    eta_n = (
      higher_relation
      .rhs
      .generator
    )

    if not isinstance(
      eta_n,
      HomotopyElement,
    ):
      return False

    return (
      eta_n.generator
      == GeneratorSymbol(
        family="η",
        index=n,
      )
    )

  def build_conclusion(
    premises,
  ):
    eta_9 = (
      toda_eta_family_definition_statement(
        9
      ).element
    )

    iota_10 = HomotopyElement(
      name="ι_10",
      dimension=10,
      generator=GeneratorSymbol(
        family="ι",
        index=10,
      ),
    )

    return Relation(
      lhs=Composition(
        left=eta_9,
        right=Multiple(
          coefficient=2,
          expression=iota_10,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "eta_9 two iota_10 zero"
    ),
    description=(
      "Specialize the independently "
      "derived Proposition 5.1 relation "
      "pi_(n+1)^n=Z/2{eta_n} to n=9. "
      "Therefore 2 eta_9=0, equivalently "
      "eta_9 composed with 2 iota_10=0. "
      "This replaces the former GIVEN "
      "second zero-composition premise."
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


def toda_lemma510_ordinary_indeterminacy_double_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    ordinary_zero = (
      premises[
        0
      ].conclusion
    )

    nu6_eta9_zero = (
      premises[
        1
      ].conclusion
    )

    eta9_two_iota10_zero = (
      premises[
        2
      ].conclusion
    )

    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
    )

    eta_9 = (
      toda_eta_family_definition_statement(
        9
      ).element
    )

    if (
      ordinary_zero
      != TodaLemma510Nu6OrdinaryCompositionZeroStatement(
        left_element=nu_6,
        ordinary_right_group=HomotopyGroup(
          group_dimension=11,
          sphere_dimension=9,
        ),
      )
    ):
      return False

    expected_first_zero = Relation(
      lhs=Composition(
        left=nu_6,
        right=eta_9,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      nu6_eta9_zero
      != expected_first_zero
    ):
      return False

    iota_10 = HomotopyElement(
      name="ι_10",
      dimension=10,
      generator=GeneratorSymbol(
        family="ι",
        index=10,
      ),
    )

    expected_second_zero = Relation(
      lhs=Composition(
        left=eta_9,
        right=Multiple(
          coefficient=2,
          expression=iota_10,
        ),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      eta9_two_iota10_zero
      == expected_second_zero
    )

  def build_conclusion(
    premises,
  ):
    ordinary_zero = (
      premises[
        0
      ].conclusion
    )

    nu_6 = (
      ordinary_zero
      .left_element
    )

    eta_9 = (
      toda_eta_family_definition_statement(
        9
      ).element
    )

    iota_10 = HomotopyElement(
      name="ι_10",
      dimension=10,
      generator=GeneratorSymbol(
        family="ι",
        index=10,
      ),
    )

    bracket = TodaBracket(
      first=nu_6,
      second=eta_9,
      third=Multiple(
        coefficient=2,
        expression=iota_10,
      ),
    )

    return (
      TodaLemma510OrdinaryIndeterminacyDoubleStatement(
        bracket=bracket,
        ambient_group=HomotopyGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
        modulus=2,
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "ordinary indeterminacy double"
    ),
    description=(
      "For the ordinary Toda bracket "
      "{nu_6, eta_9, 2 iota_10}, "
      "the indeterminacy is "
      "nu_6 composed with pi_11(S^9) "
      "+ pi_11(S^6) composed with "
      "2 iota_11. "
      "The first summand is independently "
      "derived to be zero. "
      "The second summand is exactly "
      "2 pi_11(S^6). "
      "Therefore the indeterminacy is "
      "2 pi_11(S^6). "
      "Toda (4.7) is used only as the "
      "primary-composition reference; "
      "this rule does not identify "
      "ordinary and 2-primary groups."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma510Nu6OrdinaryCompositionZeroStatement
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


@dataclass(frozen=True)
class TodaLemma510OrdinarySuspensionImageFiniteStatement:
  suspension_map: MapSymbol
  source_group: HomotopyGroup
  target_group: HomotopyGroup


@dataclass(frozen=True)
class TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement:
  suspension_map: MapSymbol
  source_group: HomotopyGroup
  target_group: HomotopyGroup


@dataclass(frozen=True)
class TodaLemma510OrdinarySuspensionImageInDoubleStatement:
  suspension_map: MapSymbol
  source_group: HomotopyGroup
  target_group: HomotopyGroup
  modulus: int


def toda_lemma510_indeterminacy_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop53 = (
      premises[
        0
      ].conclusion
    )

    nu6_eta9_zero = (
      premises[
        1
      ].conclusion
    )

    pi11_6_relation = (
      premises[
        2
      ].conclusion
    )

    if not isinstance(
      prop53,
      TodaProp53FiniteDimensionalStatement,
    ):
      return False

    if not isinstance(
      nu6_eta9_zero,
      Relation,
    ):
      return False

    if (
      nu6_eta9_zero.relation_type
      != RelationType.ZERO
    ):
      return False

    if (
      nu6_eta9_zero.rhs
      != Zero()
    ):
      return False

    if not isinstance(
      nu6_eta9_zero.lhs,
      Composition,
    ):
      return False

    nu_6 = (
      nu6_eta9_zero
      .lhs
      .left
    )

    eta_9 = (
      nu6_eta9_zero
      .lhs
      .right
    )

    if not isinstance(
      nu_6,
      HomotopyElement,
    ):
      return False

    if (
      nu_6.generator
      != GeneratorSymbol(
        family="ν",
        index=6,
      )
    ):
      return False

    if not isinstance(
      eta_9,
      HomotopyElement,
    ):
      return False

    if (
      eta_9.generator
      != GeneratorSymbol(
        family="η",
        index=9,
      )
    ):
      return False

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    if (
      pi11_6_relation.lhs
      != pi11_6
    ):
      return False

    if not isinstance(
      pi11_6_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    delta_iota13 = (
      pi11_6_relation
      .rhs
      .generator
    )

    if not isinstance(
      delta_iota13,
      MapApplication,
    ):
      return False

    if (
      delta_iota13.map
      != EHP_DELTA_MAP
    ):
      return False

    iota_13 = (
      delta_iota13
      .expression
    )

    if not isinstance(
      iota_13,
      HomotopyElement,
    ):
      return False

    if (
      iota_13.generator
      != GeneratorSymbol(
        family="ι",
        index=13,
      )
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    nu6_eta9_zero = (
      premises[
        1
      ].conclusion
    )

    pi11_6_relation = (
      premises[
        2
      ].conclusion
    )

    nu_6 = (
      nu6_eta9_zero
      .lhs
      .left
    )

    eta_9 = (
      nu6_eta9_zero
      .lhs
      .right
    )

    iota_10 = HomotopyElement(
      name="ι_10",
      dimension=10,
      generator=GeneratorSymbol(
        family="ι",
        index=10,
      ),
    )

    bracket = TodaBracket(
      first=nu_6,
      second=eta_9,
      third=Multiple(
        coefficient=2,
        expression=iota_10,
      ),
    )

    delta_iota13 = (
      pi11_6_relation
      .rhs
      .generator
    )

    return (
      Toda54IndeterminacyGeneratorStatement(
        bracket=bracket,
        generator=Multiple(
          coefficient=2,
          expression=delta_iota13,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "indeterminacy reduction"
    ),
    description=(
      "Use the finite-dimensional "
      "Proposition 5.3 result, the "
      "independently derived relation "
      "nu_6 composed with eta_9 = 0, "
      "and pi_11(S^6)=Z{Delta iota_13}. "
      "The Toda (4.7) indeterminacy "
      "nu_6 composed with pi_11(S^9) "
      "plus 2 pi_11(S^6) therefore "
      "reduces to the subgroup generated "
      "by 2 Delta(iota_13). "
      "No generic Toda-bracket coset "
      "algebra is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp53FiniteDimensionalStatement
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
          RelationType.EQUALITY
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma510_suspension_image_in_double_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi10_5_relation = (
      premises[
        0
      ].conclusion
    )

    pi11_6_relation = (
      premises[
        1
      ].conclusion
    )

    pi10_5 = TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=5,
    )

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    if (
      pi10_5_relation.lhs
      != pi10_5
    ):
      return False

    if not isinstance(
      pi10_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi10_5_relation.rhs.order
      != 2
    ):
      return False

    if (
      pi11_6_relation.lhs
      != pi11_6
    ):
      return False

    if not isinstance(
      pi11_6_relation.rhs,
      FreeCyclicGroup,
    ):
      return False

    delta_iota13 = (
      pi11_6_relation
      .rhs
      .generator
    )

    if not isinstance(
      delta_iota13,
      MapApplication,
    ):
      return False

    if (
      delta_iota13.map
      != EHP_DELTA_MAP
    ):
      return False

    return (
      isinstance(
        delta_iota13.expression,
        HomotopyElement,
      )
      and delta_iota13.expression.generator
      == GeneratorSymbol(
        family="ι",
        index=13,
      )
    )

  def build_conclusion(
    premises,
  ):
    return (
      TodaLemma510SuspensionImageInDoubleStatement(
        suspension_map=TodaSuspensionMap(
          source_group=TodaPrimaryGroup(
            group_dimension=10,
            sphere_dimension=5,
          ),
          target_group=TodaPrimaryGroup(
            group_dimension=11,
            sphere_dimension=6,
          ),
        ),
        ambient_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
        modulus=2,
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "suspension image in double subgroup"
    ),
    description=(
      "Use the independently derived "
      "pi_10(S^5)=Z/2 result and "
      "pi_11(S^6)=Z{Delta iota_13}. "
      "The image of the concrete "
      "suspension homomorphism from the "
      "finite order-two source to the "
      "free cyclic target is zero, hence "
      "it is contained in "
      "2 pi_11(S^6). "
      "This is a theorem-specific "
      "finite-dimensional consequence, "
      "not a generic finite-subgroup "
      "solver."
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


def toda_lemma510_ordinary_suspension_image_finite_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    finite_group = (
      premises[
        0
      ].conclusion
    )

    if not isinstance(
      finite_group,
      FiniteHomotopyGroupStatement,
    ):
      return False

    return (
      finite_group.group
      == HomotopyGroup(
        group_dimension=10,
        sphere_dimension=5,
      )
    )

  def build_conclusion(
    premises,
  ):
    finite_group = (
      premises[
        0
      ].conclusion
    )

    return (
      TodaLemma510OrdinarySuspensionImageFiniteStatement(
        suspension_map=EHP_E_MAP,
        source_group=finite_group.group,
        target_group=HomotopyGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "ordinary suspension image finite"
    ),
    description=(
      "Use the independently derived "
      "Serre (4.2) finiteness of "
      "pi_10(S^5). "
      "The image of the suspension "
      "homomorphism "
      "E: pi_10(S^5) -> pi_11(S^6) "
      "is therefore finite. "
      "This rule records only the "
      "concrete finite-image consequence "
      "needed for Toda Lemma 5.10."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          FiniteHomotopyGroupStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma510_ordinary_suspension_image_two_primary_zero_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi10_5_relation = (
      premises[
        0
      ].conclusion
    )

    suspension_zero = (
      premises[
        1
      ].conclusion
    )

    if not isinstance(
      pi10_5_relation,
      Relation,
    ):
      return False

    if (
      pi10_5_relation.relation_type
      != RelationType.EQUALITY
    ):
      return False

    if (
      pi10_5_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=5,
      )
    ):
      return False

    if not isinstance(
      pi10_5_relation.rhs,
      FiniteCyclicGroup,
    ):
      return False

    if (
      pi10_5_relation.rhs.order
      != 2
    ):
      return False

    generator = (
      pi10_5_relation
      .rhs
      .generator
    )

    expected_suspension_zero = Relation(
      lhs=Suspension(
        expression=generator,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    return (
      suspension_zero
      == expected_suspension_zero
    )

  def build_conclusion(
    premises,
  ):
    return (
      TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement(
        suspension_map=EHP_E_MAP,
        source_group=HomotopyGroup(
          group_dimension=10,
          sphere_dimension=5,
        ),
        target_group=HomotopyGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "ordinary suspension image "
      "two-primary zero"
    ),
    description=(
      "Use the independently derived "
      "pi_10^5=Z/2{nu_5 eta_8^2} "
      "and E(nu_5 eta_8^2)=0. "
      "Since pi_10^5 is the concrete "
      "2-primary component of "
      "pi_10(S^5), the suspension image "
      "of that 2-primary component is "
      "zero. "
      "This is the narrow ordinary/"
      "2-primary bridge needed for "
      "Toda Lemma 5.10."
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
          RelationType.ZERO
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma510_ordinary_suspension_image_in_double_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    finite_image = (
      premises[
        0
      ].conclusion
    )

    two_primary_zero = (
      premises[
        1
      ].conclusion
    )

    expected_source = HomotopyGroup(
      group_dimension=10,
      sphere_dimension=5,
    )

    expected_target = HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    if (
      finite_image.suspension_map
      != EHP_E_MAP
    ):
      return False

    if (
      two_primary_zero.suspension_map
      != EHP_E_MAP
    ):
      return False

    if (
      finite_image.source_group
      != expected_source
    ):
      return False

    if (
      two_primary_zero.source_group
      != expected_source
    ):
      return False

    if (
      finite_image.target_group
      != expected_target
    ):
      return False

    if (
      two_primary_zero.target_group
      != expected_target
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    finite_image = (
      premises[
        0
      ].conclusion
    )

    return (
      TodaLemma510OrdinarySuspensionImageInDoubleStatement(
        suspension_map=finite_image.suspension_map,
        source_group=finite_image.source_group,
        target_group=finite_image.target_group,
        modulus=2,
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "ordinary suspension image "
      "in double subgroup"
    ),
    description=(
      "Let I=E pi_10(S^5). "
      "The independently derived Serre "
      "branch shows that I is finite. "
      "The independently derived "
      "2-primary branch shows that "
      "the 2-primary component of I "
      "is zero. "
      "Therefore I has odd order. "
      "Multiplication by 2 is an "
      "automorphism of the finite "
      "odd-order group I, so I=2I. "
      "Hence "
      "E pi_10(S^5) is contained in "
      "2 pi_11(S^6). "
      "No generic primary-decomposition "
      "or finite-group image solver "
      "is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma510OrdinarySuspensionImageFiniteStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma510_modulo_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    core = (
      premises[
        0
      ].conclusion
    )

    indeterminacy = (
      premises[
        1
      ].conclusion
    )

    image_containment = (
      premises[
        2
      ].conclusion
    )

    if (
      core.bracket
      != indeterminacy.bracket
    ):
      return False

    if (
      core.suspension_map
      != image_containment.suspension_map
    ):
      return False

    if (
      image_containment.modulus
      != 2
    ):
      return False

    pi11_6 = TodaPrimaryGroup(
      group_dimension=11,
      sphere_dimension=6,
    )

    if (
      image_containment.ambient_group
      != pi11_6
    ):
      return False

    generator = (
      indeterminacy
      .generator
    )

    if not isinstance(
      generator,
      Multiple,
    ):
      return False

    if (
      generator.coefficient
      != 2
    ):
      return False

    if not isinstance(
      generator.expression,
      MapApplication,
    ):
      return False

    if (
      generator.expression.map
      != EHP_DELTA_MAP
    ):
      return False

    if (
      core.element
      != generator.expression
    ):
      return False

    return True

  def build_conclusion(
    premises,
  ):
    core = (
      premises[
        0
      ].conclusion
    )

    image_containment = (
      premises[
        2
      ].conclusion
    )

    return (
      TodaLemma510BracketModuloStatement(
        element=core.element,
        bracket=core.bracket,
        ambient_group=(
          image_containment
          .ambient_group
        ),
        modulus=(
          image_containment
          .modulus
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "modulo indeterminacy integration"
    ),
    description=(
      "Combine the Phase 72-3 result "
      "Delta(iota_13) in the bracket "
      "plus E pi_10(S^5), the derived "
      "bracket indeterminacy "
      "2 pi_11(S^6), and containment "
      "of the suspension image in that "
      "double subgroup. "
      "Derive the concrete Toda "
      "Lemma 5.10 modulo statement. "
      "No generic coset or quotient "
      "inference framework is added."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma510BracketPlusSuspensionImageStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda54IndeterminacyGeneratorStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma510SuspensionImageInDoubleStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_lemma510_hopf_bracket_contains_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    bracket_defined = (
      premises[
        0
      ].conclusion
    )

    delta_iota11_relation = (
      premises[
        1
      ].conclusion
    )

    nu_6 = (
      toda_nu_family_definition_statement(
        6
      ).element
    )

    eta_9 = (
      toda_eta_family_definition_statement(
        9
      ).element
    )

    iota_10 = HomotopyElement(
      name="ι_10",
      dimension=10,
      generator=GeneratorSymbol(
        family="ι",
        index=10,
      ),
    )

    expected_bracket = TodaBracket(
      first=nu_6,
      second=eta_9,
      third=Multiple(
        coefficient=2,
        expression=iota_10,
      ),
    )

    if (
      bracket_defined.bracket
      != expected_bracket
    ):
      return False

    if not isinstance(
      delta_iota11_relation,
      Relation,
    ):
      return False

    if (
      delta_iota11_relation
      .relation_type
      != RelationType.EQUALITY
    ):
      return False

    if not isinstance(
      delta_iota11_relation.lhs,
      MapApplication,
    ):
      return False

    if (
      delta_iota11_relation
      .lhs
      .map
      != EHP_DELTA_MAP
    ):
      return False

    iota_11 = (
      delta_iota11_relation
      .lhs
      .expression
    )

    if not isinstance(
      iota_11,
      HomotopyElement,
    ):
      return False

    if (
      iota_11.dimension
      != 11
    ):
      return False

    if (
      iota_11.generator
      != GeneratorSymbol(
        family="ι",
        index=11,
      )
    ):
      return False

    delta_value = (
      delta_iota11_relation
      .rhs
    )

    if not isinstance(
      delta_value,
      Composition,
    ):
      return False

    nu_5 = (
      delta_value.left
    )

    eta_8 = (
      delta_value.right
    )

    if not isinstance(
      nu_5,
      HomotopyElement,
    ):
      return False

    if (
      nu_5.generator
      != GeneratorSymbol(
        family="ν",
        index=5,
      )
    ):
      return False

    if not isinstance(
      eta_8,
      HomotopyElement,
    ):
      return False

    return (
      eta_8.generator
      == GeneratorSymbol(
        family="η",
        index=8,
      )
    )

  def build_conclusion(
    premises,
  ):
    bracket_defined = (
      premises[
        0
      ].conclusion
    )

    delta_iota11_relation = (
      premises[
        1
      ].conclusion
    )

    iota_11 = (
      delta_iota11_relation
      .lhs
      .expression
    )

    return (
      TodaLemma510HopfBracketContainsStatement(
        bracket=(
          bracket_defined
          .bracket
        ),
        value=Multiple(
          coefficient=2,
          expression=iota_11,
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "Hopf bracket consequence"
    ),
    description=(
      "For the defined bracket "
      "{nu_6, eta_9, 2 iota_10}, "
      "reuse the independently derived "
      "Toda (5.10) relation "
      "Delta(iota_11)=nu_5 eta_8 "
      "and apply the concrete "
      "Proposition 2.6 consequence used "
      "in Toda Lemma 5.10. "
      "Derive that the Hopf image of the "
      "bracket contains 2 iota_11. "
      "The nu_5 and eta_8 factors are "
      "recognized by their generator "
      "identities rather than by "
      "reconstructing canonical display "
      "objects. "
      "No generic Hopf-of-bracket "
      "calculus or global generator "
      "normalization is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaBracketDefinedStatement
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


def toda_lemma510_exactness_core_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    hopf_bracket = (
      premises[
        0
      ].conclusion
    )

    hopf_delta = (
      premises[
        1
      ].conclusion
    )

    exactness = (
      premises[
        2
      ].conclusion
    )

    iota_11 = HomotopyElement(
      name="ι_11",
      dimension=11,
      generator=GeneratorSymbol(
        family="ι",
        index=11,
      ),
    )

    expected_hopf_value = Multiple(
      coefficient=2,
      expression=iota_11,
    )

    if (
      hopf_bracket.value
      != expected_hopf_value
    ):
      return False

    if (
      hopf_delta.positive_value
      != expected_hopf_value
    ):
      return False

    delta_iota13 = (
      hopf_delta
      .argument
    )

    if not isinstance(
      delta_iota13,
      MapApplication,
    ):
      return False

    if (
      delta_iota13.map
      != EHP_DELTA_MAP
    ):
      return False

    iota_13 = (
      delta_iota13
      .expression
    )

    if not isinstance(
      iota_13,
      HomotopyElement,
    ):
      return False

    if (
      iota_13.dimension
      != 13
    ):
      return False

    if (
      iota_13.generator
      != GeneratorSymbol(
        family="ι",
        index=13,
      )
    ):
      return False

    expected_window = (
      TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=5,
        ),
        middle_term=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
        target_term=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=11,
        ),
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
      )
    )

    return (
      exactness.window
      == expected_window
    )

  def build_conclusion(
    premises,
  ):
    hopf_bracket = (
      premises[
        0
      ].conclusion
    )

    hopf_delta = (
      premises[
        1
      ].conclusion
    )

    return (
      TodaLemma510BracketPlusSuspensionImageStatement(
        element=(
          hopf_delta
          .argument
        ),
        bracket=(
          hopf_bracket
          .bracket
        ),
        suspension_map=(
          TodaSuspensionMap(
            source_group=TodaPrimaryGroup(
              group_dimension=10,
              sphere_dimension=5,
            ),
            target_group=TodaPrimaryGroup(
              group_dimension=11,
              sphere_dimension=6,
            ),
          )
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.10 "
      "E-H exactness core"
    ),
    description=(
      "Toda Lemma 5.10 has "
      "H{nu_6, eta_9, 2 iota_10} "
      "containing 2 iota_11, while "
      "H(Delta(iota_13)) equals "
      "plus or minus 2 iota_11. "
      "Using exactness of "
      "pi_10(S^5) -> pi_11(S^6) "
      "-> pi_11(S^11), derive the "
      "concrete conclusion that "
      "Delta(iota_13) lies in the "
      "Toda bracket plus the suspension "
      "image E pi_10(S^5). "
      "No generic preimage, coset, or "
      "image algebra is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma510HopfBracketContainsStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp27HopfInvariantUpToSignStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaProp42ExactnessStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


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


@dataclass(frozen=True)
class Toda56Nu4Prop44SpecializationStatement:
  lemma54_statement: TodaLemma54Statement
  n: int
  alpha: HomotopyElement
  membership: TodaPrimaryGroupMembershipStatement
  hopf_relation: Relation


@dataclass(frozen=True)
class Toda56Nu4DecompositionIsomorphismStatement:
  prop44_isomorphism: TodaProp44IsomorphismStatement


@dataclass(frozen=True)
class Toda56Nu4DecompositionStatement:
  decomposition_isomorphism: (
    Toda56Nu4DecompositionIsomorphismStatement
  )
  lemma54_statement: TodaLemma54Statement
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


def toda_56_nu4_decomposition_literature_statements():
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
        label="Toda (5.6)",
        locator="Equation (5.6)",
        **toda_reference,
      ),
      statement=(
        "The map "
        "(α,β)↦Eα+ν₄∘β gives an "
        "isomorphism "
        "π_(i-1)^3⊕π_i^7≅π_i^4."
      ),
    ),
  )


def toda_56_nu4_decomposition_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    decomposition_statement = (
      premises[
        0
      ].conclusion
    )

    lemma54_statement = (
      premises[
        1
      ].conclusion
    )

    prop44_isomorphism = (
      decomposition_statement
      .prop44_isomorphism
    )

    decomposition_map = (
      prop44_isomorphism.map
    )

    nu_4 = HomotopyElement(
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
      lemma54_statement.nu4
      != nu_4
    ):
      return False

    if (
      decomposition_map.alpha
      != nu_4
    ):
      return False

    if (
      decomposition_map.alpha
      != lemma54_statement.nu4
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
      != 4
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

    expected_target_group = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=4,
      )
    )

    if (
      target_group
      != expected_target_group
    ):
      return False

    source_group = (
      decomposition_map.source_group
    )

    expected_source_group = DirectSumGroup(
      summands=(
        TodaPrimaryGroup(
          group_dimension=ScalarSum(
            left=i,
            right=-1,
          ),
          sphere_dimension=3,
        ),
        TodaPrimaryGroup(
          group_dimension=i,
          sphere_dimension=7,
        ),
      ),
    )

    if (
      source_group
      != expected_source_group
    ):
      return False

    expected_formula = Sum(
      left=Suspension(
        expression=(
          decomposition_map.beta
        ),
      ),
      right=Composition(
        left=nu_4,
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
    return (
      Toda56Nu4DecompositionStatement(
        decomposition_isomorphism=(
          premises[
            0
          ].conclusion
        ),
        lemma54_statement=(
          premises[
            1
          ].conclusion
        ),
        literature_statements=(
          toda_56_nu4_decomposition_literature_statements()
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda (5.6) "
      "nu_4 decomposition integration"
    ),
    description=(
      "Integrate the derived Toda "
      "(5.6) decomposition "
      "isomorphism semantics with the "
      "independently derived Toda "
      "Lemma 5.4 nu_4 provenance. "
      "The map "
      "(alpha,beta) -> "
      "E(alpha)+nu_4 composed with beta "
      "gives an isomorphism from "
      "pi_(i-1)^3 direct sum pi_i^7 "
      "to pi_i^4. "
      "Direct Toda (5.6) literature "
      "is stored on this aggregate, "
      "while Lemma 5.4 literature "
      "remains inherited through the "
      "nested lemma54 statement."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda56Nu4DecompositionIsomorphismStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Statement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_56_nu4_prop44_specialization_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    lemma54_statement = (
      premises[
        0
      ].conclusion
    )

    nu_4 = HomotopyElement(
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
      lemma54_statement.nu4
      != nu_4
    ):
      return False

    expected_membership = (
      HomotopyGroupMembershipStatement(
        element=nu_4,
        group_dimension=7,
        sphere_dimension=4,
      )
    )

    if (
      lemma54_statement.membership
      != expected_membership
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

    expected_hopf_relation = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=nu_4,
      ),
      rhs=iota_7,
      relation_type=RelationType.EQUALITY,
    )

    return (
      lemma54_statement.hopf_relation
      == expected_hopf_relation
    )

  def build_conclusion(
    premises,
  ):
    lemma54_statement = (
      premises[
        0
      ].conclusion
    )

    nu_4 = (
      lemma54_statement.nu4
    )

    return (
      Toda56Nu4Prop44SpecializationStatement(
        lemma54_statement=(
          lemma54_statement
        ),
        n=4,
        alpha=nu_4,
        membership=(
          TodaPrimaryGroupMembershipStatement(
            element=nu_4,
            group=TodaPrimaryGroup(
              group_dimension=7,
              sphere_dimension=4,
            ),
          )
        ),
        hopf_relation=(
          lemma54_statement
          .hopf_relation
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda (5.6) "
      "nu_4 Proposition 4.4 "
      "specialization premises"
    ),
    description=(
      "The independently derived "
      "Toda Lemma 5.4 statement gives "
      "nu_4 in pi_7^4 and "
      "H(nu_4)=iota_7. "
      "Record these as the concrete "
      "n=4, alpha=nu_4 premises needed "
      "for the Proposition 4.4 "
      "specialization used in "
      "Toda (5.6)."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Statement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_56_nu4_prop44_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    specialization = (
      premises[
        0
      ].conclusion
    )

    decomposition_map = (
      premises[
        1
      ].conclusion
    )

    if (
      specialization.n
      != 4
    ):
      return False

    nu_4 = HomotopyElement(
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
      specialization.alpha
      != nu_4
    ):
      return False

    expected_membership = (
      TodaPrimaryGroupMembershipStatement(
        element=nu_4,
        group=TodaPrimaryGroup(
          group_dimension=7,
          sphere_dimension=4,
        ),
      )
    )

    if (
      specialization.membership
      != expected_membership
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

    expected_hopf_relation = Relation(
      lhs=MapApplication(
        map=EHP_H_MAP,
        expression=nu_4,
      ),
      rhs=iota_7,
      relation_type=RelationType.EQUALITY,
    )

    if (
      specialization.hopf_relation
      != expected_hopf_relation
    ):
      return False

    if (
      decomposition_map.alpha
      != nu_4
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
      != 4
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

    expected_target_group = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=4,
      )
    )

    if (
      target_group
      != expected_target_group
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
        sphere_dimension=3,
      )
    )

    expected_second_summand = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=7,
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
        left=nu_4,
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
        1
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
      "nu_4 n=4 decomposition "
      "specialization"
    ),
    description=(
      "Specialize Toda Proposition 4.4 "
      "to n=4 and alpha=nu_4 using "
      "the independently derived "
      "Phase 63 nu_4 specialization "
      "premises. The concrete map from "
      "pi_(i-1)^3 direct sum pi_i^7 "
      "to pi_i^4 sending "
      "(alpha,beta) to "
      "E(alpha)+nu_4 composed with beta "
      "is an isomorphism."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda56Nu4Prop44SpecializationStatement
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


def toda_56_nu4_decomposition_isomorphism_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    prop44_isomorphism = (
      premises[
        0
      ].conclusion
    )

    decomposition_map = (
      prop44_isomorphism.map
    )

    nu_4 = HomotopyElement(
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
      decomposition_map.alpha
      != nu_4
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
      != 4
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

    expected_target_group = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=4,
      )
    )

    if (
      target_group
      != expected_target_group
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
        sphere_dimension=3,
      )
    )

    expected_second_summand = (
      TodaPrimaryGroup(
        group_dimension=i,
        sphere_dimension=7,
      )
    )

    if (
      source_group.summands
      != (
        expected_first_summand,
        expected_second_summand,
      )
    ):
      return False

    first_variable = (
      decomposition_map.beta
    )

    second_variable = (
      decomposition_map.gamma
    )

    expected_formula = Sum(
      left=Suspension(
        expression=first_variable,
      ),
      right=Composition(
        left=nu_4,
        right=second_variable,
      ),
    )

    return (
      decomposition_map.formula
      == expected_formula
    )

  def build_conclusion(
    premises,
  ):
    return (
      Toda56Nu4DecompositionIsomorphismStatement(
        prop44_isomorphism=(
          premises[
            0
          ].conclusion
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda (5.6) "
      "nu_4 decomposition "
      "isomorphism semantics"
    ),
    description=(
      "Recognize the derived "
      "Proposition 4.4 specialization "
      "with n=4 and alpha=nu_4 as "
      "the finite-dimensional "
      "Toda equation (5.6) "
      "decomposition isomorphism "
      "from pi_(i-1)^3 direct sum "
      "pi_i^7 to pi_i^4, sending "
      "(alpha,beta) to "
      "E(alpha)+nu_4 composed with beta."
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


def toda_prop56_finite_dimensional_literature_statements():
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
        label="Toda Proposition 5.6",
        locator="Proposition 5.6",
        **toda_reference,
      ),
      statement=(
        "Finite-dimensional part: "
        "pi_5^2 is cyclic of order 2 "
        "generated by eta_2 cubed; "
        "pi_6^3 is cyclic of order 4 "
        "generated by nu-prime; "
        "pi_7^4 is the direct sum of "
        "Z generated by nu_4 and "
        "Z/4 generated by E nu-prime; "
        "and pi_(n+3)^n is cyclic of "
        "order 8 generated by nu_n "
        "for n at least 5."
      ),
    ),
  )


def toda_prop56_finite_dimensional_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi5_2_relation = (
      premises[
        0
      ].conclusion
    )

    pi6_3_relation = (
      premises[
        1
      ].conclusion
    )

    pi7_4_relation = (
      premises[
        2
      ].conclusion
    )

    pi8_5_relation = (
      premises[
        3
      ].conclusion
    )

    higher_relation = (
      premises[
        4
      ].conclusion
    )

    higher_range = (
      premises[
        5
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

    eta_2_cube = Composition(
      left=eta_2,
      right=Composition(
        left=eta_3,
        right=eta_4,
      ),
    )

    expected_pi5_2 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=5,
        sphere_dimension=2,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_2_cube,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi5_2_relation
      != expected_pi5_2
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

    expected_pi6_3 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=6,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=4,
        generator=nu_prime,
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi6_3_relation
      != expected_pi6_3
    ):
      return False

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
      ),
    )

    expected_pi7_4 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=4,
      ),
      rhs=DirectSumGroup(
        summands=(
          FreeCyclicGroup(
            generator=nu_4,
          ),
          FiniteCyclicGroup(
            order=4,
            generator=Suspension(
              expression=nu_prime,
            ),
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi7_4_relation
      != expected_pi7_4
    ):
      return False

    nu5_definition = (
      toda_nu_family_definition_statement(
        5
      )
    )

    expected_pi8_5 = Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=8,
        sphere_dimension=5,
      ),
      rhs=FiniteCyclicGroup(
        order=8,
        generator=(
          nu5_definition.element
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      pi8_5_relation
      != expected_pi8_5
    ):
      return False

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

    if (
      higher_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=6,
      )
    ):
      return False

    if (
      higher_relation.lhs
      != TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=3,
        ),
        sphere_dimension=n,
      )
    ):
      return False

    if (
      higher_relation.rhs.order
      != 8
    ):
      return False

    nu_n_definition = (
      toda_nu_family_definition_statement(
        n
      )
    )

    return (
      higher_relation
      .rhs
      .generator
      == nu_n_definition.element
    )

  def build_conclusion(
    premises,
  ):
    return (
      TodaProp56FiniteDimensionalStatement(
        pi5_2_group_relation=(
          premises[
            0
          ].conclusion
        ),
        pi6_3_group_relation=(
          premises[
            1
          ].conclusion
        ),
        pi7_4_group_relation=(
          premises[
            2
          ].conclusion
        ),
        pi8_5_group_relation=(
          premises[
            3
          ].conclusion
        ),
        higher_nu_group_relation=(
          premises[
            4
          ].conclusion
        ),
        higher_range=(
          premises[
            5
          ].conclusion
        ),
        literature_statements=(
          toda_prop56_finite_dimensional_literature_statements()
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Proposition 5.6 "
      "finite-dimensional integration"
    ),
    description=(
      "Integrate the independently "
      "derived finite-dimensional "
      "results "
      "pi_5^2=Z/2{eta_2 cubed}, "
      "pi_6^3=Z/4{nu-prime}, "
      "pi_7^4=Z{nu_4} direct sum "
      "Z/4{E nu-prime}, "
      "the concrete base case "
      "pi_8^5=Z/8{nu_5}, "
      "and the Toda (4.5) higher "
      "transport "
      "pi_(n+3)^n=Z/8{nu_n} "
      "for n at least 6. "
      "Together the last two branches "
      "give the finite-dimensional "
      "nu-family result for n at least 5."
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
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_58_delta_iota9_nu4_nu_prime_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    pi7_4_relation = (
      premises[
        0
      ].conclusion
    )

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
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
      lhs=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=4,
      ),
      rhs=DirectSumGroup(
        summands=(
          FreeCyclicGroup(
            generator=nu_4,
          ),
          FiniteCyclicGroup(
            order=4,
            generator=Suspension(
              expression=nu_prime,
            ),
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

    return (
      pi7_4_relation
      == expected_relation
    )

  def build_conclusion(
    premises,
  ):
    pi7_4_relation = (
      premises[
        0
      ].conclusion
    )

    nu_4 = (
      pi7_4_relation
      .rhs
      .summands[
        0
      ]
      .generator
    )

    e_nu_prime = (
      pi7_4_relation
      .rhs
      .summands[
        1
      ]
      .generator
    )

    positive_value = Sum(
      left=Multiple(
        coefficient=2,
        expression=nu_4,
      ),
      right=Multiple(
        coefficient=-1,
        expression=e_nu_prime,
      ),
    )

    return TodaDeltaImageUpToSignStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=9,
          sphere_dimension=9,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=7,
          sphere_dimension=4,
        ),
      ),
      element=HomotopyElement(
        name="ι_9",
        dimension=9,
        generator=GeneratorSymbol(
          family="ι",
          index=9,
        ),
      ),
      positive_value=positive_value,
    )

  return InferenceRule(
    name=(
      "Toda Equation 5.8 "
      "Delta iota_9 nu-expression"
    ),
    description=(
      "For the independently derived "
      "decomposition "
      "pi_7^4=Z{nu_4} plus "
      "Z/4{E nu-prime}, derive the "
      "Equation (5.8) minimum "
      "consequence that Delta(iota_9) "
      "equals plus or minus "
      "(2 nu_4 - E nu-prime)."
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


def toda_58_whitehead_square_nu_expression_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_statement = (
      premises[
        0
      ].conclusion
    )

    whitehead_data = (
      premises[
        1
      ].conclusion
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
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

    iota_9 = HomotopyElement(
      name="ι_9",
      dimension=9,
      generator=GeneratorSymbol(
        family="ι",
        index=9,
      ),
    )

    if (
      delta_statement.element
      != iota_9
    ):
      return False

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
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

    expected_positive_value = Sum(
      left=Multiple(
        coefficient=2,
        expression=nu_4,
      ),
      right=Multiple(
        coefficient=-1,
        expression=Suspension(
          expression=nu_prime,
        ),
      ),
    )

    if (
      delta_statement.positive_value
      != expected_positive_value
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

    return (
      whitehead_data.whitehead_square
      == expected_whitehead_square
    )

  def build_conclusion(
    premises,
  ):
    delta_statement = (
      premises[
        0
      ].conclusion
    )

    whitehead_data = (
      premises[
        1
      ].conclusion
    )

    return (
      Toda58WhiteheadSquareUpToSignStatement(
        whitehead_square=(
          whitehead_data
          .whitehead_square
        ),
        positive_value=(
          delta_statement
          .positive_value
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Equation 5.8 "
      "Whitehead-square nu-expression"
    ),
    description=(
      "Connect the independently "
      "derived Equation (5.8) result "
      "Delta(iota_9)=plus or minus "
      "(2 nu_4-E nu-prime) with the "
      "independently derived "
      "Lemma 5.4 Whitehead square "
      "[iota_4,iota_4]. "
      "For this concrete Equation "
      "(5.8) instance, derive "
      "[iota_4,iota_4]=plus or minus "
      "(2 nu_4-E nu-prime). "
      "No generic up-to-sign "
      "transitivity or sign algebra "
      "is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaImageUpToSignStatement
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


def toda_58_delta_iota9_whitehead_square_inference_rule():
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
      group_dimension=9,
      sphere_dimension=9,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
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

    iota_9 = HomotopyElement(
      name="ι_9",
      dimension=9,
      generator=GeneratorSymbol(
        family="ι",
        index=9,
      ),
    )

    if (
      delta_statement.element
      != iota_9
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
      whitehead_statement.whitehead_square
      != expected_whitehead_square
    ):
      return False

    return (
      delta_statement.positive_value
      == whitehead_statement.positive_value
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

    return (
      TodaDeltaImageUpToSignStatement(
        map=delta_statement.map,
        element=delta_statement.element,
        positive_value=(
          whitehead_statement
          .whitehead_square
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Equation 5.8 "
      "Delta iota_9 Whitehead-square"
    ),
    description=(
      "For the concrete Toda Equation "
      "(5.8) instance, combine the "
      "independently derived relations "
      "Delta(iota_9)=plus or minus "
      "(2 nu_4-E nu-prime) and "
      "[iota_4,iota_4]=plus or minus "
      "(2 nu_4-E nu-prime). "
      "Because the two concrete "
      "up-to-sign statements have the "
      "same positive representative, "
      "derive "
      "Delta(iota_9)=plus or minus "
      "[iota_4,iota_4]. "
      "No generic up-to-sign "
      "transitivity or sign algebra "
      "is introduced."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaImageUpToSignStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda58WhiteheadSquareUpToSignStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def toda_58_literature_statements():
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
        label="Toda (5.8)",
        locator="Equation (5.8)",
        **toda_reference,
      ),
      statement=(
        "Δ(ι₉)=±(2ν₄-Eν′)"
        "=±[ι₄,ι₄]."
      ),
    ),
  )


def toda_58_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    delta_nu_relation = (
      premises[
        0
      ].conclusion
    )

    whitehead_nu_relation = (
      premises[
        1
      ].conclusion
    )

    delta_whitehead_relation = (
      premises[
        2
      ].conclusion
    )

    expected_source = TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=9,
    )

    expected_target = TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )

    if (
      delta_nu_relation.map.source_group
      != expected_source
    ):
      return False

    if (
      delta_nu_relation.map.target_group
      != expected_target
    ):
      return False

    iota_9 = HomotopyElement(
      name="ι_9",
      dimension=9,
      generator=GeneratorSymbol(
        family="ι",
        index=9,
      ),
    )

    if (
      delta_nu_relation.element
      != iota_9
    ):
      return False

    nu_4 = HomotopyElement(
      name="ν₄",
      dimension=4,
      source=7,
      target=4,
      generator=GeneratorSymbol(
        family="ν",
        index=4,
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

    expected_nu_expression = Sum(
      left=Multiple(
        coefficient=2,
        expression=nu_4,
      ),
      right=Multiple(
        coefficient=-1,
        expression=Suspension(
          expression=nu_prime,
        ),
      ),
    )

    if (
      delta_nu_relation.positive_value
      != expected_nu_expression
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
      whitehead_nu_relation.whitehead_square
      != expected_whitehead_square
    ):
      return False

    if (
      whitehead_nu_relation.positive_value
      != expected_nu_expression
    ):
      return False

    if (
      delta_whitehead_relation.map
      != delta_nu_relation.map
    ):
      return False

    if (
      delta_whitehead_relation.element
      != delta_nu_relation.element
    ):
      return False

    return (
      delta_whitehead_relation.positive_value
      == expected_whitehead_square
    )

  def build_conclusion(
    premises,
  ):
    return Toda58EquationStatement(
      delta_nu_relation=(
        premises[
          0
        ].conclusion
      ),
      whitehead_nu_relation=(
        premises[
          1
        ].conclusion
      ),
      delta_whitehead_relation=(
        premises[
          2
        ].conclusion
      ),
      literature_statements=(
        toda_58_literature_statements()
      ),
    )

  return InferenceRule(
    name=(
      "Toda Equation 5.8 integration"
    ),
    description=(
      "Integrate the independently "
      "derived Equation (5.8) forms "
      "Delta(iota_9)=plus or minus "
      "(2 nu_4-E nu-prime), "
      "[iota_4,iota_4]=plus or minus "
      "(2 nu_4-E nu-prime), and "
      "Delta(iota_9)=plus or minus "
      "[iota_4,iota_4]. "
      "The resulting aggregate stores "
      "the direct Toda Equation (5.8) "
      "literature statement while "
      "retaining the complete derived "
      "premise provenance."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaDeltaImageUpToSignStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Toda58WhiteheadSquareUpToSignStatement
        ),
      ),
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
class TodaLemma55Statement:
  nu4: HomotopyElement
  lemma54_statement: TodaLemma54Statement
  beta_membership: HomotopyGroupMembershipStatement
  beta_eta_zero_relation: Relation
  t_range: ScalarGreaterEqualStatement
  bracket_inclusion: TodaLemma55BracketContainsUpToSignStatement
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


@dataclass(frozen=True)
class Toda55NuFamilyFiniteDimensionalStatement:
  nu_family_definition: TodaNuFamilyDefinitionStatement
  lemma54_statement: TodaLemma54Statement
  n_range: ScalarGreaterEqualStatement
  double_nu_relation: Relation
  quadruple_nu_relation: Relation
  literature_statements: tuple[
    LiteratureStatement,
    ...
  ]


def toda_55_nu_family_literature_statements():
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
        label="Toda (5.5)",
        locator="Equation (5.5)",
        **toda_reference,
      ),
      statement=(
        "Finite-dimensional part: "
        "ν_n:=E^(n-4)ν₄ for n>=4; "
        "for n>=5, "
        "2ν_n=E^(n-3)ν′ and "
        "4ν_n=η_n∘η_(n+1)∘η_(n+2)."
      ),
    ),
  )


def toda_55_nu_family_finite_dimensional_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    lemma54_statement = (
      premises[
        0
      ].conclusion
    )

    definition = (
      premises[
        1
      ].conclusion
    )

    n_range = (
      premises[
        2
      ].conclusion
    )

    double_nu_relation = (
      premises[
        3
      ].conclusion
    )

    quadruple_nu_relation = (
      premises[
        4
      ].conclusion
    )

    n = definition.index

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      definition
      != toda_nu_family_definition_statement(
        n
      )
    ):
      return False

    if (
      n_range
      != ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ):
      return False

    if (
      lemma54_statement.nu4
      != (
        definition
        .iterated_suspension
        .expression
      )
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

    expected_double_relation = Relation(
      lhs=Multiple(
        coefficient=2,
        expression=definition.element,
      ),
      rhs=IteratedSuspension(
        expression=nu_prime,
        exponent=ScalarSum(
          left=n,
          right=ScalarProduct(
            left=-1,
            right=3,
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

    if (
      double_nu_relation
      != expected_double_relation
    ):
      return False

    n_plus_one = ScalarSum(
      left=n,
      right=1,
    )

    n_plus_two = ScalarSum(
      left=n,
      right=2,
    )

    n_plus_three = ScalarSum(
      left=n,
      right=3,
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
      source=n_plus_three,
      target=n_plus_two,
      generator=GeneratorSymbol(
        family="η",
        index=n_plus_two,
      ),
    )

    expected_eta_cube = Composition(
      left=eta_n,
      right=Composition(
        left=eta_n_plus_one,
        right=eta_n_plus_two,
      ),
    )

    expected_quadruple_relation = Relation(
      lhs=Multiple(
        coefficient=4,
        expression=definition.element,
      ),
      rhs=expected_eta_cube,
      relation_type=RelationType.EQUALITY,
    )

    return (
      quadruple_nu_relation
      == expected_quadruple_relation
    )

  def build_conclusion(
    premises,
  ):
    return (
      Toda55NuFamilyFiniteDimensionalStatement(
        nu_family_definition=(
          premises[
            1
          ].conclusion
        ),
        lemma54_statement=(
          premises[
            0
          ].conclusion
        ),
        n_range=(
          premises[
            2
          ].conclusion
        ),
        double_nu_relation=(
          premises[
            3
          ].conclusion
        ),
        quadruple_nu_relation=(
          premises[
            4
          ].conclusion
        ),
        literature_statements=(
          toda_55_nu_family_literature_statements()
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda 5.5 nu-family "
      "finite-dimensional integration"
    ),
    description=(
      "Integrate the derived Toda "
      "Lemma 5.4 nu_4 provenance, "
      "the explicit nu-family "
      "definition, the n>=5 "
      "applicability condition, "
      "the derived relation "
      "2 nu_n=E^(n-3) nu-prime, "
      "and the derived relation "
      "4 nu_n=eta_n eta_(n+1) "
      "eta_(n+2) into the "
      "finite-dimensional part of "
      "Toda equation (5.5). "
      "The stable relation "
      "4 nu=eta^3 remains deferred."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Statement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          TodaNuFamilyDefinitionStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          ScalarGreaterEqualStatement
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


def toda_lemma55_literature_statements():
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
        label="Toda Lemma 5.5",
        locator="Lemma 5.5",
        **toda_reference,
      ),
      statement=(
        "If β∈π_(t+2)(S^m), "
        "β∘η_(t+2)=0, and t>0, then "
        "{η_(m+2),E^3β,η_(t+5)}_3 "
        "contains "
        "E^2β∘E^tν₄ or "
        "-E^2β∘E^tν₄."
      ),
    ),
    LiteratureStatement(
      reference=LiteratureReference(
        label="Toda Lemma 5.5 proof",
        locator="Lemma 5.5 proof",
        **toda_reference,
      ),
      statement=(
        "The preceding Lemma 5.4 proof "
        "gives a representative "
        "±(E^2β∘E^tα*). "
        "Since E[ι₄,ι₄]=0, "
        "the definition of ν₄ gives "
        "E^tν₄=±E^tα* for t>0."
      ),
    ),
  )


def toda_lemma55_integration_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    lemma54_statement = (
      premises[
        0
      ].conclusion
    )

    beta_membership = (
      premises[
        1
      ].conclusion
    )

    beta_eta_zero = (
      premises[
        2
      ].conclusion
    )

    t_range = (
      premises[
        3
      ].conclusion
    )

    bracket_inclusion = (
      premises[
        4
      ].conclusion
    )

    nu4 = (
      lemma54_statement
      .nu4
    )

    beta = (
      beta_membership
      .element
    )

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

    if (
      t_range
      != ScalarGreaterEqualStatement(
        left=t,
        right=1,
      )
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

    expected_zero = Relation(
      lhs=Composition(
        left=beta,
        right=eta_t_plus_two,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )

    if (
      beta_eta_zero
      != expected_zero
    ):
      return False

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

    expected_bracket = TodaBracket(
      first=eta_m_plus_two,
      second=IteratedSuspension(
        expression=beta,
        exponent=3,
      ),
      third=eta_t_plus_five,
      index=3,
    )

    expected_positive_value = Composition(
      left=IteratedSuspension(
        expression=beta,
        exponent=2,
      ),
      right=IteratedSuspension(
        expression=nu4,
        exponent=t,
      ),
    )

    expected_inclusion = (
      TodaLemma55BracketContainsUpToSignStatement(
        bracket=expected_bracket,
        positive_value=(
          expected_positive_value
        ),
      )
    )

    return (
      bracket_inclusion
      == expected_inclusion
    )

  def build_conclusion(
    premises,
  ):
    lemma54_statement = (
      premises[
        0
      ].conclusion
    )

    return (
      TodaLemma55Statement(
        nu4=(
          lemma54_statement
          .nu4
        ),
        lemma54_statement=(
          lemma54_statement
        ),
        beta_membership=(
          premises[
            1
          ].conclusion
        ),
        beta_eta_zero_relation=(
          premises[
            2
          ].conclusion
        ),
        t_range=(
          premises[
            3
          ].conclusion
        ),
        bracket_inclusion=(
          premises[
            4
          ].conclusion
        ),
        literature_statements=(
          toda_lemma55_literature_statements()
        ),
      )
    )

  return InferenceRule(
    name=(
      "Toda Lemma 5.5 integration"
    ),
    description=(
      "Integrate the derived Toda "
      "Lemma 5.4 nu_4, the Lemma 5.5 "
      "hypotheses on beta and t, and "
      "the derived bracket inclusion "
      "containing plus or minus "
      "E^2 beta composed with E^t nu_4 "
      "into the final Toda Lemma 5.5 "
      "aggregate. "
      "The aggregate records the "
      "Lemma 5.5 literature statement "
      "and proof consequence while "
      "preserving the independently "
      "derived Lemma 5.4 aggregate."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Statement
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
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma55BracketContainsUpToSignStatement
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


def toda_nu_family_definition_statement(
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
    and n < 4
  ):
    raise ValueError(
      "nu family requires n >= 4"
    )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  if n == 4:
    name = "ν₄"
    source = 7
    exponent = 0
  elif isinstance(
    n,
    int,
  ):
    name = (
      "ν_"
      + str(
        n
      )
    )
    source = n + 3
    exponent = n - 4
  else:
    name = "ν_n"
    source = ScalarSum(
      left=n,
      right=3,
    )
    exponent = ScalarSum(
      left=n,
      right=-4,
    )

  nu_n = HomotopyElement(
    name=name,
    dimension=n,
    source=source,
    target=n,
    generator=GeneratorSymbol(
      family="ν",
      index=n,
    ),
  )

  return TodaNuFamilyDefinitionStatement(
    index=n,
    element=nu_n,
    iterated_suspension=(
      IteratedSuspension(
        expression=nu_4,
        exponent=exponent,
      )
    ),
  )


def toda_55_nu_family_double_suspension_transport_inference_rule():
  def guard(
    premises,
    bindings,
  ):
    lemma54_statement = (
      premises[
        0
      ].conclusion
    )

    definition = (
      premises[
        1
      ].conclusion
    )

    n_range = (
      premises[
        2
      ].conclusion
    )

    n = definition.index

    if not isinstance(
      n,
      ScalarSymbol,
    ):
      return False

    if (
      n_range.left
      != n
    ):
      return False

    if (
      n_range.right
      != 5
    ):
      return False

    expected_definition = (
      toda_nu_family_definition_statement(
        n
      )
    )

    if (
      definition
      != expected_definition
    ):
      return False

    nu4 = (
      definition
      .iterated_suspension
      .expression
    )

    if (
      lemma54_statement.nu4
      != nu4
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

    expected_double_relation = Relation(
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
      lemma54_statement
      .double_suspension_relation
      == expected_double_relation
    )

  def build_conclusion(
    premises,
  ):
    definition = (
      premises[
        1
      ].conclusion
    )

    n = definition.index

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

    return Relation(
      lhs=Multiple(
        coefficient=2,
        expression=definition.element,
      ),
      rhs=IteratedSuspension(
        expression=nu_prime,
        exponent=ScalarSum(
          left=n,
          right=ScalarProduct(
            left=-1,
            right=3,
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )

  return InferenceRule(
    name=(
      "Toda 5.5 nu-family "
      "double suspension transport"
    ),
    description=(
      "For symbolic n>=5, combine the "
      "derived Toda Lemma 5.4 relation "
      "2 E nu_4 = E^2 nu-prime with "
      "the definition "
      "nu_n = E^(n-4) nu_4. "
      "Suspending the Lemma 5.4 "
      "relation by E^(n-5) gives "
      "2 nu_n = E^(n-3) nu-prime. "
      "This is a Toda (5.5)-specific "
      "transport rule and does not "
      "introduce generic suspension "
      "normalization."
    ),
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          TodaLemma54Statement
        ),
      ),
      PremisePattern(
        statement_type=(
          TodaNuFamilyDefinitionStatement
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


