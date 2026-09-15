from proof import ProofRule
from probes.probe_phase81_capabilities import (
  build_phase81_representative_result,
  main,
)


def test_phase81_probe_builds_actual_derived_goal():
  result = (
    build_phase81_representative_result()
  )

  assert (
    result[
      "goal_step"
    ].conclusion
    == result[
      "goal"
    ]
  )

  assert (
    result[
      "goal_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase81_probe_uses_automatically_selected_actual_rule():
  result = (
    build_phase81_representative_result()
  )

  assert (
    result[
      "selected_rule"
    ]
    is result[
      "data"
    ][
      "final_rule"
    ]
  )


def test_phase81_probe_excludes_unsafe_and_unrelated_rules():
  result = (
    build_phase81_representative_result()
  )

  data = result[
    "data"
  ]

  assert (
    data[
      "unsafe_rule"
    ]
    not in result[
      "compatible_rules"
    ]
  )

  assert (
    data[
      "unrelated_rule"
    ]
    not in result[
      "compatible_rules"
    ]
  )


def test_phase81_probe_wrong_candidates_do_not_match():
  result = (
    build_phase81_representative_result()
  )

  assert (
    result[
      "wrong_rule_match_count"
    ]
    == 0
  )


def test_phase81_probe_has_one_accepted_goal_proof():
  result = (
    build_phase81_representative_result()
  )

  assert (
    result[
      "accepted_goal_count"
    ]
    == 1
  )


def test_phase81_probe_goal_is_not_seeded():
  result = (
    build_phase81_representative_result()
  )

  assert (
    result[
      "initial_goal_present"
    ]
    is False
  )


def test_phase81_probe_preserves_exact_repository_premises():
  result = (
    build_phase81_representative_result()
  )

  phase80 = result[
    "phase80"
  ]

  assert (
    result[
      "goal_step"
    ].premises
    == (
      phase80[
        "bracket_sum_step"
      ],
      phase80[
        "composition_step"
      ],
    )
  )


def test_phase81_probe_output(capsys):
  main()

  output = capsys.readouterr().out

  assert (
    "Phase 81: automatic rule selection"
    in output
  )

  assert (
    "Toda Lemma 5.16 final consequence"
    in output
  )

  assert (
    "unsafe candidate excluded = True"
    in output
  )

  assert (
    "wrong-guard candidate rejected = True"
    in output
  )

  assert (
    "selected existing Phase 77 rule = True"
    in output
  )

  assert (
    "accepted goal proofs = 1"
    in output
  )

  assert (
    "multi-step unknown-premise search = not implemented"
    in output
  )
