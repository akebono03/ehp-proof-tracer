from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase55_capabilities import (
  build_phase55_representative_result,
  main,
)
from toda_rules import (
  TodaProp51FiniteDimensionalStatement,
)


def test_phase55_probe_derives_all_four_dependencies():
  representative = (
    build_phase55_representative_result()
  )

  dependency_steps = (
    representative[
      "pi3_2_group_steps"
    ],
    representative[
      "eta2_hopf_steps"
    ],
    representative[
      "delta_two_eta_2_steps"
    ],
    representative[
      "higher_eta_group_steps"
    ],
  )

  assert all(
    len(
      steps
    ) == 1
    for steps in dependency_steps
  )

  assert all(
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
    for steps in dependency_steps
  )


def test_phase55_probe_derives_final_prop51_statement():
  representative = (
    build_phase55_representative_result()
  )

  steps = representative[
    "prop51_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaProp51FiniteDimensionalStatement,
  )

  assert steps[
    0
  ].rule == (
    ProofRule.INFERENCE
  )


def test_phase55_probe_final_statement_preserves_four_derived_premises():
  representative = (
    build_phase55_representative_result()
  )

  step = representative[
    "prop51_steps"
  ][
    0
  ]

  expected_premises = (
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

  assert len(
    step.premises
  ) == 4

  assert (
    step.premises
    == expected_premises
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )


def test_phase55_probe_does_not_reintroduce_phase49_results_as_given():
  representative = (
    build_phase55_representative_result()
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in representative[
      "premise_steps"
    ]
  )

  assert (
    representative[
      "eta2_hopf_relation"
    ]
    not in initial_conclusions
  )

  assert (
    representative[
      "pi3_2_group_relation"
    ]
    not in initial_conclusions
  )


def test_phase55_probe_does_not_use_prop51_result_as_given():
  representative = (
    build_phase55_representative_result()
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in representative[
      "premise_steps"
    ]
  )

  assert (
    representative[
      "expected_statement"
    ]
    not in initial_conclusions
  )


def test_phase55_probe_reaches_fixed_point():
  representative = (
    build_phase55_representative_result()
  )

  assert (
    representative[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase55_probe_final_result_occurs_in_last_round():
  representative = (
    build_phase55_representative_result()
  )

  final_step = (
    representative[
      "prop51_steps"
    ][
      0
    ]
  )

  assert final_step in (
    representative[
      "result"
    ]
    .round_results[
      -1
    ]
    .new_steps
  )


def test_phase55_probe_output_contains_results_provenance_and_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 55 capability demonstration"
    in output
  )

  assert (
    "π_3^2 = Z{η₂}"
    in output
  )

  assert (
    "H(η₂) = ι₃"
    in output
  )

  assert (
    "Δ(ι₅) = ±2η₂"
    in output
  )

  assert (
    "π_(n+1)^n = Z/2{η_n}"
    in output
  )

  assert (
    "final Prop.5.1 result is derived = True"
    in output
  )

  assert (
    "final premise count = 4"
    in output
  )

  assert (
    "final premises are derived = True"
    in output
  )

  assert (
    "H(eta_2)=iota_3 is GIVEN premise = False"
    in output
  )

  assert (
    "pi_3^2 result is GIVEN premise = False"
    in output
  )

  assert (
    "Prop.5.1 result is GIVEN premise = False"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )

  assert (
    "stable (G_1;2)=Z/2{eta}"
    in output
  )

  assert (
    "composition isomorphism (5.2)"
    in output
  )



