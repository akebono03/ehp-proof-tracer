from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase54_capabilities import (
  build_phase54_representative_result,
  main,
)


def test_phase54_probe_has_fifteen_given_premises():
  representative = (
    build_phase54_representative_result()
  )

  assert len(
    representative[
      "premise_steps"
    ]
  ) == 15

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in representative[
      "premise_steps"
    ]
  )


def test_phase54_probe_phase53_transport_is_derived():
  representative = (
    build_phase54_representative_result()
  )

  steps = representative[
    "transported_steps"
  ]

  assert len(
    steps
  ) == 1

  assert steps[
    0
  ].rule == (
    ProofRule.INFERENCE
  )


def test_phase54_probe_higher_eta_bridge_is_derived():
  representative = (
    build_phase54_representative_result()
  )

  steps = representative[
    "higher_eta_steps"
  ]

  assert len(
    steps
  ) == 1

  step = steps[
    0
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule is not None

  assert (
    step.inference_rule.name
    == (
      "Toda higher eta-family "
      "iterated suspension bridge"
    )
  )


def test_phase54_probe_derives_final_finite_cyclic_group():
  representative = (
    build_phase54_representative_result()
  )

  steps = representative[
    "final_steps"
  ]

  assert len(
    steps
  ) == 1

  relation = (
    steps[
      0
    ].conclusion
  )

  assert relation == (
    representative[
      "final_relation"
    ]
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert (
    relation.rhs.generator
    == representative[
      "eta_n_definition"
    ].element
  )


def test_phase54_probe_final_result_preserves_derived_provenance():
  representative = (
    build_phase54_representative_result()
  )

  step = representative[
    "final_steps"
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
      "Toda higher eta-family "
      "finite-cyclic generator bridge"
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

  assert (
    representative[
      "transported_steps"
    ][
      0
    ]
    in step.premises
  )

  assert (
    representative[
      "higher_eta_steps"
    ][
      0
    ]
    in step.premises
  )


def test_phase54_probe_has_thirteen_derived_steps_and_eight_rounds():
  representative = (
    build_phase54_representative_result()
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
  ) == 13

  assert result.round_count == 8

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase54_probe_round_eight_contains_final_group():
  representative = (
    build_phase54_representative_result()
  )

  final_step = (
    representative[
      "final_steps"
    ][
      0
    ]
  )

  eighth_round = (
    representative[
      "result"
    ]
    .round_results[
      7
    ]
    .new_steps
  )

  assert final_step in (
    eighth_round
  )


def test_phase54_probe_output_contains_bridge_final_group_and_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 54 capability demonstration"
    in output
  )

  assert (
    "η_n = E^(n-2)η₂"
    in output
  )

  assert (
    "η₃ = Eη₂"
    in output
  )

  assert (
    "E^(n-3)η₃ = η_n"
    in output
  )

  assert (
    "π_(n+1)^n "
    "= Z/2{E^(n-3)η₃}"
    in output
  )

  assert (
    "π_(n+1)^n "
    "= Z/2{η_n}"
    in output
  )

  assert (
    "source group result is derived = True"
    in output
  )

  assert (
    "transport result is derived = True"
    in output
  )

  assert (
    "higher eta bridge is derived = True"
    in output
  )

  assert (
    "final group result is derived = True"
    in output
  )

  assert (
    "final premise count = 2"
    in output
  )

  assert (
    "final premises are derived = True"
    in output
  )

  assert (
    "given premise count = 15"
    in output
  )

  assert (
    "derived step count = 13"
    in output
  )

  assert (
    "derived round count = 8"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )

  assert (
    "generic cyclic-generator rewrite"
    in output
  )

  assert (
    "Proposition 5.1 integration"
    in output
  )


