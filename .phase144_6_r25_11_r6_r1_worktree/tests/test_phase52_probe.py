from expression import (
  Multiple,
  WhiteheadProduct,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase52_capabilities import (
  build_phase52_representative_result,
  main,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
)


def test_phase52_probe_reuses_eleven_given_premises():
  representative = (
    build_phase52_representative_result()
  )

  assert len(
    representative[
      "premise_steps"
    ]
  ) == 11

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in representative[
      "premise_steps"
    ]
  )


def test_phase52_probe_has_original_delta_whitehead_statement():
  representative = (
    build_phase52_representative_result()
  )

  steps = representative[
    "delta_whitehead_steps"
  ]

  assert len(
    steps
  ) == 1

  statement = steps[
    0
  ].conclusion

  assert isinstance(
    statement,
    TodaDeltaImageUpToSignStatement,
  )

  assert isinstance(
    statement.positive_value,
    WhiteheadProduct,
  )


def test_phase52_probe_has_whitehead_two_eta2_statement():
  representative = (
    build_phase52_representative_result()
  )

  steps = representative[
    "whitehead_two_eta_2_steps"
  ]

  assert len(
    steps
  ) == 1

  statement = steps[
    0
  ].conclusion

  assert isinstance(
    statement,
    TodaPi32WhiteheadSquareUpToSignStatement,
  )

  assert statement.positive_value == (
    Multiple(
      coefficient=2,
      expression=representative[
        "eta_2"
      ],
    )
  )


def test_phase52_probe_derives_direct_delta_two_eta2_statement():
  representative = (
    build_phase52_representative_result()
  )

  steps = representative[
    "delta_two_eta_2_steps"
  ]

  assert len(
    steps
  ) == 1

  statement = steps[
    0
  ].conclusion

  assert isinstance(
    statement,
    TodaDeltaImageUpToSignStatement,
  )

  assert statement.positive_value == (
    Multiple(
      coefficient=2,
      expression=representative[
        "eta_2"
      ],
    )
  )


def test_phase52_probe_direct_bridge_has_expected_provenance():
  representative = (
    build_phase52_representative_result()
  )

  step = representative[
    "delta_two_eta_2_steps"
  ][
    0
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule is not None

  assert (
    step.inference_rule.name
    == (
      "Toda Delta iota_5 "
      "twice eta_2 up-to-sign bridge"
    )
  )

  assert len(
    step.premises
  ) == 2

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )


def test_phase52_probe_round_three_contains_direct_bridge():
  representative = (
    build_phase52_representative_result()
  )

  third_round = (
    representative[
      "result"
    ]
    .round_results[
      2
    ]
    .new_steps
  )

  bridge_step = (
    representative[
      "delta_two_eta_2_steps"
    ][
      0
    ]
  )

  assert bridge_step in (
    third_round
  )


def test_phase52_probe_has_ten_derived_steps_and_six_rounds():
  representative = (
    build_phase52_representative_result()
  )

  result = representative[
    "result"
  ]

  derived_steps = tuple(
    step
    for step in result.steps
    if step.rule
    == ProofRule.INFERENCE
  )

  assert len(
    derived_steps
  ) == 10

  assert result.round_count == 6

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase52_probe_output_contains_direct_bridge(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 52 capability demonstration"
    in output
  )

  assert (
    "Δ(ι_5) = ±[ι_2,ι_2]"
    in output
  )

  assert (
    "[ι_2,ι_2] = ±2η₂"
    in output
  )

  assert (
    "Δ(ι_5) = ±2η₂"
    in output
  )

  assert (
    "bridge premise count = 2"
    in output
  )

  assert (
    "bridge premises are derived = True"
    in output
  )

  assert (
    "bridge result is derived = True"
    in output
  )

  assert (
    "given premise count = 11"
    in output
  )

  assert (
    "derived step count = 10"
    in output
  )

  assert (
    "derived round count = 6"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )


