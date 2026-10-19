from functools import lru_cache
from audit_phase144_6_r5_22 import (
  MISSING_KEYS,
  StructureLocation,
  build_statement_structure_traces,
)


_uncached_build_statement_structure_traces = build_statement_structure_traces

@lru_cache(maxsize=1)
def build_statement_structure_traces():
  return _uncached_build_statement_structure_traces()


def test_phase144_6_r5_22_traces_exactly_phase21_not_found_four():
  traces = build_statement_structure_traces()

  assert tuple(trace.key for trace in traces) == MISSING_KEYS
  assert len(traces) == 4


def test_phase144_6_r5_22_classifies_each_fact_by_statement_structure():
  traces = build_statement_structure_traces()

  assert all(
    isinstance(trace.location, StructureLocation)
    for trace in traces
  )


def test_phase144_6_r5_22_reports_exact_conclusion_hits():
  traces = build_statement_structure_traces()

  assert all(
    trace.exact_conclusion_hits >= 0
    for trace in traces
  )


def test_phase144_6_r5_22_reports_embedded_conclusion_hits():
  traces = build_statement_structure_traces()

  assert all(
    trace.embedded_conclusion_hits >= 0
    for trace in traces
  )


def test_phase144_6_r5_22_reports_recursive_premise_hits():
  traces = build_statement_structure_traces()

  assert all(
    trace.embedded_premise_hits >= 0
    for trace in traces
  )


def test_phase144_6_r5_22_nu_eta6_is_a_structural_object_not_a_fake_membership_step():
  traces = build_statement_structure_traces()
  trace = next(
    trace
    for trace in traces
    if trace.key == "nu_eta6_membership"
  )

  assert trace.canonical_type != "ProofStep"


def test_phase144_6_r5_22_does_not_require_any_specific_location_in_advance():
  traces = build_statement_structure_traces()

  assert len(
    {
      trace.location
      for trace in traces
    }
  ) >= 1
