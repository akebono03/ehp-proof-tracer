from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase57_capabilities import (
  build_phase57_representative_result,
  main,
)


def test_phase57_probe_derives_all_lemma52_conclusions():
  representative = (
    build_phase57_representative_result()
  )

  groups = (
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

  assert all(
    len(
      steps
    ) == 1
    for steps in groups
  )

  assert all(
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
    for steps in groups
  )


def test_phase57_probe_does_not_use_final_results_as_given():
  representative = (
    build_phase57_representative_result()
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in representative[
      "premise_steps"
    ]
  )

  assert (
    representative[
      "expected_hopf_relation"
    ]
    not in initial_conclusions
  )

  assert (
    representative[
      "expected_double_relation"
    ]
    not in initial_conclusions
  )

  assert (
    representative[
      "expected_beta_membership"
    ]
    not in initial_conclusions
  )

  assert (
    representative[
      "expected_delta_zero"
    ]
    not in initial_conclusions
  )


def test_phase57_probe_reaches_fixed_point():
  representative = (
    build_phase57_representative_result()
  )

  assert (
    representative[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase57_probe_output_contains_final_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 57 capability demonstration"
    in output
  )

  assert (
    "H(β) = E²α"
    in output
  )

  assert (
    "2β = η₃∘Eα∘η_(i+1)"
    in output
  )

  assert (
    "β ∈ π_(i+2)^3"
    in output
  )

  assert (
    "Δ(E²α) = 0"
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
    "fixed point = True"
    in output
  )


