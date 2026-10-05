from __future__ import annotations

from audit_phase158_r5_5d import (
  _duplicate_visible_conclusions,
  _interval_crosses,
  _transition_findings_from_paragraphs,
)


def test_phase158_r5_5d_crossing_interval_detector():
  assert _interval_crosses(
    (
      2,
      6,
    ),
    (
      4,
      8,
    ),
  )
  assert not _interval_crosses(
    (
      2,
      4,
    ),
    (
      5,
      8,
    ),
  )
  assert not _interval_crosses(
    (
      2,
      8,
    ),
    (
      4,
      6,
    ),
  )


def test_phase158_r5_5d_transition_detector_accepts_following_target():
  findings = _transition_findings_from_paragraphs(
    (
      "以上より,",
      "$A=B$",
    )
  )

  assert findings == ()


def test_phase158_r5_5d_transition_detector_flags_dangling_transition():
  findings = _transition_findings_from_paragraphs(
    (
      "$A=B$",
      "以上より,",
      "したがって,",
    )
  )

  assert len(
    findings
  ) == 2


def test_phase158_r5_5d_duplicate_conclusion_detector():
  body = (
    "$A=B$\n"
    "$C=D$\n"
    "$A=B$\n"
  )
  findings = _duplicate_visible_conclusions(
    body,
    (
      (
        0,
        "$A=B$",
      ),
      (
        1,
        "$C=D$",
      ),
    ),
  )

  assert len(
    findings
  ) == 1
  assert findings[
    0
  ][
    0
  ] == 0
  assert findings[
    0
  ][
    2
  ] == (
    1,
    3,
  )
