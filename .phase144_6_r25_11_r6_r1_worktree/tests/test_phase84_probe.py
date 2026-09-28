from probes.probe_phase84_capabilities import (
  build_phase84_representative_result,
  main,
)


def test_phase84_probe_selects_two_producer_nodes():
  result = build_phase84_representative_result()

  assert len(
    result[
      "search_result"
    ].producer_nodes
  ) == 2


def test_phase84_probe_records_shared_depths():
  result = build_phase84_representative_result()

  assert (
    result[
      "bracket_sum_node"
    ].depths
    == (
      1,
      2,
    )
  )

  assert result[
    "bracket_sum_node"
  ].is_shared

  assert (
    result[
      "composition_node"
    ].dependencies
    == (
      result[
        "bracket_sum_node"
      ],
    )
  )


def test_phase84_probe_derives_all_actual_steps():
  result = build_phase84_representative_result()

  assert not result[
    "bracket_sum_initially_present"
  ]
  assert not result[
    "composition_initially_present"
  ]
  assert not result[
    "goal_initially_present"
  ]

  assert result[
    "bracket_sum_derived"
  ]
  assert result[
    "composition_derived"
  ]
  assert result[
    "final_derived"
  ]


def test_phase84_probe_reuses_shared_proof_step():
  result = build_phase84_representative_result()

  assert result[
    "shared_bracket_sum_step"
  ]


def test_phase84_probe_reuses_actual_rules():
  result = build_phase84_representative_result()

  assert result[
    "bracket_sum_rule_reused"
  ]
  assert result[
    "composition_rule_reused"
  ]
  assert result[
    "final_rule_reused"
  ]


def test_phase84_probe_preserves_safety():
  result = build_phase84_representative_result()

  assert (
    result[
      "search_result"
    ].is_within_depth_limit
  )
  assert result[
    "graph_acyclic"
  ]
  assert not result[
    "repository_mutated"
  ]


def test_phase84_probe_prints_completion_flow(
  capsys,
):
  main()

  output = capsys.readouterr().out

  assert (
    "Phase 84: bounded depth=2 producer search"
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
    "bracket-sum shared = True"
    in output
  )
  assert (
    "composition depends on bracket-sum = True"
    in output
  )
  assert (
    "final goal derived = True"
    in output
  )
  assert (
    "producer execution depth = 2"
    in output
  )
  assert (
    "depth > 2 = not implemented"
    in output
  )
