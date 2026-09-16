from repository_inference import (
  BoundedProducerSearchStatus,
)
from probes.probe_phase86_capabilities import (
  build_phase86_depth_three_representative_result,
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
    "Phase 86-3: bounded depth=3 completion"
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
    "max_depth=2 status = depth_limit"
    in output
  )
  assert (
    "required next depth = 3"
    in output
  )
  assert (
    "max_depth=3 status = success"
    in output
  )
  assert (
    "selected max depth = 3"
    in output
  )
  assert (
    "producer depths = ((3,), (2,), (1,))"
    in output
  )
  assert (
    "dependency-first order = True"
    in output
  )
  assert (
    "goal derived = True"
    in output
  )
  assert (
    "B uses C ProofStep = True"
    in output
  )
  assert (
    "A uses B ProofStep = True"
    in output
  )
  assert (
    "final uses A ProofStep = True"
    in output
  )
  assert (
    "repository mutated = False"
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
    "selection / diagnostics / report / execution "
    "support max_depth=2,3"
    in output
  )


def test_phase86_3_6_probe_reports_depth_three_boundary_pair():
  result = (
    build_phase86_depth_three_representative_result()
  )

  assert result[
    "depth_two_status"
  ] is BoundedProducerSearchStatus.DEPTH_LIMIT
  assert result[
    "depth_two_current_depth"
  ] == 2
  assert result[
    "depth_two_required_next_depth"
  ] == 3
  assert result[
    "depth_three_status"
  ] is BoundedProducerSearchStatus.SUCCESS
  assert result[
    "depth_three_max_depth"
  ] == 3
  assert result[
    "producer_depths"
  ] == (
    (3,),
    (2,),
    (1,),
  )


def test_phase86_3_6_probe_reports_depth_three_execution_provenance():
  result = (
    build_phase86_depth_three_representative_result()
  )

  assert result[
    "dependency_first_order"
  ]
  assert result[
    "goal_derived"
  ]
  assert result[
    "c_rule_reused"
  ]
  assert result[
    "b_uses_c_step"
  ]
  assert result[
    "a_uses_b_step"
  ]
  assert result[
    "final_uses_a_step"
  ]
  assert not result[
    "repository_mutated"
  ]
