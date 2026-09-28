from audit_phase144_6_r5_43_5 import (
  build_chain_audit,
)


def test_phase144_6_r5_43_5_audits_three_transitive_segments():
  (
    presentation,
    connected,
    contributions,
    segments,
  ) = build_chain_audit()

  assert len(
    contributions
  ) == 5
  assert len(
    segments
  ) == 3


def test_phase144_6_r5_43_5_each_segment_has_a_reachable_target():
  (
    presentation,
    connected,
    contributions,
    segments,
  ) = build_chain_audit()

  assert all(
    segment[
      "target"
    ] is not None
    for segment in segments
  )
  assert all(
    segment[
      "paths"
    ]
    for segment in segments
  )


def test_phase144_6_r5_43_5_records_all_shortest_path_steps():
  (
    presentation,
    connected,
    contributions,
    segments,
  ) = build_chain_audit()

  for segment in segments:
    source = segment[
      "source"
    ]
    target = segment[
      "target"
    ]

    for path in segment[
      "paths"
    ]:
      assert path[
        0
      ] is source
      assert path[
        -1
      ] is target
      assert len(
        path
      ) >= 2


def test_phase144_6_r5_43_5_is_audit_only():
  import inspect
  import audit_phase144_6_r5_43_5 as module

  source = inspect.getsource(
    module
  )

  assert "write_text(" not in source
  assert "open(" not in source
