from audit_phase144_6_r5_26 import (
  FRONTIER_KEYS,
  build_derivation_path_traces,
  build_step_dedup_impacts,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_26_measures_all_six_groups_for_step_dedup():
  impacts = build_step_dedup_impacts()

  assert tuple((impact.n, impact.k) for impact in impacts) == TARGETS


def test_phase144_6_r5_26_step_dedup_counts_are_consistent():
  impacts = build_step_dedup_impacts()

  for impact in impacts:
    assert (
      impact.step_policy_still_suppressed_steps
      + impact.step_policy_released_steps
      == impact.block_policy_suppressed_steps
    )


def test_phase144_6_r5_26_pi6_has_shared_non_exact_blocks():
  impact = build_step_dedup_impacts()[0]

  assert impact.shared_non_exact_block_occurrences > 0


def test_phase144_6_r5_26_traces_all_four_frontier_facts():
  traces = build_derivation_path_traces()
  found = {trace.key for trace in traces}

  assert found == set(FRONTIER_KEYS)


def test_phase144_6_r5_26_records_raw_and_augmented_path_status():
  traces = build_derivation_path_traces()

  assert all(
    isinstance(trace.on_raw_premise_path_to_conclusion, bool)
    for trace in traces
  )
  assert all(
    isinstance(trace.on_semantic_augmented_path_to_conclusion, bool)
    for trace in traces
  )


def test_phase144_6_r5_26_preserves_frontier_hidden_observation():
  traces = build_derivation_path_traces()

  for key in FRONTIER_KEYS:
    assert any(
      trace.key == key and trace.hidden_by_frontier
      for trace in traces
    )
