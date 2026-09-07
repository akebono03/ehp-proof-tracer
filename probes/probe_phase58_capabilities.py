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
  Suspension,
  TodaBracket,
  Zero,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase50_capabilities import (
  build_phase50_representative_result,
  print_separator,
)
from relation_rules import (
  equality_preserved_under_left_composition_inference_rule,
  equality_preserved_under_right_composition_inference_rule,
  equality_transitivity_inference_rule,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  toda_53_eta3_twice_zero_inference_rule,
  toda_53_eta4_suspension_bridge_inference_rule,
  toda_53_eta5_iterated_suspension_bridge_inference_rule,
  toda_53_nu_prime_bracket_specialization_inference_rule,
  toda_53_nu_prime_lemma52_double_inference_rule,
  toda_53_nu_prime_lemma52_hopf_inference_rule,
  toda_53_nu_prime_lemma52_membership_inference_rule,
  toda_eta_family_definition_statement,
)


def build_phase58_representative_result():
  phase50 = (
    build_phase50_representative_result()
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

  bracket_membership = (
    TodaBracketMembershipStatement(
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
    )
  )

  bracket_membership_step = ProofStep(
    conclusion=bracket_membership,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  specialization_rule = (
    toda_53_nu_prime_bracket_specialization_inference_rule()
  )

  specialization_result = (
    run_inference_until_stable_with_history(
      specialization_rule,
      (
        bracket_membership_step,
      ),
    )
  )

  specialization_step = next(
    step
    for step in specialization_result.steps
    if isinstance(
      step.conclusion,
      Toda53NuPrimeBracketSpecializationStatement,
    )
  )

  pi4_3_step = (
    phase50[
      "final_group_steps"
    ][
      0
    ]
  )

  eta3_zero_rule = (
    toda_53_eta3_twice_zero_inference_rule()
  )

  eta3_zero_result = (
    run_inference_until_stable_with_history(
      eta3_zero_rule,
      (
        pi4_3_step,
      ),
    )
  )

  expected_two_eta3_zero = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=eta_3,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  two_eta3_zero_step = next(
    step
    for step in eta3_zero_result.steps
    if (
      step.conclusion
      == expected_two_eta3_zero
    )
  )

  raw_hopf_rule = (
    toda_53_nu_prime_lemma52_hopf_inference_rule()
  )

  raw_double_rule = (
    toda_53_nu_prime_lemma52_double_inference_rule()
  )

  membership_rule = (
    toda_53_nu_prime_lemma52_membership_inference_rule()
  )

  phase58_3_result = (
    run_inference_until_stable_with_history(
      (
        raw_hopf_rule,
        raw_double_rule,
        membership_rule,
      ),
      (
        specialization_step,
        two_eta3_zero_step,
      ),
    )
  )

  expected_raw_hopf = Relation(
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

  expected_raw_double = Relation(
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

  expected_membership = (
    HomotopyGroupMembershipStatement(
      element=nu_prime,
      group_dimension=6,
      sphere_dimension=3,
    )
  )

  raw_hopf_step = next(
    step
    for step in phase58_3_result.steps
    if (
      step.conclusion
      == expected_raw_hopf
    )
  )

  raw_double_step = next(
    step
    for step in phase58_3_result.steps
    if (
      step.conclusion
      == expected_raw_double
    )
  )

  membership_step = next(
    step
    for step in phase58_3_result.steps
    if (
      step.conclusion
      == expected_membership
    )
  )

  eta3_definition_step = ProofStep(
    conclusion=(
      toda_eta_family_definition_statement(
        3
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta4_definition_step = ProofStep(
    conclusion=(
      toda_eta_family_definition_statement(
        4
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta5_definition_step = ProofStep(
    conclusion=(
      toda_eta_family_definition_statement(
        5
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta5_bridge_rule = (
    toda_53_eta5_iterated_suspension_bridge_inference_rule()
  )

  eta5_bridge_result = (
    run_inference_until_stable_with_history(
      eta5_bridge_rule,
      (
        eta3_definition_step,
        eta5_definition_step,
      ),
    )
  )

  expected_eta5_bridge = Relation(
    lhs=IteratedSuspension(
      expression=eta_3,
      exponent=2,
    ),
    rhs=eta_5,
    relation_type=RelationType.EQUALITY,
  )

  eta5_bridge_step = next(
    step
    for step in eta5_bridge_result.steps
    if (
      step.conclusion
      == expected_eta5_bridge
    )
  )

  hopf_transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  hopf_result = (
    run_inference_until_stable_with_history(
      hopf_transitivity_rule,
      (
        raw_hopf_step,
        eta5_bridge_step,
      ),
    )
  )

  expected_final_hopf = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=nu_prime,
    ),
    rhs=eta_5,
    relation_type=RelationType.EQUALITY,
  )

  final_hopf_step = next(
    step
    for step in hopf_result.steps
    if (
      step.conclusion
      == expected_final_hopf
    )
  )

  eta4_bridge_rule = (
    toda_53_eta4_suspension_bridge_inference_rule()
  )

  eta4_bridge_result = (
    run_inference_until_stable_with_history(
      eta4_bridge_rule,
      (
        eta3_definition_step,
        eta4_definition_step,
      ),
    )
  )

  expected_eta4_bridge = Relation(
    lhs=Suspension(
      expression=eta_3,
    ),
    rhs=eta_4,
    relation_type=RelationType.EQUALITY,
  )

  eta4_bridge_step = next(
    step
    for step in eta4_bridge_result.steps
    if (
      step.conclusion
      == expected_eta4_bridge
    )
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
    raise AssertionError(
      "Phase 58 representative "
      "right-composition did not match"
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
    raise AssertionError(
      "Phase 58 representative "
      "left-composition did not match"
    )

  composition_step = (
    apply_inference_match(
      left_match
    )
  )

  double_transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  double_result = (
    run_inference_until_stable_with_history(
      double_transitivity_rule,
      (
        raw_double_step,
        composition_step,
      ),
    )
  )

  expected_final_double = Relation(
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

  final_double_step = next(
    step
    for step in double_result.steps
    if (
      step.conclusion
      == expected_final_double
    )
  )

  premise_steps = (
    bracket_membership_step,
    eta3_definition_step,
    eta4_definition_step,
    eta5_definition_step,
  )

  return {
    "phase50": phase50,
    "eta_3": eta_3,
    "eta_4": eta_4,
    "eta_5": eta_5,
    "nu_prime": nu_prime,
    "bracket_membership": (
      bracket_membership
    ),
    "bracket_membership_step": (
      bracket_membership_step
    ),
    "pi4_3_step": pi4_3_step,
    "specialization_result": (
      specialization_result
    ),
    "specialization_step": (
      specialization_step
    ),
    "eta3_zero_result": (
      eta3_zero_result
    ),
    "two_eta3_zero_step": (
      two_eta3_zero_step
    ),
    "expected_two_eta3_zero": (
      expected_two_eta3_zero
    ),    
    "phase58_3_result": (
      phase58_3_result
    ),
    "raw_hopf_step": raw_hopf_step,
    "raw_double_step": raw_double_step,
    "membership_step": (
      membership_step
    ),
    "eta3_definition_step": (
      eta3_definition_step
    ),
    "eta4_definition_step": (
      eta4_definition_step
    ),
    "eta5_definition_step": (
      eta5_definition_step
    ),
    "eta5_bridge_result": (
      eta5_bridge_result
    ),
    "eta5_bridge_step": (
      eta5_bridge_step
    ),
    "hopf_result": hopf_result,
    "final_hopf_step": (
      final_hopf_step
    ),
    "eta4_bridge_result": (
      eta4_bridge_result
    ),
    "eta4_bridge_step": (
      eta4_bridge_step
    ),
    "right_step": right_step,
    "composition_step": (
      composition_step
    ),
    "double_result": double_result,
    "final_double_step": (
      final_double_step
    ),
    "expected_raw_hopf": (
      expected_raw_hopf
    ),
    "expected_raw_double": (
      expected_raw_double
    ),
    "expected_membership": (
      expected_membership
    ),
    "expected_eta5_bridge": (
      expected_eta5_bridge
    ),
    "expected_eta4_bridge": (
      expected_eta4_bridge
    ),
    "expected_final_hopf": (
      expected_final_hopf
    ),
    "expected_final_double": (
      expected_final_double
    ),
    "premise_steps": premise_steps,
  }


def print_phase58_result(
  representative,
):
  print()
  print_separator()
  print(
    "Toda (5.3) nu-prime consequence"
  )
  print_separator()
  print()

  print(
    "  ν′ ∈ {η₃, 2ι₄, η₄}_1"
  )
  print()
  print(
    "  ↓ Lemma 5.2 specialization"
  )
  print()
  print(
    "  ν′ ∈ π_6^3"
  )
  print(
    "  H(ν′) = η₅"
  )
  print(
    "  2ν′ = η₃∘η₄∘η₅"
  )


def print_phase58_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / integration"
  )
  print_separator()
  print()

  final_steps = (
    representative[
      "membership_step"
    ],
    representative[
      "final_hopf_step"
    ],
    representative[
      "final_double_step"
    ],
  )

  print(
    "nu-prime membership derived =",
    (
      final_steps[
        0
      ].conclusion
      == representative[
        "expected_membership"
      ]
    ),
  )

  print(
    "H(nu-prime)=eta_5 derived =",
    (
      final_steps[
        1
      ].conclusion
      == representative[
        "expected_final_hopf"
      ]
    ),
  )

  print(
    "2 nu-prime relation derived =",
    (
      final_steps[
        2
      ].conclusion
      == representative[
        "expected_final_double"
      ]
    ),
  )

  print(
    "all final results are INFERENCE =",
    all(
      step.rule
      == ProofRule.INFERENCE
      for step in final_steps
    ),
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in representative[
      "premise_steps"
    ]
  )

  print(
    "final results are GIVEN =",
    any(
      conclusion
      in initial_conclusions
      for conclusion in (
        representative[
          "expected_membership"
        ],
        representative[
          "expected_final_hopf"
        ],
        representative[
          "expected_final_double"
        ],
      )
    ),
  )


def print_phase58_execution(
  representative,
):
  print()
  print_separator()
  print(
    "Same-run execution"
  )
  print_separator()
  print()

  safe_results = (
    representative[
      "specialization_result"
    ],
    representative[
      "eta3_zero_result"
    ],
    representative[
      "phase58_3_result"
    ],
    representative[
      "eta5_bridge_result"
    ],
    representative[
      "hopf_result"
    ],
    representative[
      "eta4_bridge_result"
    ],
    representative[
      "double_result"
    ],
  )

  print(
    "fixed-point-safe stages complete =",
    all(
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
      for result in safe_results
    ),
  )

  print(
    "composition propagation one-shot =",
    (
      representative[
        "right_step"
      ].rule
      == ProofRule.INFERENCE
      and representative[
        "composition_step"
      ].rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "shared raw specialization =",
    (
      representative[
        "raw_hopf_step"
      ]
      in representative[
        "phase58_3_result"
      ].steps
      and representative[
        "raw_double_step"
      ]
      in representative[
        "phase58_3_result"
      ].steps
      and representative[
        "membership_step"
      ]
      in representative[
        "phase58_3_result"
      ].steps
    ),
  )


def print_phase58_boundary():
  print()
  print_separator()
  print(
    "Phase 58 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  Toda (5.3) nu-prime specialization"
  )
  print(
    "  nu-prime in pi_6^3"
  )
  print(
    "  H(nu-prime)=eta_5"
  )
  print(
    "  2 nu-prime=eta_3 o eta_4 o eta_5"
  )
  print(
    "  derived provenance"
  )
  print(
    "  representative staged same-run"
  )

  print()
  print(
    "Still outside Phase 58:"
  )
  print(
    "  generic concrete eta normalization"
  )
  print(
    "  unrestricted fixed-point composition closure"
  )
  print(
    "  generic Toda-bracket specialization framework"
  )
  print(
    "  stable homotopy group model"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 58 capability demonstration"
  )

  representative = (
    build_phase58_representative_result()
  )

  print_phase58_result(
    representative
  )

  print_phase58_provenance(
    representative
  )

  print_phase58_execution(
    representative
  )

  print_phase58_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


