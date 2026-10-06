from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
ROOT_TEXT = str(
  ROOT
)

if ROOT_TEXT not in sys.path:
  sys.path.insert(
    0,
    ROOT_TEXT,
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET = r"E: \pi_{4}^{2} \to \pi_{5}^{3}"


def main() -> None:
  report = build_standard_toda_report(
    n=3,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 pi_5^3 numbered-reasoning focused audit"
  )
  print(
    "=" * 78
  )

  marker = "## 証明\n\n"
  parts = rendered.split(
    marker,
    1,
  )
  proof = (
    parts[1]
    if len(
      parts
    ) == 2
    else rendered
  )

  print()
  print(
    "[ALL TARGET-MAP PUBLIC LINES]"
  )

  target_lines = []

  for line_number, line in enumerate(
    proof.splitlines(),
    start=1,
  ):
    if TARGET in line:
      target_lines.append(
        (
          line_number,
          line,
        )
      )
      print(
        f"line {line_number}: {line}"
      )

  print()
  print(
    "[FULL PROOF BODY]"
  )
  print(
    proof
  )

  print()
  print(
    "=" * 78
  )
  print(
    "SUMMARY"
  )
  print(
    "=" * 78
  )
  print(
    "target-map lines:",
    len(
      target_lines
    ),
  )
  print(
    "has injective:",
    any(
      "は単射."
      in line
      for _, line in target_lines
    ),
  )
  print(
    "has surjective:",
    any(
      "は全射."
      in line
      for _, line in target_lines
    ),
  )
  print(
    "has isomorphism:",
    any(
      (
        "は同型."
        in line
        or "は同型写像."
        in line
        or "は同型である."
        in line
        or "は同型写像である."
        in line
      )
      for _, line in target_lines
    ),
  )
  print(
    "Production code changes: none"
  )
  print(
    "Test code changes: none"
  )
  print(
    "Full pytest: not run"
  )


if __name__ == "__main__":
  main()
