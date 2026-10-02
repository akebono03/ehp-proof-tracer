from __future__ import annotations

from phase155_closure_r2b_r2_audit import (
  RULE_BY_FUNCTION,
)


def test_duplicate_and_order_contract_is_not_marked_deletable():
  rule = RULE_BY_FUNCTION[
    "test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations"
  ]

  assert (
    rule[
      0
    ]
    == "UNIQUE_CURRENT_INVARIANT"
  )
  assert (
    rule[
      3
    ]
    == "KEEP_OR_LIGHTWEIGHT_REPLACE"
  )


def test_conclusion_placement_contract_is_not_marked_deletable():
  rule = RULE_BY_FUNCTION[
    "test_phase144_6_r5_43_11_all_rendered_contributions_precede_owning_argument_conclusion"
  ]

  assert (
    rule[
      0
    ]
    == "UNIQUE_CURRENT_INVARIANT"
  )


def test_final_transport_connector_supersedes_old_count_contract():
  rule = RULE_BY_FUNCTION[
    "test_phase144_6_r5_43_11_all_sixteen_transport_chains_are_connected"
  ]

  assert (
    rule[
      0
    ]
    == "FULLY_COVERED"
  )
  assert any(
    "43_11d"
    in coverage
    for coverage in rule[
      1
    ]
  )


def test_old_13_177_split_is_historical_not_current_contract():
  rule = RULE_BY_FUNCTION[
    "test_phase144_6_r5_43_11a_reproduces_13_insertable_and_177_non_insertable"
  ]

  assert (
    rule[
      0
    ]
    == "OBSOLETE_HISTORICAL"
  )


def test_audit_meta_tests_are_delete_candidates():
  for function_name in (
    "test_phase144_6_r5_43_6_is_audit_only",
    "test_phase144_6_r5_43_8_is_audit_only",
    "test_phase144_6_r5_43_9_is_audit_only",
  ):
    rule = RULE_BY_FUNCTION[
      function_name
    ]

    assert (
      rule[
        3
      ]
      == "DELETE_CANDIDATE"
    )
