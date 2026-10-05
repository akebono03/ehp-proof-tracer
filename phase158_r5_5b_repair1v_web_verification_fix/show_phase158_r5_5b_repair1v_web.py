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


def line_text(
  line,
) -> str:
  if line.segments:
    return "".join(
      segment.value
      for segment in line.segments
    )

  return (
    line.prefix
    + (
      ""
      if line.statement_latex is None
      else line.statement_latex
    )
    + line.suffix
  )


for label, n, k in (
  ("pi6_3", 3, 3),
  ("pi7_4", 4, 3),
  ("pi15_8", 8, 7),
):
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )

  print(
    "=" * 100
  )
  print(
    label
  )
  print(
    "=" * 100
  )

  in_proof = False

  for index, line in enumerate(
    view.rendered_lines
  ):
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    text = line_text(
      line
    )

    if text.strip():
      print(
        f"{index:03d}: {text}"
      )
