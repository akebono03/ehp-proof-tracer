from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase58_capabilities import (
  build_phase58_representative_result,
  main,
)


def test_phase58_probe_derives_all_toda53_conclusions():
  representative = (
    build_phase58_representative_result()
  )

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

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in final_steps
  )

  assert (
    final_steps[
      0
    ].conclusion
    == representative[
      "expected_membership"
    ]
  )

  assert (
    final_steps[
      1
    ].conclusion
    == representative[
      "expected_final_hopf"
    ]
  )

  assert (
    final_steps[
      2
    ].conclusion
    == representative[
      "expected_final_double"
    ]
  )


def test_phase58_probe_does_not_use_final_results_as_given():
  representative = (
    build_phase58_representative_result()
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in representative[
      "premise_steps"
    ]
  )

  assert (
    representative[
      "expected_membership"
    ]
    not in initial_conclusions
  )

  assert (
    representative[
      "expected_final_hopf"
    ]
    not in initial_conclusions
  )

  assert (
    representative[
      "expected_final_double"
    ]
    not in initial_conclusions
  )


def test_phase58_probe_raw_results_share_phase58_3_stage():
  representative = (
    build_phase58_representative_result()
  )

  result = representative[
    "phase58_3_result"
  ]

  assert (
    representative[
      "raw_hopf_step"
    ]
    in result.steps
  )

  assert (
    representative[
      "raw_double_step"
    ]
    in result.steps
  )

  assert (
    representative[
      "membership_step"
    ]
    in result.steps
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase58_probe_hopf_provenance_connects_raw_value_and_eta5_bridge():
  representative = (
    build_phase58_representative_result()
  )

  final_step = representative[
    "final_hopf_step"
  ]

  assert (
    final_step.premises
    == (
      representative[
        "raw_hopf_step"
      ],
      representative[
        "eta5_bridge_step"
      ],
    )
  )

  assert (
    final_step.rule
    == ProofRule.INFERENCE
  )


def test_phase58_probe_double_provenance_connects_raw_value_and_composition_bridge():
  representative = (
    build_phase58_representative_result()
  )

  final_step = representative[
    "final_double_step"
  ]

  assert (
    final_step.premises
    == (
      representative[
        "raw_double_step"
      ],
      representative[
        "composition_step"
      ],
    )
  )

  assert (
    representative[
      "composition_step"
    ].premises
    == (
      representative[
        "right_step"
      ],
    )
  )

  assert (
    representative[
      "right_step"
    ].premises
    == (
      representative[
        "eta4_bridge_step"
      ],
    )
  )


def test_phase58_probe_safe_stages_reach_fixed_point():
  representative = (
    build_phase58_representative_result()
  )

  results = (
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

  assert all(
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
    for result in results
  )


def test_phase58_probe_composition_propagation_is_one_shot():
  representative = (
    build_phase58_representative_result()
  )

  assert (
    representative[
      "right_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    representative[
      "composition_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    representative[
      "right_step"
    ].premises
    == (
      representative[
        "eta4_bridge_step"
      ],
    )
  )


def test_phase58_probe_output_contains_final_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 58 capability demonstration"
    in output
  )

  assert (
    "ν′ ∈ π_6^3"
    in output
  )

  assert (
    "H(ν′) = η₅"
    in output
  )

  assert (
    "2ν′ = η₃∘η₄∘η₅"
    in output
  )

  assert (
    "all final results are INFERENCE = True"
    in output
  )

  assert (
    "final results are GIVEN = False"
    in output
  )

  assert (
    "fixed-point-safe stages complete = True"
    in output
  )

  assert (
    "composition propagation one-shot = True"
    in output
  )

  assert (
    "shared raw specialization = True"
    in output
  )


def test_phase58_probe_uses_derived_two_eta3_zero_premise():
  representative = (
    build_phase58_representative_result()
  )

  step = representative[
    "two_eta3_zero_step"
  ]

  assert (
    step.conclusion
    == representative[
      "expected_two_eta3_zero"
    ]
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.premises
    == (
      representative[
        "pi4_3_step"
      ],
    )
  )

