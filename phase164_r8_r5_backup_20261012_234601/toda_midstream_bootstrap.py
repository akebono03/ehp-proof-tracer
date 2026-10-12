from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaProp53FiniteDimensionalStatement,
  toda_53_n3_hopf_eta5_surjective_inference_rule,
  toda_53_n3_hopf_surjective_delta_zero_inference_rule,
  toda_53_n3_delta_zero_suspension_injective_inference_rule,
  toda_53_n3_suspension_isomorphism_inference_rule,
  toda_55_nu_family_finite_dimensional_integration_inference_rule,
  toda_55_nu_family_literature_statements,
  toda_56_nu4_decomposition_integration_inference_rule,
  toda_56_nu4_decomposition_literature_statements,
  toda_48_lemma54_hopf_odd_multiple_inference_rule,
  toda_eta_family_definition_statement,
  toda_lemma54_pi6_5_finite_cyclic_inference_rule,
  toda_prop53_finite_dimensional_integration_inference_rule,
  toda_prop53_higher_eta_squared_bridge_inference_rule,
  toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule,
  toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
  toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule,
  toda_53_n3_prop51_delta_injective_inference_rule,
  toda_53_n3_delta_injective_hopf_zero_inference_rule,
  toda_53_n3_hopf_zero_suspension_surjective_inference_rule,
)


def _find_unique_step(
  steps: tuple[ProofStep, ...],
  predicate,
  description: str,
) -> ProofStep:
  matches = tuple(
    step
    for step in steps
    if predicate(step)
  )

  if len(matches) != 1:
    raise ValueError(
      "expected exactly one "
      f"{description} step, "
      f"found {len(matches)}"
    )

  return matches[0]


def build_phase59_pi5_3_step(
  pi4_2_step: ProofStep,
  suspension_isomorphism_step: ProofStep,
) -> ProofStep:
  eta3_definition_step = ProofStep(
    conclusion=toda_eta_family_definition_statement(
      3
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta4_definition_step = ProofStep(
    conclusion=toda_eta_family_definition_statement(
      4
    ),
    premises=(),
    rule=ProofRule.GIVEN,
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

  expected_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=eta_3,
        right=eta_4,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop53_n3_eta_square_suspension_bridge_inference_rule(),
      toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule(),
    ),
    (
      pi4_2_step,
      suspension_isomorphism_step,
      eta3_definition_step,
      eta4_definition_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected_relation
    ),
    "pi_5^3",
  )


def build_phase59_hopf_surjective_step(
  prop51_step: ProofStep,
  hopf_eta5_step: ProofStep,
) -> ProofStep:
  pi_4_2 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=2,
  )
  pi_5_3 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=3,
  )
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )
  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )
  pi_6_5 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=5,
  )
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  premise_steps = (
    prop51_step,
    hopf_eta5_step,
    ProofStep(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_5_3,
          middle_term=pi_5_5,
          target_term=pi_3_2,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_4_2,
          middle_term=pi_5_3,
          target_term=pi_5_5,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_6_3,
          middle_term=pi_6_5,
          target_term=pi_4_2,
          first_map=EHP_H_MAP,
          second_map=EHP_DELTA_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_6_5,
          middle_term=pi_4_2,
          target_term=pi_5_3,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  result = run_inference_until_stable_with_history(
    (
      toda_53_n3_prop51_delta_injective_inference_rule(),
      toda_53_n3_delta_injective_hopf_zero_inference_rule(),
      toda_53_n3_hopf_zero_suspension_surjective_inference_rule(),
      toda_53_n3_hopf_eta5_surjective_inference_rule(),
      toda_53_n3_hopf_surjective_delta_zero_inference_rule(),
      toda_53_n3_delta_zero_suspension_injective_inference_rule(),
      toda_53_n3_suspension_isomorphism_inference_rule(),
    ),
    premise_steps,
  )

  expected = TodaHopfInvariantSurjectiveStatement(
    map=TodaHopfInvariantMap(
      source_group=pi_6_3,
      target_group=pi_6_5,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected
    ),
    "H: pi_6^3 -> pi_6^5 surjective",
  )


def build_phase59_prop53_step(
  pi4_2_step: ProofStep,
  pi5_3_step: ProofStep,
  pi6_4_step: ProofStep,
  higher_transport_step: ProofStep,
  higher_range_step: ProofStep,
) -> ProofStep:
  n = higher_range_step.conclusion.left

  eta_n_definition_step = ProofStep(
    conclusion=toda_eta_family_definition_statement(
      n
    ),
    premises=(),
    rule=ProofRule.GIVEN,
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

  eta_n = eta_n_definition_step.conclusion.element
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

  expected_higher_relation = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=2,
      ),
      sphere_dimension=n,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_n_squared,
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_statement = TodaProp53FiniteDimensionalStatement(
    pi4_2_group_relation=pi4_2_step.conclusion,
    pi5_3_group_relation=pi5_3_step.conclusion,
    pi6_4_group_relation=pi6_4_step.conclusion,
    higher_eta_squared_group_relation=(
      expected_higher_relation
    ),
    higher_range=higher_range_step.conclusion,
  )

  result = run_inference_until_stable_with_history(
    (
      toda_prop53_higher_eta_squared_bridge_inference_rule(),
      toda_prop53_higher_eta_squared_finite_cyclic_generator_inference_rule(),
      toda_prop53_finite_dimensional_integration_inference_rule(),
    ),
    (
      pi4_2_step,
      pi5_3_step,
      pi6_4_step,
      higher_transport_step,
      higher_range_step,
      eta_n_definition_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected_statement
    ),
    "Toda Proposition 5.3",
  )


def build_phase60_pi6_5_step(
  prop51_step: ProofStep,
  theorem36_step: ProofStep,
  final_double_step: ProofStep,
  nu_prime_hopf_step: ProofStep,
) -> ProofStep:
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

  result = run_inference_until_stable_with_history(
    (
      toda_lemma54_pi6_5_finite_cyclic_inference_rule(),
      toda_48_lemma54_hopf_odd_multiple_inference_rule(),
    ),
    (
      prop51_step,
      theorem36_step,
      final_double_step,
      nu_prime_hopf_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected_pi6_5
    ),
    "pi_6^5",
  )


def build_phase62_toda55_step(
  lemma54_step: ProofStep,
  definition_step: ProofStep,
  n_range_step: ProofStep,
  double_nu_step: ProofStep,
  quadruple_nu_step: ProofStep,
) -> ProofStep:
  expected_statement = (
    Toda55NuFamilyFiniteDimensionalStatement(
      nu_family_definition=(
        definition_step.conclusion
      ),
      lemma54_statement=(
        lemma54_step.conclusion
      ),
      n_range=(
        n_range_step.conclusion
      ),
      double_nu_relation=(
        double_nu_step.conclusion
      ),
      quadruple_nu_relation=(
        quadruple_nu_step.conclusion
      ),
      literature_statements=(
        toda_55_nu_family_literature_statements()
      ),
    )
  )

  result = run_inference_until_stable_with_history(
    toda_55_nu_family_finite_dimensional_integration_inference_rule(),
    (
      lemma54_step,
      definition_step,
      n_range_step,
      double_nu_step,
      quadruple_nu_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected_statement
    ),
    "Toda (5.5)",
  )


def build_phase63_toda56_step(
  decomposition_step: ProofStep,
  lemma54_step: ProofStep,
) -> ProofStep:
  expected_statement = (
    Toda56Nu4DecompositionStatement(
      decomposition_isomorphism=(
        decomposition_step.conclusion
      ),
      lemma54_statement=(
        lemma54_step.conclusion
      ),
      literature_statements=(
        toda_56_nu4_decomposition_literature_statements()
      ),
    )
  )

  result = run_inference_until_stable_with_history(
    toda_56_nu4_decomposition_integration_inference_rule(),
    (
      decomposition_step,
      lemma54_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: (
      step.conclusion
      == expected_statement
    ),
    "Toda (5.6)",
  )
