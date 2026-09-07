from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  run_inference_until_stable_with_history,
)
from probes.probe_phase49_capabilities import (
  build_phase49_representative_result,
)
from probes.probe_phase50_capabilities import (
  build_phase50_representative_result,
  print_separator,
)
from probes.probe_phase53_capabilities import (
  build_phase53_representative_result,
)
from probes.probe_phase54_capabilities import (
  build_phase54_representative_result,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaProp51FiniteDimensionalStatement,
  toda_delta_iota5_two_eta2_up_to_sign_inference_rule,
  toda_prop51_finite_dimensional_integration_inference_rule,
)


def build_phase55_representative_result():
  phase49 = (
    build_phase49_representative_result()
  )

  phase50 = (
    build_phase50_representative_result()
  )

  phase53 = (
    build_phase53_representative_result()
  )

  phase54 = (
    build_phase54_representative_result()
  )

  phase49_known_conclusions = tuple(
    step.conclusion
    for step in phase49[
      "result"
    ].steps
  )

  phase50_additional_premises = tuple(
    step
    for step in phase50[
      "premise_steps"
    ]
    if (
      step.conclusion
      not in phase49_known_conclusions
    )
  )

  phase53_additional_premises = (
    phase53[
      "premise_steps"
    ][
      len(
        phase50[
          "premise_steps"
        ]
      ):
    ]
  )

  phase54_additional_premises = (
    phase54[
      "premise_steps"
    ][
      len(
        phase53[
          "premise_steps"
        ]
      ):
    ]
  )

  premise_steps = (
    phase49[
      "premise_steps"
    ]
    + phase50_additional_premises
    + phase53_additional_premises
    + phase54_additional_premises
  )

  phase53_additional_rules = (
    phase53[
      "rules"
    ][
      len(
        phase50[
          "rules"
        ]
      ):
    ]
  )

  phase54_additional_rules = (
    phase54[
      "rules"
    ][
      len(
        phase53[
          "rules"
        ]
      ):
    ]
  )

  rules = (
    phase49[
      "rules"
    ]
    + phase50[
      "rules"
    ]
    + phase53_additional_rules
    + phase54_additional_rules
    + (
      toda_delta_iota5_two_eta2_up_to_sign_inference_rule(),
      toda_prop51_finite_dimensional_integration_inference_rule(),
    )
  )

  eta_2 = phase50[
    "eta_2"
  ]

  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )

  delta_two_eta_2_relation = (
    TodaDeltaImageUpToSignStatement(
      map=phase50[
        "delta_map"
      ],
      element=iota_5,
      positive_value=Multiple(
        coefficient=2,
        expression=eta_2,
      ),
    )
  )

  pi3_2_group_relation = (
    phase50[
      "pi_3_2_relation"
    ]
  )

  eta2_hopf_relation = (
    phase50[
      "eta_2_hopf_relation"
    ]
  )

  higher_eta_group_relation = (
    phase54[
      "final_relation"
    ]
  )

  expected_statement = (
    TodaProp51FiniteDimensionalStatement(
      pi3_2_group_relation=(
        pi3_2_group_relation
      ),
      eta2_hopf_relation=(
        eta2_hopf_relation
      ),
      delta_iota5_relation=(
        delta_two_eta_2_relation
      ),
      higher_eta_group_relation=(
        higher_eta_group_relation
      ),
    )
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  pi3_2_group_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == pi3_2_group_relation
    )
  )

  eta2_hopf_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == eta2_hopf_relation
    )
  )

  delta_two_eta_2_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == delta_two_eta_2_relation
    )
  )

  higher_eta_group_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == higher_eta_group_relation
    )
  )

  prop51_steps = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_statement
    )
  )

  return {
    "phase49": phase49,
    "phase50": phase50,
    "phase53": phase53,
    "phase54": phase54,
    "premise_steps": premise_steps,
    "rules": rules,
    "result": result,
    "pi3_2_group_relation": (
      pi3_2_group_relation
    ),
    "eta2_hopf_relation": (
      eta2_hopf_relation
    ),
    "delta_two_eta_2_relation": (
      delta_two_eta_2_relation
    ),
    "higher_eta_group_relation": (
      higher_eta_group_relation
    ),
    "expected_statement": (
      expected_statement
    ),
    "pi3_2_group_steps": (
      pi3_2_group_steps
    ),
    "eta2_hopf_steps": (
      eta2_hopf_steps
    ),
    "delta_two_eta_2_steps": (
      delta_two_eta_2_steps
    ),
    "higher_eta_group_steps": (
      higher_eta_group_steps
    ),
    "prop51_steps": prop51_steps,
  }


def print_phase55_finite_dimensional_results(
  representative,
):
  print()
  print_separator()
  print(
    "Toda Proposition 5.1 "
    "finite-dimensional results"
  )
  print_separator()
  print()

  print(
    "  π_3^2 = Z{η₂}"
  )

  print(
    "  H(η₂) = ι₃"
  )

  print(
    "  Δ(ι₅) = ±2η₂"
  )

  print(
    "  π_(n+1)^n = Z/2{η_n}"
  )

  print()
  print(
    "  ↓"
  )

  print()

  print(
    "  Toda Proposition 5.1"
  )

  print(
    "  finite-dimensional result"
  )


def print_phase55_rounds(
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


def print_phase55_provenance(
  representative,
):
  print()
  print_separator()
  print(
    "Provenance / circular dependency"
  )
  print_separator()
  print()

  result = representative[
    "result"
  ]

  final_step = (
    representative[
      "prop51_steps"
    ][
      0
    ]
  )

  dependency_steps = (
    representative[
      "pi3_2_group_steps"
    ][
      0
    ],
    representative[
      "eta2_hopf_steps"
    ][
      0
    ],
    representative[
      "delta_two_eta_2_steps"
    ][
      0
    ],
    representative[
      "higher_eta_group_steps"
    ][
      0
    ],
  )

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
    "pi_3^2 result is derived =",
    (
      dependency_steps[
        0
      ].rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "H(eta_2)=iota_3 is derived =",
    (
      dependency_steps[
        1
      ].rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "Delta(iota_5)=+-2eta_2 is derived =",
    (
      dependency_steps[
        2
      ].rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "higher eta group is derived =",
    (
      dependency_steps[
        3
      ].rule
      == ProofRule.INFERENCE
    ),
  )

  print(
    "final Prop.5.1 result is derived =",
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
    "H(eta_2)=iota_3 is GIVEN premise =",
    (
      representative[
        "eta2_hopf_relation"
      ]
      in initial_conclusions
    ),
  )

  print(
    "pi_3^2 result is GIVEN premise =",
    (
      representative[
        "pi3_2_group_relation"
      ]
      in initial_conclusions
    ),
  )

  print(
    "Prop.5.1 result is GIVEN premise =",
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


def print_phase55_boundary():
  print()
  print_separator()
  print(
    "Phase 55 boundary"
  )
  print_separator()
  print()

  print(
    "Implemented:"
  )

  print(
    "  finite-dimensional "
    "Proposition 5.1 integration"
  )

  print(
    "  four independently derived premises"
  )

  print(
    "  circular-dependency rejection"
  )

  print(
    "  derived provenance"
  )

  print()
  print(
    "Still outside Phase 55:"
  )

  print(
    "  stable (G_1;2)=Z/2{eta}"
  )

  print(
    "  stable homotopy-group model"
  )

  print(
    "  composition isomorphism (5.2)"
  )

  print(
    "  generic cyclic-generator rewrite"
  )

  print(
    "  generic suspension normalization"
  )


def main():
  print()
  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 55 capability demonstration"
  )

  representative = (
    build_phase55_representative_result()
  )

  print_phase55_finite_dimensional_results(
    representative
  )

  print_phase55_rounds(
    representative
  )

  print_phase55_provenance(
    representative
  )

  print_phase55_boundary()

  print()
  print_separator()
  print(
    "Demo complete"
  )
  print_separator()


if __name__ == "__main__":
  main()


