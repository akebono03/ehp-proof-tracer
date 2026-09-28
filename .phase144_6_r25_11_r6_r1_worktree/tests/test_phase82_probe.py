from probes.probe_phase82_capabilities import (
  build_phase82_representative_result,
  main,
)


def test_phase82_probe_detects_one_missing_premise():
  result = build_phase82_representative_result()

  assert (
    result[
      "availability"
    ].missing_indices
    == (
      1,
    )
  )


def test_phase82_probe_finds_unique_producer():
  result = build_phase82_representative_result()

  assert len(
    result[
      "producer_rules"
    ]
  ) == 1


def test_phase82_probe_derives_new_intermediate():
  result = build_phase82_representative_result()

  assert not result[
    "intermediate_initially_present"
  ]

  assert result[
    "intermediate_is_inference"
  ]

  assert result[
    "producer_rule_reused"
  ]


def test_phase82_probe_derives_final_goal():
  result = build_phase82_representative_result()

  assert not result[
    "goal_initially_present"
  ]

  assert result[
    "final_is_inference"
  ]

  assert result[
    "final_rule_reused"
  ]

  assert result[
    "final_uses_new_intermediate"
  ]


def test_phase82_probe_preserves_non_circularity():
  result = build_phase82_representative_result()

  assert result[
    "goal_absent_from_ancestors"
  ]

  assert result[
    "graph_acyclic"
  ]


def test_phase82_probe_does_not_mutate_repository():
  result = build_phase82_representative_result()

  assert not result[
    "repository_mutated"
  ]


def test_phase82_probe_prints_completion_flow(
  capsys,
):
  main()

  output = capsys.readouterr().out

  assert (
    "Phase 82: one-level goal-directed proof search"
    in output
  )
  assert (
    "missing premise count = 1"
    in output
  )
  assert (
    "unique producer selected = True"
    in output
  )
  assert (
    "intermediate derived = True"
    in output
  )
  assert (
    "final goal derived = True"
    in output
  )
  assert (
    "recursive producer search = not implemented"
    in output
  )
