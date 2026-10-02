from phase155_closure_r2c_r4_audit import (
  CLASSIFICATION,
  EXPECTED_KEEP_ROUTINE,
)


def test_r2c_r4_covers_exactly_fourteen_candidates():
  assert len(
    EXPECTED_KEEP_ROUTINE
  ) == 14
  assert set(
    CLASSIFICATION
  ) == EXPECTED_KEEP_ROUTINE


def test_r2c_r4_expected_classification_counts():
  counts = {
    "KEEP": 0,
    "MERGE_CANDIDATE": 0,
    "DELETE_CANDIDATE": 0,
  }

  for (
    classification,
    rationale,
    overlap_group,
  ) in CLASSIFICATION.values():
    counts[
      classification
    ] += 1
    assert rationale
    assert overlap_group

  assert counts == {
    "KEEP": 3,
    "MERGE_CANDIDATE": 5,
    "DELETE_CANDIDATE": 6,
  }


def test_pi10_6_baseline_keeps_only_current_r3_4_contract():
  baseline_rows = {
    nodeid: values[
      0
    ]
    for nodeid, values in CLASSIFICATION.items()
    if values[
      2
    ] == "phase153_pi10_6_reference_baseline"
  }

  assert list(
    baseline_rows.values()
  ).count(
    "KEEP"
  ) == 1


def test_population_scans_are_merge_candidates():
  rows = [
    values[
      0
    ]
    for values in CLASSIFICATION.values()
    if values[
      2
    ] == "phase153_all_group_reference_population"
  ]

  assert rows
  assert set(
    rows
  ) == {
    "MERGE_CANDIDATE",
  }


def test_final_render_surfaces_are_kept():
  kept = {
    nodeid
    for nodeid, values in CLASSIFICATION.items()
    if values[
      0
    ] == "KEEP"
  }

  assert any(
    "full_proof_report_renderer"
    in nodeid
    for nodeid in kept
  )
  assert any(
    "human_readable_renderer"
    in nodeid
    for nodeid in kept
  )
