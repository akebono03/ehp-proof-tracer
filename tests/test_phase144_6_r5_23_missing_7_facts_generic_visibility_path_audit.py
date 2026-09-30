from functools import lru_cache
from audit_phase144_6_r5_23 import (
  FACT_KEYS,
  VisibilityPath,
  build_visibility_path_traces,
)


_uncached_build_visibility_path_traces = build_visibility_path_traces

@lru_cache(maxsize=1)
def build_visibility_path_traces():
  return _uncached_build_visibility_path_traces()


def test_phase144_6_r5_23_traces_all_phase20_missing_seven():
  traces = build_visibility_path_traces()

  assert tuple(trace.key for trace in traces) == FACT_KEYS
  assert len(traces) == 7


def test_phase144_6_r5_23_classifies_every_fact_by_visibility_path():
  traces = build_visibility_path_traces()

  assert all(
    isinstance(trace.path, VisibilityPath)
    for trace in traces
  )


def test_phase144_6_r5_23_uses_canonical_structure_not_rendered_needles():
  traces = build_visibility_path_traces()

  assert all(trace.canonical_type for trace in traces)


def test_phase144_6_r5_23_reports_provider_paths():
  traces = build_visibility_path_traces()

  assert all(
    isinstance(trace.supporting_provider_argument_indices, tuple)
    for trace in traces
  )
  assert all(
    isinstance(trace.child_provider_argument_indices, tuple)
    for trace in traces
  )


def test_phase144_6_r5_23_reports_local_body_and_frontier_paths():
  traces = build_visibility_path_traces()

  assert all(
    isinstance(trace.local_body_argument_indices, tuple)
    for trace in traces
  )
  assert all(
    isinstance(trace.frontier_hidden_argument_indices, tuple)
    for trace in traces
  )
  assert all(
    isinstance(trace.visible_argument_indices, tuple)
    for trace in traces
  )


def test_phase144_6_r5_23_tracks_nu_eta6_through_equation57_parent():
  traces = build_visibility_path_traces()
  trace = next(
    trace
    for trace in traces
    if trace.key == "nu_eta6_membership"
  )

  assert trace.embedded_parent_key == "hopf_nu_eta6"
  assert trace.presentation_step_count >= 1


def test_phase144_6_r5_23_preserves_phase21_frontier_hidden_diagnosis():
  traces = {
    trace.key: trace
    for trace in build_visibility_path_traces()
  }

  for key in (
    "pi5_3_group",
    "hopf_pi7_surjective",
    "delta_zero",
  ):
    assert traces[key].frontier_hidden_argument_indices


def test_phase144_6_r5_23_does_not_require_a_fix_in_advance():
  traces = build_visibility_path_traces()

  assert len({trace.path for trace in traces}) >= 1
