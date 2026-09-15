from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase80_capabilities import (
  build_phase80_representative_result,
)


def test_phase80_7_probe_goal_is_not_initial():
  result = (
    build_phase80_representative_result()
  )

  assert not result[
    "initial_goal_present"
  ]


def test_phase80_7_probe_derives_goal():
  result = (
    build_phase80_representative_result()
  )

  assert result[
    "goal_step"
  ] is not None


def test_phase80_7_probe_creates_new_inference_step():
  result = (
    build_phase80_representative_result()
  )

  assert result[
    "goal_is_new_step"
  ]
  assert result[
    "goal_step"
  ].rule == ProofRule.INFERENCE


def test_phase80_7_probe_reuses_exact_repository_premises():
  result = (
    build_phase80_representative_result()
  )

  assert result[
    "exact_repository_premises"
  ]


def test_phase80_7_probe_reuses_existing_phase77_rule():
  result = (
    build_phase80_representative_result()
  )

  assert (
    result[
      "goal_step"
    ].inference_rule
    is result[
      "data"
    ][
      "final_rule"
    ]
  )


def test_phase80_7_probe_reaches_fixed_point():
  result = (
    build_phase80_representative_result()
  )

  assert (
    result[
      "result"
    ].inference_result
    .termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase80_7_probe_goal_absent_from_ancestors():
  result = (
    build_phase80_representative_result()
  )

  assert result[
    "goal_absent_from_ancestors"
  ]


def test_phase80_7_probe_graph_is_acyclic():
  result = (
    build_phase80_representative_result()
  )

  assert result[
    "graph_acyclic"
  ]
