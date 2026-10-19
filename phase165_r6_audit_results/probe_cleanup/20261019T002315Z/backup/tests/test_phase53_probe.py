from expression import (
  IteratedSuspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase53_capabilities import (
  build_phase53_representative_result,
  main,
)
from toda_rules import (
  Toda45IsomorphismStatement,
)


def test_phase53_probe_has_fourteen_given_premises():
  representative = (
    build_phase53_representative_result()
  )

  assert len(
    representative[
      "premise_steps"
    ]
  ) == 14

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in representative[
      "premise_steps"
    ]
  )


def test_phase53_probe_phase50_source_group_is_derived():
  representative = (
    build_phase53_representative_result()
  )

  steps = representative[
    "phase50_final_steps"
  ]

  assert len(
    steps
  ) == 1

  assert steps[
    0
  ].rule == (
    ProofRule.INFERENCE
  )


def test_phase53_probe_toda45_isomorphism_is_derived():
  representative = (
    build_phase53_representative_result()
  )

  steps = representative[
    "toda45_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    Toda45IsomorphismStatement,
  )

  assert steps[
    0
  ].rule == (
    ProofRule.INFERENCE
  )


def test_phase53_probe_derives_transported_finite_cyclic_group():
  representative = (
    build_phase53_representative_result()
  )

  steps = representative[
    "transported_steps"
  ]

  assert len(
    steps
  ) == 1

  relation = (
    steps[
      0
    ].conclusion
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert isinstance(
    relation.rhs.generator,
    IteratedSuspension,
  )

  assert (
    relation
    .rhs
    .generator
    .expression
    == representative[
      "phase50"
    ][
      "eta_3"
    ]
  )

  assert (
    relation
    .rhs
    .generator
    .exponent
    == representative[
      "suspension_map"
    ].exponent
  )


def test_phase53_probe_transport_preserves_derived_provenance():
  representative = (
    build_phase53_representative_result()
  )

  step = representative[
    "transported_steps"
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
      "Toda 4.5 pi_4^3 "
      "finite-cyclic transport"
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
      "phase50_final_steps"
    ][
      0
    ]
    in step.premises
  )

  assert (
    representative[
      "toda45_steps"
    ][
      0
    ]
    in step.premises
  )


def test_phase53_probe_has_eleven_derived_steps_and_seven_rounds():
  representative = (
    build_phase53_representative_result()
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
  ) == 11

  assert result.round_count == 7

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase53_probe_round_seven_contains_transport():
  representative = (
    build_phase53_representative_result()
  )

  transport_step = (
    representative[
      "transported_steps"
    ][
      0
    ]
  )

  seventh_round = (
    representative[
      "result"
    ]
    .round_results[
      6
    ]
    .new_steps
  )

  assert transport_step in (
    seventh_round
  )


def test_phase53_probe_output_contains_transport_and_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 53 capability demonstration"
    in output
  )

  assert (
    "π_4^3 = Z/2{η₃}"
    in output
  )

  assert (
    "E^(n-3): "
    "π_4^3 ≅ π_(n+1)^n"
    in output
  )

  assert (
    "π_(n+1)^n "
    "= Z/2{E^(n-3)η₃}"
    in output
  )

  assert (
    "source group result is derived = True"
    in output
  )

  assert (
    "Toda45 isomorphism is derived = True"
    in output
  )

  assert (
    "transport result is derived = True"
    in output
  )

  assert (
    "transport premise count = 2"
    in output
  )

  assert (
    "transport premises are derived = True"
    in output
  )

  assert (
    "given premise count = 14"
    in output
  )

  assert (
    "derived step count = 11"
    in output
  )

  assert (
    "derived round count = 7"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )

  assert (
    "E^(n-3)eta_3 = eta_n"
    in output
  )



