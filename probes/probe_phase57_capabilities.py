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
  ScalarSum,
  ScalarSymbol,
  Suspension,
  TodaBracket,
  Zero,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
)
from probes.probe_phase49_capabilities import (
  print_separator,
)
from probes.probe_phase55_capabilities import (
  build_phase55_representative_result,
)
from relation_rules import (
  zero_equality_implies_zero_inference_rule,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  toda_21_lemma52_suspended_indeterminacy_zero_inference_rule,
  toda_cor37_lemma52_representative_inference_rule,
  toda_lemma45_n4_suspension_zero_reflection_inference_rule,
  toda_lemma45_n4_two_iota3_composition_inference_rule,
  toda_lemma52_beta_membership_inference_rule,
  toda_lemma52_delta_e2_alpha_zero_inference_rule,
  toda_lemma52_delta_two_eta2_preimage_inference_rule,
  toda_lemma52_double_value_inference_rule,
  toda_lemma52_hopf_value_inference_rule,
  toda_lemma52_prop26_first_zero_inference_rule,
  toda_prop13_lemma52_bracket_transformation_inference_rule,
  toda_prop14_lemma52_bracket_transformation_inference_rule,
  toda_prop26_lemma52_hopf_bracket_inference_rule,
  toda_prop51_eta4_twice_zero_inference_rule,
)


def build_phase57_representative_result():
  phase55 = (
    build_phase55_representative_result()
  )

  i = ScalarSymbol(
    name="i",
  )

  i_plus_one = ScalarSum(
    left=i,
    right=1,
  )

  i_plus_two = ScalarSum(
    left=i,
    right=2,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  beta = HomotopyElement(
    name="β",
    dimension=i_plus_two,
    source=i_plus_two,
    target=3,
  )

  gamma = HomotopyElement(
    name="γ",
    dimension=i_plus_two,
    source=i_plus_two,
    target=4,
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

  iota_4 = HomotopyElement(
    name="ι_4",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
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

  alpha_membership = (
    HomotopyGroupMembershipStatement(
      element=alpha,
      group_dimension=i,
      sphere_dimension=3,
    )
  )

  two_alpha_zero = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=alpha,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  bracket = TodaBracket(
    first=eta_3,
    second=Multiple(
      coefficient=2,
      expression=iota_4,
    ),
    third=Suspension(
      expression=alpha,
    ),
    index=1,
  )

  bracket_membership = (
    TodaBracketMembershipStatement(
      element=beta,
      bracket=bracket,
    )
  )

  gamma_membership = (
    HomotopyGroupMembershipStatement(
      element=gamma,
      group_dimension=i_plus_two,
      sphere_dimension=4,
    )
  )

  phase57_premise_steps = (
    ProofStep(
      conclusion=alpha_membership,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=two_alpha_zero,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=bracket_membership,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=gamma_membership,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  premise_steps = (
    phase55[
      "premise_steps"
    ]
    + phase57_premise_steps
  )

  rules = (
    phase55[
      "rules"
    ]
    + (
      zero_equality_implies_zero_inference_rule(),
      toda_lemma45_n4_two_iota3_composition_inference_rule(),
      toda_lemma52_prop26_first_zero_inference_rule(),
      toda_prop26_lemma52_hopf_bracket_inference_rule(),
      toda_lemma52_delta_two_eta2_preimage_inference_rule(),
      toda_prop14_lemma52_bracket_transformation_inference_rule(),
      toda_prop13_lemma52_bracket_transformation_inference_rule(),
      toda_cor37_lemma52_representative_inference_rule(),
      toda_prop51_eta4_twice_zero_inference_rule(),
      toda_21_lemma52_suspended_indeterminacy_zero_inference_rule(),
      toda_lemma45_n4_suspension_zero_reflection_inference_rule(),
      toda_lemma52_hopf_value_inference_rule(),
      toda_lemma52_double_value_inference_rule(),
      toda_lemma52_beta_membership_inference_rule(),
      toda_lemma52_delta_e2_alpha_zero_inference_rule(),
    )
  )

  expected_hopf_relation = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=beta,
    ),
    rhs=IteratedSuspension(
      expression=alpha,
      exponent=2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  expected_double_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=beta,
    ),
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

  expected_beta_membership = (
    HomotopyGroupMembershipStatement(
      element=beta,
      group_dimension=i_plus_two,
      sphere_dimension=3,
    )
  )

  expected_delta_zero = Relation(
    lhs=MapApplication(
      map=EHP_DELTA_MAP,
      expression=IteratedSuspension(
        expression=alpha,
        exponent=2,
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  hopf_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_hopf_relation
    )
  )

  double_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_double_relation
    )
  )

  beta_membership_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_beta_membership
    )
  )

  delta_zero_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_delta_zero
    )
  )

  return {
    "phase55": phase55,
    "i": i,
    "i_plus_one": i_plus_one,
    "i_plus_two": i_plus_two,
    "alpha": alpha,
    "beta": beta,
    "gamma": gamma,
    "eta_3": eta_3,
    "eta_i_plus_one": eta_i_plus_one,
    "alpha_membership": alpha_membership,
    "two_alpha_zero": two_alpha_zero,
    "bracket": bracket,
    "bracket_membership": (
      bracket_membership
    ),
    "gamma_membership": gamma_membership,
    "phase57_premise_steps": (
      phase57_premise_steps
    ),
    "premise_steps": premise_steps,
    "rules": rules,
    "expected_hopf_relation": (
      expected_hopf_relation
    ),
    "expected_double_relation": (
      expected_double_relation
    ),
    "expected_beta_membership": (
      expected_beta_membership
    ),
    "expected_delta_zero": (
      expected_delta_zero
    ),
    "result": result,
    "hopf_steps": hopf_steps,
    "double_steps": double_steps,
    "beta_membership_steps": (
      beta_membership_steps
    ),
    "delta_zero_steps": (
      delta_zero_steps
    ),
  }


def print_phase57_result(
  representative,
):
  print()
  print_separator()
  print(
    "Toda Lemma 5.2"
  )
  print_separator()
  print()

  print(
    "  α ∈ π_i(S^3)"
  )
  print(
    "  2α = 0"
  )
  print(
    "  β ∈ {η₃, 2ι₄, Eα}_1"
  )
  print()
  print(
    "  ↓"
  )
  print()
  print(
    "  H(β) = E²α"
  )
  print(
    "  2β = η₃∘Eα∘η_(i+1)"
  )
  print(
    "  β ∈ π_(i+2)^3"
  )
  print(
    "  Δ(E²α) = 0"
  )


def print_phase57_rounds(
  representative,
):
  print()
  print_separator()
  print(
    "Inference rounds"
  )
  print_separator()
  print()

  for index, round_result in enumerate(
    representative[
      "result"
    ].round_results,
    start=1,
  ):
    print(
      "round",
      index,
      "new step count =",
      len(
        round_result.new_steps
      ),
    )


def print_phase57_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / integration"
  )
  print_separator()
  print()

  final_groups = (
    representative[
      "hopf_steps"
    ],
    representative[
      "double_steps"
    ],
    representative[
      "beta_membership_steps"
    ],
    representative[
      "delta_zero_steps"
    ],
  )

  print(
    "H(beta)=E^2 alpha derived =",
    len(
      final_groups[
        0
      ]
    ) == 1,
  )

  print(
    "2 beta relation derived =",
    len(
      final_groups[
        1
      ]
    ) == 1,
  )

  print(
    "beta membership derived =",
    len(
      final_groups[
        2
      ]
    ) == 1,
  )

  print(
    "Delta(E^2 alpha)=0 derived =",
    len(
      final_groups[
        3
      ]
    ) == 1,
  )

  print(
    "all final results are INFERENCE =",
    all(
      len(
        steps
      ) == 1
      and steps[
        0
      ].rule
      == ProofRule.INFERENCE
      for steps in final_groups
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
      expected
      in initial_conclusions
      for expected in (
        representative[
          "expected_hopf_relation"
        ],
        representative[
          "expected_double_relation"
        ],
        representative[
          "expected_beta_membership"
        ],
        representative[
          "expected_delta_zero"
        ],
      )
    ),
  )

  print(
    "fixed point =",
    (
      representative[
        "result"
      ].termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase57_boundary():
  print()
  print_separator()
  print(
    "Phase 57 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  Toda Lemma 5.2 end-to-end integration"
  )
  print(
    "  H(beta)=E^2 alpha"
  )
  print(
    "  2 beta=eta_3 o E alpha o eta_(i+1)"
  )
  print(
    "  beta in pi_(i+2)^3"
  )
  print(
    "  Delta(E^2 alpha)=0"
  )
  print(
    "  derived provenance"
  )

  print()
  print(
    "Still outside Phase 57:"
  )
  print(
    "  generic Toda-bracket coset algebra"
  )
  print(
    "  generic inverse-image algebra"
  )
  print(
    "  generic sign normalization"
  )
  print(
    "  generic Delta-H rewrite framework"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 57 capability demonstration"
  )

  representative = (
    build_phase57_representative_result()
  )

  print_phase57_result(
    representative
  )

  print_phase57_rounds(
    representative
  )

  print_phase57_provenance(
    representative
  )

  print_phase57_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


