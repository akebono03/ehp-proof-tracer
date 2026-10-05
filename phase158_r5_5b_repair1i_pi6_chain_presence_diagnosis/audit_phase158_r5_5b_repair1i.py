from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from web_group_proof import (
  build_standard_web_group_proof_view,
)


EXPECTED = (
  (
    "equation_one",
    (
      r"$2\nu' = "
      r"\eta_{3}\eta_{4}\eta_{5}\tag{1}$"
    ),
  ),
  (
    "equation_two",
    (
      r"$\eta_{3}\eta_{4}\eta_{5} = "
      r"\eta_{3}^{3}\tag{2}$"
    ),
  ),
  (
    "connector",
    "(1) と (2) より,",
  ),
  (
    "equation_three",
    r"$2\nu' = \eta_{3}^{3}\tag{3}$",
  ),
  (
    "order_statement",
    (
      r"$\operatorname{ord}\left("
      r"\eta_{3}^{3}"
      r"\right) = 2$"
    ),
  ),
)


def web_line_text(
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


def web_proof_body() -> str:
  view = build_standard_web_group_proof_view(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )
  lines = []
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

    text = web_line_text(
      line
    )

    if text.strip():
      lines.append(
        text
      )

  return "\n".join(
    lines
  )


def multi_argument_body() -> str:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def describe(
  label: str,
  text: str,
) -> list[str]:
  lines = [
    label,
    "-" * 100,
  ]

  previous_index = None

  for name, expected in EXPECTED:
    index = text.find(
      expected
    )
    present = index >= 0
    ordered_after_previous = (
      None
      if (
        not present
        or previous_index is None
      )
      else index > previous_index
    )

    lines.append(
      (
        f"{name}: "
        f"present={present} "
        f"index={index} "
        f"after_previous={ordered_after_previous}"
      )
    )
    lines.append(
      "  expected="
      + expected
    )

    if present:
      previous_index = index

  lines.extend(
    (
      "",
      "FULL OUTPUT",
      "-" * 100,
      text,
      "",
    )
  )

  return lines


def main() -> int:
  multi = multi_argument_body()
  web = web_proof_body()

  lines = [
    "=" * 100,
    "Phase 158-R5-5b repair1i - pi6 chain presence diagnosis",
    "=" * 100,
    "",
  ]

  lines.extend(
    describe(
      "A. MULTI-ARGUMENT OUTPUT",
      multi,
    )
  )
  lines.extend(
    describe(
      "B. WEB DEPTH=2 PROOF BODY",
      web,
    )
  )

  lines.extend(
    (
      "=" * 100,
      "Production code changes: none",
      "Repository-wide pytest: not run",
      "=" * 100,
    )
  )

  output_dir = (
    Path(__file__).resolve().parent
    / "audit_output"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )
  (
    output_dir
    / "pi6_chain_presence.txt"
  ).write_text(
    "\n".join(
      lines
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
  )

  print(
    "\n".join(
      lines
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
