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
      "tests/test_phase153_r3_10_public_reference_connection_repair.py::"
      "test_phase153_r3_10_all_group_reference_population_invariants"
    ),
    (
      "tests/test_phase97_actual_representative_targets_top_level_api.py::"
      "test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api"
    ),
  }
  assert len(
    nodeids
  ) == 2


def test_phase155_audit_boundary_contains_only_reviewed_phase153_or_phase97_tests():
  nodeids = _phase155_audit_nodeids()

  assert all(
    (
      nodeid.startswith(
        "tests/test_phase153_"
      )
      or nodeid.startswith(
        "tests/test_phase97_"
      )
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
