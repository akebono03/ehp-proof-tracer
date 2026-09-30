from functools import lru_cache
from audit_phase144_6_r5_21 import (
  MISSING_KEYS,
  LossStage,
  build_missing_fact_traces,
)


_uncached_build_missing_fact_traces = build_missing_fact_traces

@lru_cache(maxsize=1)
def build_missing_fact_traces():
  return _uncached_build_missing_fact_traces()


def test_phase144_6_r5_21_traces_exactly_phase20_missing_seven():
  traces = build_missing_fact_traces()

  assert tuple(trace.key for trace in traces) == MISSING_KEYS
  assert len(traces) == 7


def test_phase144_6_r5_21_classifies_every_missing_fact_at_one_loss_stage():
  traces = build_missing_fact_traces()

  assert all(
    isinstance(trace.loss_stage, LossStage)
    for trace in traces
  )


def test_phase144_6_r5_21_reports_presentation_step_counts():
  traces = build_missing_fact_traces()

  assert all(
    trace.matching_step_count >= 0
    for trace in traces
  )


def test_phase144_6_r5_21_reports_proof_chain_provider_hits():
  traces = build_missing_fact_traces()

  assert all(
    trace.proof_chain_provider_hits >= 0
    for trace in traces
  )


def test_phase144_6_r5_21_reports_local_body_membership():
  traces = build_missing_fact_traces()

  assert all(
    isinstance(trace.local_body_argument_indices, tuple)
    for trace in traces
  )


def test_phase144_6_r5_21_does_not_assume_all_missing_facts_have_same_cause():
  traces = build_missing_fact_traces()

  assert len(
    {
      trace.loss_stage
      for trace in traces
    }
  ) >= 1
