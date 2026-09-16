from repository_inference import (
  BoundedProducerSearchStatus,
)
from probes.probe_phase86_capabilities import (
  build_phase86_representative_result,
  main,
)


def test_phase86_probe_reports_successful_default_and_explicit_search():
  result = (
    build_phase86_representative_result()
  )

  assert result[
    "default_status"
  ] is BoundedProducerSearchStatus.SUCCESS

  assert result[
    "explicit_status"
  ] is BoundedProducerSearchStatus.SUCCESS


def test_phase86_probe_reports_explicit_depth_two():
  result = (
    build_phase86_representative_result()
  )

  assert result[
    "default_max_depth"
  ] == 2

  assert result[
    "explicit_max_depth"
  ] == 2


def test_phase86_probe_preserves_selected_path():
  result = (
    build_phase86_representative_result()
  )

  assert result[
    "same_final_rule"
  ]

  assert result[
    "same_producer_path"
  ]

  assert result[
    "same_depths"
  ]

  assert result[
    "same_dependencies"
  ]

  assert result[
    "default_producer_node_count"
  ] == 2

  assert result[
    "explicit_producer_node_count"
  ] == 2


def test_phase86_probe_preserves_shared_dependency():
  result = (
    build_phase86_representative_result()
  )

  assert result[
    "default_shared_depths"
  ] == (
    1,
    2,
  )

  assert result[
    "explicit_shared_depths"
  ] == (
    1,
    2,
  )

  assert result[
    "default_shared_dependency"
  ]

  assert result[
    "explicit_shared_dependency"
  ]


def test_phase86_probe_preserves_goal_provenance():
  result = (
    build_phase86_representative_result()
  )

  assert result[
    "default_goal_derived"
  ]

  assert result[
    "explicit_goal_derived"
  ]

  assert result[
    "same_goal_conclusion"
  ]

  assert result[
    "same_goal_rule"
  ]

  assert result[
    "same_goal_premise_conclusions"
  ]

  assert result[
    "same_goal_premise_rules"
  ]


def test_phase86_probe_preserves_depth_limit_diagnostic():
  result = (
    build_phase86_representative_result()
  )

  assert result[
    "diagnostic_status"
  ] is BoundedProducerSearchStatus.DEPTH_LIMIT

  assert result[
    "diagnostic_current_depth"
  ] == 2

  assert result[
    "diagnostic_required_next_depth"
  ] == 3


def test_phase86_probe_preserves_repository_non_mutation():
  result = (
    build_phase86_representative_result()
  )

  assert not result[
    "repository_mutated"
  ]


def test_phase86_probe_preserves_phase_boundary():
  result = (
    build_phase86_representative_result()
  )

  assert result[
    "max_depth_one_rejected"
  ]

  assert result[
    "max_depth_three_accepted"
  ]

  assert result[
    "max_depth_four_rejected"
  ]


def test_phase86_probe_prints_completion_flow(
  capsys,
):
  main()

  output = capsys.readouterr().out

  assert (
    "Phase 86-2: explicit max_depth "
    "parameterization compatibility"
    in output
  )

  assert (
    "Toda Lemma 5.16 final "
    "bracket-sum consequence"
    in output
  )

  assert (
    "default max depth = 2"
    in output
  )

  assert (
    "explicit max depth = 2"
    in output
  )

  assert (
    "same producer path = True"
    in output
  )

  assert (
    "same dependencies = True"
    in output
  )

  assert (
    "default shared depths = (1, 2)"
    in output
  )

  assert (
    "explicit shared depths = (1, 2)"
    in output
  )

  assert (
    "same goal inference rule = True"
    in output
  )

  assert (
    "status = depth_limit"
    in output
  )

  assert (
    "current depth = 2"
    in output
  )

  assert (
    "required next depth = 3"
    in output
  )

  assert (
    "repository mutated = False"
    in output
  )

  assert (
    "max_depth=1 rejected = True"
    in output
  )

  assert (
    "max_depth=3 accepted = True"
    in output
  )

  assert (
    "max_depth=4 rejected = True"
    in output
  )

  assert (
    "explicit max_depth=2 = enabled"
    in output
  )

  assert (
    "max_depth=3 = enabled"
    in output
  )

  assert (
    "max_depth > 3 = not implemented"
    in output
  )


