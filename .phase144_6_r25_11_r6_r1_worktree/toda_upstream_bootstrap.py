from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
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
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
)
from low_dimensional_facts import (
  e_pi_1_1_to_pi_2_2_isomorphism_fact,
  pi_2_1_zero_fact,
  pi_3_3_free_cyclic_fact,
  pi_4_5_zero_fact,
  pi_5_5_free_cyclic_fact,
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
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_preserved_under_left_composition_inference_rule,
  equality_preserved_under_right_composition_inference_rule,
  equality_transitivity_inference_rule,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  TodaBracketMembershipStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaPi32Eta2DefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaSuspensionInjectiveStatement,
  toda_45_isomorphism_inference_rule,
  toda_52_eta2_composition_isomorphism_inference_rule,
  toda_53_eta3_twice_zero_inference_rule,
  toda_53_eta4_suspension_bridge_inference_rule,
  toda_53_eta5_iterated_suspension_bridge_inference_rule,
  toda_53_nu_prime_bracket_specialization_inference_rule,
  toda_53_nu_prime_lemma52_double_inference_rule,
  toda_53_nu_prime_lemma52_hopf_inference_rule,
  toda_53_nu_prime_lemma52_membership_inference_rule,
  toda_delta_iota5_whitehead_square_inference_rule,
  toda_eta_family_definition_statement,
  toda_eta3_suspension_relation_inference_rule,
  toda_exactness_injective_right_implies_delta_zero_inference_rule,
  toda_exactness_zero_delta_implies_hopf_surjective_inference_rule,
  toda_exactness_zero_left_implies_hopf_injective_inference_rule,
  toda_hopf_injective_surjective_implies_isomorphism_inference_rule,
  toda_pi3_2_define_eta2_inference_rule,
  toda_pi3_2_eta2_hopf_relation_inference_rule,
  toda_pi3_2_free_cyclic_generator_inference_rule,
  toda_pi3_2_whitehead_square_up_to_sign_inference_rule,
  toda_pi4_3_delta_image_free_cyclic_inference_rule,
  toda_pi4_3_eta3_generator_inference_rule,
  toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule,
  toda_pi4_3_finite_cyclic_inference_rule,
  toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule,
  toda_pi_i_minus_1_1_zero_inference_rule,
  toda_prop27_iota2_whitehead_hopf_invariant_inference_rule,
  toda_prop44_eta2_n2_isomorphism_inference_rule,
  toda_prop44_eta2_second_summand_restriction_inference_rule,
  toda_suspension_isomorphism_implies_injective_inference_rule,
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


def build_toda_45_stable_isomorphism_step(
  n=5,
  k=3,
  m=None,
) -> ProofStep:
  if m is None:
    m = ScalarSymbol(
      name="n",
    )

  stable_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=ScalarSum(
        left=k,
        right=2,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=m,
      right=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_map_step = ProofStep(
    conclusion=TodaIteratedSuspensionMap(
      exponent=ScalarSum(
        left=m,
        right=ScalarProduct(
          left=-1,
          right=n,
        ),
      ),
      source_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=n,
          right=k,
        ),
        sphere_dimension=n,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=m,
          right=k,
        ),
        sphere_dimension=m,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable_with_history(
    toda_45_isomorphism_inference_rule(),
    (
      stable_range_step,
      suspension_range_step,
      suspension_map_step,
    ),
  )

  return _find_unique_step(
    result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda45IsomorphismStatement,
    ),
    "Toda (4.5) isomorphism",
  )


def _build_phase49_result():
  pi_2_1 = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=1,
  )
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )
  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )
  pi_1_1 = TodaPrimaryGroup(
    group_dimension=1,
    sphere_dimension=1,
  )
  pi_2_2 = TodaPrimaryGroup(
    group_dimension=2,
    sphere_dimension=2,
  )

  premise_steps = (
    ProofStep(
      conclusion=pi_2_1_zero_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=pi_3_3_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=e_pi_1_1_to_pi_2_2_isomorphism_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_2_1,
          middle_term=pi_3_2,
          target_term=pi_3_3,
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
          source_term=pi_3_2,
          middle_term=pi_3_3,
          target_term=pi_1_1,
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
          source_term=pi_3_3,
          middle_term=pi_1_1,
          target_term=pi_2_2,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),
    toda_suspension_isomorphism_implies_injective_inference_rule(),
    toda_exactness_injective_right_implies_delta_zero_inference_rule(),
    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),
    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),
    toda_pi3_2_define_eta2_inference_rule(),
    toda_pi3_2_eta2_hopf_relation_inference_rule(),
    toda_pi3_2_free_cyclic_generator_inference_rule(),
  )

  result = run_inference_until_stable_with_history(
    rules,
    premise_steps,
  )

  return {
    "premise_steps": premise_steps,
    "rules": rules,
    "result": result,
  }


def _build_phase50_result():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )
  pi_3_3 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=3,
  )
  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )
  pi_4_5 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=5,
  )

  iota_2 = HomotopyElement(
    name="ι_2",
    dimension=2,
    generator=GeneratorSymbol(
      family="ι",
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

  hopf_map = TodaHopfInvariantMap(
    source_group=pi_3_2,
    target_group=pi_3_3,
  )

  premise_steps = (
    ProofStep(
      conclusion=WhiteheadProduct(
        left=iota_2,
        right=iota_2,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaPi32Eta2DefinitionStatement(
        map=hopf_map,
        element=eta_2,
        image=iota_3,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=eta_2,
        ),
        rhs=iota_3,
        relation_type=RelationType.EQUALITY,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaHopfInvariantInjectiveStatement(
        map=hopf_map,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=pi_5_5_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=pi_4_5_zero_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaDeltaMap(
        source_group=pi_5_5,
        target_group=pi_3_2,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_5_5,
          middle_term=pi_3_2,
          target_term=pi_4_3,
          first_map=EHP_DELTA_MAP,
          second_map=EHP_E_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=TodaProp42ExactnessStatement(
        window=TodaEHPExactnessWindow(
          source_term=pi_3_2,
          middle_term=pi_4_3,
          target_term=pi_4_5,
          first_map=EHP_E_MAP,
          second_map=EHP_H_MAP,
        ),
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=Relation(
        lhs=pi_3_2,
        rhs=FreeCyclicGroup(
          generator=eta_2,
        ),
        relation_type=RelationType.EQUALITY,
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=toda_eta_family_definition_statement(
        3
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  rules = (
    toda_prop27_iota2_whitehead_hopf_invariant_inference_rule(),
    toda_pi3_2_whitehead_square_up_to_sign_inference_rule(),
    toda_delta_iota5_whitehead_square_inference_rule(),
    toda_pi4_3_delta_image_free_cyclic_inference_rule(),
    toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
    toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
    toda_pi4_3_finite_cyclic_inference_rule(),
    toda_eta3_suspension_relation_inference_rule(),
    toda_pi4_3_eta3_generator_inference_rule(),
  )

  result = run_inference_until_stable_with_history(
    rules,
    premise_steps,
  )

  final_group_step = _find_unique_step(
    result.steps,
    lambda step: (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == pi_4_3
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.rhs.order
      == 2
      and step.conclusion.rhs.generator
      == eta_3
    ),
    "pi_4^3",
  )

  return {
    "result": result,
    "final_group_step": final_group_step,
  }


def build_toda_52_composition_isomorphism_step() -> ProofStep:
  phase49 = _build_phase49_result()

  i = ScalarSymbol(
    name="i",
  )
  i_minus_one = ScalarSum(
    left=i,
    right=-1,
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
  beta = HomotopyElement(
    name="β",
    dimension=i_minus_one,
  )
  gamma = HomotopyElement(
    name="γ",
    dimension=i,
    source=i,
    target=3,
  )

  first_summand = TodaPrimaryGroup(
    group_dimension=i_minus_one,
    sphere_dimension=1,
  )
  second_summand = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=3,
  )
  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=2,
  )

  decomposition_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(
        first_summand,
        second_summand,
      ),
    ),
    target_group=target_group,
    alpha=eta_2,
    beta=beta,
    gamma=gamma,
    formula=Sum(
      left=Suspension(
        expression=beta,
      ),
      right=Composition(
        left=eta_2,
        right=gamma,
      ),
    ),
  )

  premise_steps = (
    phase49[
      "premise_steps"
    ]
    + (
      ProofStep(
        conclusion=ScalarGreaterEqualStatement(
          left=i,
          right=3,
        ),
        premises=(),
        rule=ProofRule.GIVEN,
      ),
      ProofStep(
        conclusion=decomposition_map,
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  rules = (
    phase49[
      "rules"
    ]
    + (
      toda_pi_i_minus_1_1_zero_inference_rule(),
      toda_prop44_eta2_n2_isomorphism_inference_rule(),
      toda_prop44_eta2_second_summand_restriction_inference_rule(),
      toda_52_eta2_composition_isomorphism_inference_rule(),
    )
  )

  result = run_inference_until_stable_with_history(
    rules,
    premise_steps,
  )

  return _find_unique_step(
    result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda52CompositionIsomorphismStatement,
    ),
    "Toda (5.2) composition isomorphism",
  )


def build_toda_53_nu_prime_steps() -> tuple[
  ProofStep,
  ProofStep,
  ProofStep,
]:
  phase50 = _build_phase50_result()

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
  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
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

  bracket_membership_step = ProofStep(
    conclusion=TodaBracketMembershipStatement(
      element=nu_prime,
      bracket=TodaBracket(
        first=eta_3,
        second=Multiple(
          coefficient=2,
          expression=iota_4,
        ),
        third=eta_4,
        index=1,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  specialization_result = (
    run_inference_until_stable_with_history(
      toda_53_nu_prime_bracket_specialization_inference_rule(),
      (
        bracket_membership_step,
      ),
    )
  )

  specialization_step = _find_unique_step(
    specialization_result.steps,
    lambda step: isinstance(
      step.conclusion,
      Toda53NuPrimeBracketSpecializationStatement,
    ),
    "nu-prime bracket specialization",
  )

  eta3_zero_result = (
    run_inference_until_stable_with_history(
      toda_53_eta3_twice_zero_inference_rule(),
      (
        phase50[
          "final_group_step"
        ],
      ),
    )
  )

  two_eta3_zero_step = _find_unique_step(
    eta3_zero_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=Multiple(
          coefficient=2,
          expression=eta_3,
        ),
        rhs=Zero(),
        relation_type=RelationType.ZERO,
      )
    ),
    "2 eta_3 zero",
  )

  raw_result = (
    run_inference_until_stable_with_history(
      (
        toda_53_nu_prime_lemma52_hopf_inference_rule(),
        toda_53_nu_prime_lemma52_double_inference_rule(),
        toda_53_nu_prime_lemma52_membership_inference_rule(),
      ),
      (
        specialization_step,
        two_eta3_zero_step,
      ),
    )
  )

  raw_hopf_step = _find_unique_step(
    raw_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=nu_prime,
        ),
        rhs=IteratedSuspension(
          expression=eta_3,
          exponent=2,
        ),
        relation_type=RelationType.EQUALITY,
      )
    ),
    "raw H(nu-prime)",
  )

  raw_double_step = _find_unique_step(
    raw_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=Multiple(
          coefficient=2,
          expression=nu_prime,
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
    ),
    "raw 2 nu-prime",
  )

  membership_step = _find_unique_step(
    raw_result.steps,
    lambda step: (
      step.conclusion
      == HomotopyGroupMembershipStatement(
        element=nu_prime,
        group_dimension=6,
        sphere_dimension=3,
      )
    ),
    "nu-prime membership",
  )

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
  eta5_definition_step = ProofStep(
    conclusion=toda_eta_family_definition_statement(
      5
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta5_bridge_result = (
    run_inference_until_stable_with_history(
      toda_53_eta5_iterated_suspension_bridge_inference_rule(),
      (
        eta3_definition_step,
        eta5_definition_step,
      ),
    )
  )

  eta5_bridge_step = _find_unique_step(
    eta5_bridge_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=IteratedSuspension(
          expression=eta_3,
          exponent=2,
        ),
        rhs=eta_5,
        relation_type=RelationType.EQUALITY,
      )
    ),
    "eta_5 suspension bridge",
  )

  hopf_result = (
    run_inference_until_stable_with_history(
      equality_transitivity_inference_rule(),
      (
        raw_hopf_step,
        eta5_bridge_step,
      ),
    )
  )

  final_hopf_step = _find_unique_step(
    hopf_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=MapApplication(
          map=EHP_H_MAP,
          expression=nu_prime,
        ),
        rhs=eta_5,
        relation_type=RelationType.EQUALITY,
      )
    ),
    "H(nu-prime)=eta_5",
  )

  eta4_bridge_result = (
    run_inference_until_stable_with_history(
      toda_53_eta4_suspension_bridge_inference_rule(),
      (
        eta3_definition_step,
        eta4_definition_step,
      ),
    )
  )

  eta4_bridge_step = _find_unique_step(
    eta4_bridge_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
        lhs=Suspension(
          expression=eta_3,
        ),
        rhs=eta_4,
        relation_type=RelationType.EQUALITY,
      )
    ),
    "eta_4 suspension bridge",
  )

  right_rule = (
    equality_preserved_under_right_composition_inference_rule(
      eta_5,
    )
  )
  right_match = find_inference_match(
    right_rule,
    (
      eta4_bridge_step,
    ),
  )

  if right_match is None:
    raise ValueError(
      "eta_4 bridge right-composition did not match"
    )

  right_step = apply_inference_match(
    right_match
  )

  left_rule = (
    equality_preserved_under_left_composition_inference_rule(
      eta_3,
    )
  )
  left_match = find_inference_match(
    left_rule,
    (
      right_step,
    ),
  )

  if left_match is None:
    raise ValueError(
      "eta_4 bridge left-composition did not match"
    )

  composition_step = apply_inference_match(
    left_match
  )

  double_result = (
    run_inference_until_stable_with_history(
      equality_transitivity_inference_rule(),
      (
        raw_double_step,
        composition_step,
      ),
    )
  )

  final_double_step = _find_unique_step(
    double_result.steps,
    lambda step: (
      step.conclusion
      == Relation(
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
    ),
    "2 nu-prime",
  )

  return (
    membership_step,
    final_hopf_step,
    final_double_step,
  )


def build_toda_prop56_upstream_core() -> dict[
  str,
  ProofStep,
]:
  membership_step, hopf_step, double_step = (
    build_toda_53_nu_prime_steps()
  )

  n = ScalarSymbol(
    name="n",
  )

  return {
    "toda52_step": (
      build_toda_52_composition_isomorphism_step()
    ),
    "hopf_nu_prime_step": hopf_step,
    "double_step": double_step,
    "membership_step": membership_step,
    "stable_isomorphism_step": (
      build_toda_45_stable_isomorphism_step(
        n=5,
        k=3,
        m=n,
      )
    ),
  }
