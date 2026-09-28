from audit_phase144_6_r5_25 import (
  FRONTIER_REQUIRED_KEYS,
  SuppressionCause,
  build_frontier_candidate_signatures,
  build_multi_suppression_traces,
)


def test_phase144_6_r5_25_traces_both_visible_hopf_facts():
  traces = build_multi_suppression_traces()

  assert tuple(trace.key for trace in traces) == (
    "hopf_nu_prime",
    "hopf_nu_eta6",
  )


def test_phase144_6_r5_25_classifies_multi_argument_suppression():
  traces = build_multi_suppression_traces()

  assert all(isinstance(trace.cause, SuppressionCause) for trace in traces)


def test_phase144_6_r5_25_records_shared_block_suppression_when_present():
  traces = build_multi_suppression_traces()

  assert all(trace.first_render_argument_index is not None for trace in traces)


def test_phase144_6_r5_25_inventories_hidden_supporting_provider_candidates():
  candidates = build_frontier_candidate_signatures()

  assert candidates
  assert all(candidate.is_supporting_provider for candidate in candidates)


def test_phase144_6_r5_25_finds_required_pi6_frontier_facts_in_candidate_inventory():
  candidates = build_frontier_candidate_signatures()
  found = {
    candidate.required_pi6_key
    for candidate in candidates
    if candidate.required_pi6_key is not None
  }

  assert found == set(FRONTIER_REQUIRED_KEYS) - {"pi7_5_group"}


def test_phase144_6_r5_25_keeps_pi7_5_as_non_direct_provider_case():
  candidates = build_frontier_candidate_signatures()

  assert not any(
    candidate.required_pi6_key == "pi7_5_group"
    for candidate in candidates
  )
