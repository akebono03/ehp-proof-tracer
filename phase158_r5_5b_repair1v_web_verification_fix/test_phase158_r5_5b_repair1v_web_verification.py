from __future__ import annotations

import sys
from pathlib import Path


REPOSITORY_ROOT = Path(
  __file__
).resolve().parents[
  1
]

if str(
  REPOSITORY_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _proof_text(
  n: int,
  k: int,
) -> str:
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )
  parts = []
  in_proof = False

  for line in view.rendered_lines:
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
      continue

    parts.append(
      line.prefix
      + (
        ""
        if line.statement_latex is None
        else line.statement_latex
      )
      + line.suffix
    )

  return "\n".join(
    parts
  )


def test_phase158_r5_5b_repair1v_web_verification_import_and_render():
  pi6 = _proof_text(
    3,
    3,
  )

  assert r"\tag{1}" in pi6
  assert r"\tag{2}" in pi6
  assert r"\tag{3}" in pi6
  assert "(1) と (2) より," in pi6

  equation_one = (
    r"2\nu' = "
    r"\eta_{3}\eta_{4}\eta_{5}\tag{1}"
  )
  equation_two = (
    r"\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}"
  )
  connector = "(1) と (2) より,"
  equation_three = (
    r"2\nu' = \eta_{3}^{3}\tag{3}"
  )
  order_statement = (
    r"\operatorname{ord}\left("
    r"\eta_{3}^{3}"
    r"\right) = 2"
  )

  assert (
    pi6.index(
      equation_one
    )
    < pi6.index(
      equation_two
    )
    < pi6.index(
      connector
    )
    < pi6.index(
      equation_three
    )
    < pi6.index(
      order_statement
    )
  )

  pi7 = _proof_text(
    4,
    3,
  )
  pi15 = _proof_text(
    8,
    7,
  )

  assert pi7
  assert pi15
