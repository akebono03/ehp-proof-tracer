from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(ROOT),
  )

from web_group_proof import (
  build_standard_web_group_proof_view,
)


def render_public_lines(view):
  lines = []

  for line in view.rendered_lines:
    if line.kind == "heading":
      text = "## " + line.prefix
    elif line.kind == "separator":
      text = "---"
    elif line.segments:
      parts = []
      for segment in line.segments:
        if segment.kind in (
          "inline_math",
          "display_math",
        ):
          parts.append(
            "$"
            + segment.value
            + "$"
          )
        elif segment.kind == "strong":
          parts.append(
            "**"
            + segment.value
            + "**"
          )
        else:
          parts.append(
            segment.value
          )
      text = "".join(
        parts
      )
    elif line.statement_latex is not None:
      text = (
        line.prefix
        + "$"
        + line.statement_latex
        + "$"
        + line.suffix
      )
    else:
      text = (
        line.prefix
        + line.suffix
      )

    lines.append(
      text
    )

  return tuple(
    lines
  )


def main() -> int:
  view = (
    build_standard_web_group_proof_view(
      3,
      1,
      max_depth=2,
      mode="narrative",
    )
  )

  rendered = "\n".join(
    render_public_lines(
      view
    )
  )

  print(
    "=============================================================="
  )
  print(
    "Phase 159 pi_4^3 repair2 public Narrative"
  )
  print(
    "=============================================================="
  )
  print(
    rendered
  )
  print(
    "=============================================================="
  )

  if (
    "TodaEtaFamilyDefinitionStatement"
    in rendered
  ):
    raise AssertionError(
      "internal eta definition leaked into public Narrative"
    )

  print(
    "PUBLIC_NARRATIVE_AUDIT=PASS"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
