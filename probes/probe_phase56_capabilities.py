from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
  TodaProp44DecompositionMap,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  run_inference_until_stable_with_history,
)
from probes.probe_phase49_capabilities import (
  build_phase49_representative_result,
  print_separator,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  toda_52_eta2_composition_isomorphism_inference_rule,
  toda_pi_i_minus_1_1_zero_inference_rule,
  toda_prop44_eta2_n2_isomorphism_inference_rule,
  toda_prop44_eta2_second_summand_restriction_inference_rule,
)


def build_phase56_representative_result():
  phase49 = (
    build_phase49_representative_result()
  )

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

  source_group = DirectSumGroup(
    summands=(
      first_summand,
      second_summand,
    ),
  )

  target_group = TodaPrimaryGroup(
    group_dimension=i,
    sphere_dimension=2,
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=source_group,
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
  )

  lower_bound = (
    ScalarGreaterEqualStatement(
      left=i,
      right=3,
    )
  )

  lower_bound_step = ProofStep(
    conclusion=lower_bound,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  decomposition_map_step = ProofStep(
    conclusion=decomposition_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  premise_steps = (
    phase49[
      "premise_steps"
    ]
    + (
      lower_bound_step,
      decomposition_map_step,
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

  expected_zero = (
    TodaPrimaryGroupZeroStatement(
      group=first_summand,
    )
  )

  expected_isomorphism = (
    TodaProp44IsomorphismStatement(
      map=decomposition_map,
    )
  )

  expected_restriction = (
    TodaProp44SecondSummandRestrictionStatement(
      decomposition_map=decomposition_map,
      composition=Composition(
        left=eta_2,
        right=gamma,
      ),
    )
  )

  expected_statement = (
    Toda52CompositionIsomorphismStatement(
      source_group=second_summand,
      target_group=target_group,
      composition=Composition(
        left=eta_2,
        right=gamma,
      ),
    )
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  eta_2_definition_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      in tuple(
        phase49_step.conclusion
        for phase49_step in phase49[
          "eta_2_definition_steps"
        ]
      )
    )
  )

  hopf_relation_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      in tuple(
        phase49_step.conclusion
        for phase49_step in phase49[
          "hopf_relation_steps"
        ]
      )
    )
  )

  zero_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_zero
    )
  )

  isomorphism_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_isomorphism
    )
  )

  restriction_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_restriction
    )
  )

  composition_isomorphism_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase49": phase49,
    "i": i,
    "eta_2": eta_2,
    "beta": beta,
    "gamma": gamma,
    "first_summand": first_summand,
    "second_summand": second_summand,
    "target_group": target_group,
    "lower_bound": lower_bound,
    "decomposition_map": decomposition_map,
    "lower_bound_step": lower_bound_step,
    "decomposition_map_step": (
      decomposition_map_step
    ),
    "premise_steps": premise_steps,
    "rules": rules,
    "expected_zero": expected_zero,
    "expected_isomorphism": (
      expected_isomorphism
    ),
    "expected_restriction": (
      expected_restriction
    ),
    "expected_statement": (
      expected_statement
    ),
    "result": result,
    "eta_2_definition_steps": (
      eta_2_definition_steps
    ),
    "hopf_relation_steps": (
      hopf_relation_steps
    ),
    "zero_steps": zero_steps,
    "isomorphism_steps": (
      isomorphism_steps
    ),
    "restriction_steps": (
      restriction_steps
    ),
    "composition_isomorphism_steps": (
      composition_isomorphism_steps
    ),
  }


def print_phase56_result(
  representative,
):
  print()
  print_separator()
  print(
    "Toda (5.2) composition isomorphism"
  )
  print_separator()
  print()

  print(
    "  i ≥ 3"
  )
  print(
    "  ↓"
  )
  print(
    "  π_(i-1)^1 = 0"
  )
  print()
  print(
    "  H(η₂) = ι₃"
  )
  print(
    "  ↓"
  )
  print(
    "  Φ:"
  )
  print(
    "  π_(i-1)^1 ⊕ π_i^3 ≅ π_i^2"
  )
  print()
  print(
    "  Φ|_(π_i^3)(γ) = η₂∘γ"
  )
  print(
    "  ↓"
  )
  print(
    "  η₂∘- : π_i^3 ≅ π_i^2"
  )


def print_phase56_rounds(
  representative,
):
  print()
  print_separator()
  print(
    "Inference rounds"
  )
  print_separator()
  print()

  result = representative[
    "result"
  ]

  for index, round_result in enumerate(
    result.round_results,
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


def print_phase56_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / applicability"
  )
  print_separator()
  print()

  result = representative[
    "result"
  ]

  zero_step = representative[
    "zero_steps"
  ][
    0
  ]

  isomorphism_step = representative[
    "isomorphism_steps"
  ][
    0
  ]

  restriction_step = representative[
    "restriction_steps"
  ][
    0
  ]

  final_step = representative[
    "composition_isomorphism_steps"
  ][
    0
  ]

  initial_conclusions = tuple(
    step.conclusion
    for step in representative[
      "premise_steps"
    ]
  )

  derived_steps = tuple(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
    )
  )

  print(
    "pi_(i-1)^1=0 is derived =",
    (
      zero_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "Prop.4.4 n=2 specialization is derived =",
    (
      isomorphism_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "second-summand restriction is derived =",
    (
      restriction_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "Toda (5.2) result is derived =",
    (
      final_step.rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "final rule =",
    final_step
    .inference_rule
    .name,
  )

  print(
    "final premise count =",
    len(
      final_step.premises
    ),
  )

  print(
    "final premises are derived =",
    all(
      premise.rule
      == ProofRule.INFERENCE
      for premise in final_step.premises
    ),
  )

  print(
    "pi_(i-1)^1=0 is GIVEN premise =",
    (
      representative[
        "expected_zero"
      ]
      in initial_conclusions
    ),
  )

  print(
    "Prop.4.4 specialization is GIVEN premise =",
    (
      representative[
        "expected_isomorphism"
      ]
      in initial_conclusions
    ),
  )

  print(
    "second-summand restriction is GIVEN premise =",
    (
      representative[
        "expected_restriction"
      ]
      in initial_conclusions
    ),
  )

  print(
    "Toda (5.2) result is GIVEN premise =",
    (
      representative[
        "expected_statement"
      ]
      in initial_conclusions
    ),
  )

  print(
    "given premise count =",
    len(
      representative[
        "premise_steps"
      ]
    ),
  )

  print(
    "derived step count =",
    len(
      derived_steps
    ),
  )

  print(
    "derived round count =",
    result.round_count,
  )

  print(
    "fixed point =",
    (
      result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    ),
  )


def print_phase56_boundary():
  print()
  print_separator()
  print(
    "Phase 56 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )
  print(
    "  pi_(i-1)^1 zero for i at least 3"
  )
  print(
    "  Proposition 4.4 n=2 eta_2 specialization"
  )
  print(
    "  second-summand restriction"
  )
  print(
    "  Toda (5.2) eta_2 composition isomorphism"
  )
  print(
    "  end-to-end derived provenance"
  )

  print()
  print(
    "Still outside Phase 56:"
  )
  print(
    "  Toda Lemma 5.2 proof integration"
  )
  print(
    "  generic direct-sum reduction"
  )
  print(
    "  generic composition-map framework"
  )
  print(
    "  generic scalar normalization"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 56 capability demonstration"
  )

  representative = (
    build_phase56_representative_result()
  )

  print_phase56_result(
    representative
  )

  print_phase56_rounds(
    representative
  )

  print_phase56_provenance(
    representative
  )

  print_phase56_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()




