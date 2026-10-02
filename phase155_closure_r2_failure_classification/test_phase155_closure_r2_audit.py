from __future__ import annotations

import phase155_closure_r2_audit as audit


def _failed(nodeid: str) -> str:
  return (
    "FAILED "
    + nodeid
    + "\n"
  )


def test_extracts_and_classifies_reviewed_phase_families():
  text = "".join(
    (
      _failed(
        "tests/test_phase132_x.py::test_a"
      ),
      _failed(
        "tests/test_phase144_x.py::test_b"
      ),
      _failed(
        "tests/test_phase153_x.py::test_c"
      ),
      _failed(
        "tests/test_phase97_x.py::test_d"
      ),
    )
  )

  records = audit._extract_failures(
    text
  )

  assert tuple(
    record.category
    for record in records
  ) == (
    "SAFE_STALE",
    "HISTORICAL_HEAVY",
    "CONTRACT_SENSITIVE",
    "CONTRACT_SENSITIVE",
  )


def test_unknown_is_not_silently_treated_as_stale():
  records = audit._extract_failures(
    _failed(
      "tests/test_unreviewed.py::test_x"
    )
  )

  assert len(
    records
  ) == 1
  assert (
    records[
      0
    ].category
    == "UNKNOWN"
  )


def test_phase150_is_safe_stale_lane():
  record = audit._classify(
    "tests/test_phase150_x.py::test_x"
  )

  assert (
    record.category
    == "SAFE_STALE"
  )


def test_phase95_to_98_are_contract_sensitive():
  for phase in (
    95,
    96,
    97,
    98,
  ):
    record = audit._classify(
      (
        "tests/test_phase"
        + str(
          phase
        )
        + "_x.py::test_x"
      )
    )

    assert (
      record.category
      == "CONTRACT_SENSITIVE"
    )


def test_slow_rows_are_sorted_descending():
  text = (
    "5.00s call     tests/test_phase132_x.py::test_a\n"
    "508.30s call     tests/test_phase97_x.py::test_b\n"
    "27.64s setup    tests/test_phase144_x.py::test_c\n"
  )

  rows = audit._extract_slow_rows(
    text
  )

  assert tuple(
    row[
      "seconds"
    ]
    for row in rows
  ) == (
    508.30,
    27.64,
    5.00,
  )
