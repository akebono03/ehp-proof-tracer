from pathlib import Path


TESTS_DIR = Path(
  __file__
).resolve().parent


def _phase155_audit_nodeids():
  path = (
    TESTS_DIR
    / "phase155_audit_only_nodeids.txt"
  )

  return tuple(
    line.strip()
    for line in path.read_text(
      encoding="utf-8",
    ).splitlines()
    if line.strip()
  )


def test_phase155_audit_boundary_has_2_exact_nodeids():
  nodeids = _phase155_audit_nodeids()

  assert set(
    nodeids
  ) == {
    (
      "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
      "test_phase144_6_r5_43_11d_final_completion_invariants_pass"
    ),
    (
      "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::"
      "test_phase144_6_r5_43_11d_renderer_remains_generic"
    ),
  }
  assert len(
    nodeids
  ) == 2


def test_phase155_audit_boundary_contains_only_phase144_tests():
  nodeids = _phase155_audit_nodeids()

  assert all(
    nodeid.startswith(
      "tests/test_phase144_"
    )
    for nodeid in nodeids
  )


def test_phase155_audit_boundary_keeps_function_level_nodeids():
  nodeids = _phase155_audit_nodeids()

  assert all(
    "::test_"
    in nodeid
    for nodeid in nodeids
  )
