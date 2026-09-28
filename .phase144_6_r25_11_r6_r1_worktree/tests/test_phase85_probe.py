from repository_inference import (
  BoundedProducerSearchStatus,
)
from probes.probe_phase85_capabilities import (
  build_phase85_representative_result,
  main,
)


def test_phase85_probe_reports_integrated_success():
  result = (
    build_phase85_representative_result()
  )

  assert result[
    "status"
  ] is BoundedProducerSearchStatus.SUCCESS

  assert result[
    "diagnostic"
  ] is None

  assert result[
    "search_result"
  ] is not None


def test_phase85_probe_preserves_depth_two_search_path():
  result = (
    build_phase85_representative_result()
  )

  assert result[
    "producer_node_count"
  ] == 2

  assert result[
    "bracket_sum_depths"
  ] == (
    1,
    2,
  )

  assert result[
    "bracket_sum_shared"
  ]

  assert result[
    "composition_depends_on_bracket_sum"
  ]

  assert result[
    "within_depth_limit"
  ]


def test_phase85_probe_derives_actual_goal():
  result = (
    build_phase85_representative_result()
  )

  assert not result[
    "goal_initially_present"
  ]

  assert result[
    "goal_derived"
  ]


def test_phase85_probe_reuses_shared_actual_proof_step():
  result = (
    build_phase85_representative_result()
  )

  assert result[
    "shared_bracket_sum_step"
  ]


def test_phase85_probe_preserves_actual_rule_identity():
  result = (
    build_phase85_representative_result()
  )

  assert result[
    "bracket_sum_rule_reused"
  ]

  assert result[
    "composition_rule_reused"
  ]

  assert result[
    "final_rule_reused"
  ]


def test_phase85_probe_preserves_safety():
  result = (
    build_phase85_representative_result()
  )

  assert result[
    "graph_acyclic"
  ]

  assert not result[
    "repository_mutated"
  ]


def test_phase85_probe_prints_completion_flow(
  capsys,
):
  main()

  output = capsys.readouterr().out

  assert (
    "Phase 85: bounded-search diagnostics "
    "and integrated execution"
    in output
  )

  assert (
    "Toda Lemma 5.16 final bracket-sum consequence"
    in output
  )

  assert (
    "status = success"
    in output
  )

  assert (
    "diagnostic present = False"
    in output
  )

  assert (
    "search result present = True"
    in output
  )

  assert (
    "producer node count = 2"
    in output
  )

  assert (
    "bracket-sum depths = (1, 2)"
    in output
  )

  assert (
    "final goal derived = True"
    in output
  )

  assert (
    "integrated bounded-search execution = enabled"
    in output
  )

  assert (
    "actual Toda Lemma 5.16 integration = verified"
    in output
  )

  assert (
    "retry / backtracking = not implemented"
    in output
  )

  assert (
    "depth > 2 = not implemented"
    in output
  )


