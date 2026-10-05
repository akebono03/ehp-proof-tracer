from __future__ import annotations

from audit_phase158_r5_5d_repair1 import (
  _canonical_visible_text,
  _duplicate_visible_conclusions,
  _line_positions,
  _target_qed_finding,
)


def test_phase158_r5_5d_repair1_canonicalizes_markdown_math_to_web_text():
  assert (
    _canonical_visible_text(
      r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    )
    ==
    _canonical_visible_text(
      r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    )
  )


def test_phase158_r5_5d_repair1_ignores_display_only_equation_tag():
  assert (
    _canonical_visible_text(
      r"$2\nu' = \eta_{3}^{3}\tag{3}$"
    )
    ==
    _canonical_visible_text(
      r"2\nu' = \eta_{3}^{3}"
    )
  )


def test_phase158_r5_5d_repair1_line_positions_match_web_math_without_dollars():
  body = (
    r"\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}"
    "\n"
    r"2\nu' = \eta_{3}^{3}\tag{3}"
    "\n"
  )

  assert _line_positions(
    body,
    r"$2\nu' = \eta_{3}^{3}$",
  ) == (
    2,
  )


def test_phase158_r5_5d_repair1_duplicate_detector_uses_canonical_form():
  body = (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    "\n"
    r"A=B"
    "\n"
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    "\n"
  )

  findings = _duplicate_visible_conclusions(
    body,
    (
      (
        0,
        r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$",
      ),
    ),
  )

  assert len(
    findings
  ) == 1
  assert findings[
    0
  ][
    2
  ] == (
    1,
    3,
  )


def test_phase158_r5_5d_repair1_target_qed_accepts_web_representation():
  body = (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    "\n"
    "□"
    "\n"
  )

  assert _target_qed_finding(
    body,
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$",
  ) is None
