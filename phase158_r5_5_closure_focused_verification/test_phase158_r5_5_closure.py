from __future__ import annotations

from audit_phase158_r5_5_closure import (
  _canonical_visible_text,
  _connector_findings,
)


def test_phase158_r5_5_closure_canonical_visible_text():
  assert (
    _canonical_visible_text(
      r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    )
    ==
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
  )


def test_phase158_r5_5_closure_connector_accepts_tagged_target():
  findings, count, tagged, untagged = (
    _connector_findings(
      (
        r"A=B\tag{1}",
        "(1) より,",
        r"A=C\tag{2}",
      )
    )
  )

  assert findings == ()
  assert count == 1
  assert tagged == 1
  assert untagged == 0


def test_phase158_r5_5_closure_connector_accepts_untagged_target():
  findings, count, tagged, untagged = (
    _connector_findings(
      (
        r"A=B\tag{1}",
        "(1) より,",
        r"A=C",
      )
    )
  )

  assert findings == ()
  assert count == 1
  assert tagged == 0
  assert untagged == 1


def test_phase158_r5_5_closure_connector_rejects_late_source():
  findings, count, tagged, untagged = (
    _connector_findings(
      (
        "(1) より,",
        r"A=C",
        r"A=B\tag{1}",
      )
    )
  )

  assert count == 1
  assert tagged == 0
  assert untagged == 0
  assert len(
    findings
  ) == 1
  assert findings[
    0
  ][
    1
  ] == "MISSING_OR_LATE_SOURCE"
