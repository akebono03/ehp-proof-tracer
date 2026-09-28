from probes.probe_phase83_capabilities import (
  build_phase83_representative_result,
  main,
)


def test_phase83_probe_detects_two_missing_premises():
  result = build_phase83_representative_result()

  assert (
    result[
      "availability"
    ].missing_indices
    == (
      0,
      1,
    )
  )


def test_phase83_probe_finds_one_producer_per_missing_premise():
  result = build_phase83_representative_result()

  assert tuple(
    len(
      lookup.producer_rules
    )
    for lookup in result[
      "lookups"
    ]
  ) == (
    1,
    1,
  )

  assert result[
    "all_unique"
  ]


def test_phase83_probe_derives_both_intermediates():
  result = build_phase83_representative_result()

  assert not result[
    "first_initially_present"
  ]
  assert not result[
    "second_initially_present"
  ]
  assert result[
    "first_is_inference"
  ]
  assert result[
    "second_is_inference"
  ]


def test_phase83_probe_derives_final_goal():
  result = build_phase83_representative_result()

  assert not result[
    "goal_initially_present"
  ]
  assert result[
    "final_is_inference"
  ]
  assert result[
    "final_uses_both_intermediates"
  ]


def test_phase83_probe_reuses_all_actual_rules():
  result = build_phase83_representative_result()

  assert result[
    "first_rule_reused"
  ]
  assert result[
    "second_rule_reused"
  ]
  assert result[
    "final_rule_reused"
  ]


def test_phase83_probe_preserves_safety():
  result = build_phase83_representative_result()

  assert result[
    "graph_acyclic"
  ]
  assert not result[
    "repository_mutated"
  ]


def test_phase83_probe_prints_completion_flow(
  capsys,
):
  main()

  output = capsys.readouterr().out

  assert (
    "Phase 83: multiple one-level producers"
    in output
  )
  assert (
    "missing premise count = 2"
    in output
  )
  assert (
    "all missing premises uniquely producible = True"
    in output
  )
  assert (
    "first intermediate derived = True"
    in output
  )
  assert (
    "second intermediate derived = True"
    in output
  )
  assert (
    "final goal derived = True"
    in output
  )
  assert (
    "producer execution depth = 1"
    in output
  )
  assert (
    "depth > 1 = not implemented"
    in output
  )
