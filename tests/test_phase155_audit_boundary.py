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


def test_phase155_audit_boundary_has_23_unique_nodeids():
  nodeids = _phase155_audit_nodeids()

  assert len(
    nodeids
  ) == 23
  assert len(
    set(
      nodeids
    )
  ) == 23


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
