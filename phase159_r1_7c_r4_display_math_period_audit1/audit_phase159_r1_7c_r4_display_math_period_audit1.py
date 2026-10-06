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


N_RANGE = range(
  2,
  16,
)
K_RANGE = range(
  0,
  8,
)
MAX_DEPTH = 2


def _label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(
      n + k
    )
    + "^"
    + str(
      n
    )
  )


def _render(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      "no report candidate"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=MAX_DEPTH,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _display_math_blocks(
  markdown: str,
) -> tuple[
  str,
  ...,
]:
  blocks = []
  position = 0

  while True:
    start = markdown.find(
      r"\[",
      position,
    )

    if start < 0:
      break

    end = markdown.find(
      r"\]",
      start + 2,
    )

    if end < 0:
      break

    blocks.append(
      markdown[
        start:
        end + 2
      ]
    )
    position = (
      end + 2
    )

  return tuple(
    blocks
  )


def _last_math_line(
  block: str,
) -> str | None:
  lines = [
    line.strip()
    for line in block.splitlines()
    if line.strip()
    not in (
      r"\[",
      r"\]",
    )
  ]

  if not lines:
    return None

  return lines[
    -1
  ]


def main() -> None:
  rendered_count = 0
  failed = []
  display_block_count = 0
  affected_outputs = []
  missing_period_count = 0

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 display-math period audit1"
  )
  print(
    "=" * 78
  )
  print(
    "audit range: n=2..15, k=0..7"
  )
  print(
    "This range is an audit sample, not a permanent group-count contract."
  )
  print()

  for n in N_RANGE:
    for k in K_RANGE:
      label = _label(
        n,
        k,
      )

      try:
        rendered = _render(
          n,
          k,
        )
      except Exception as exc:
        failed.append(
          (
            label,
            type(
              exc
            ).__name__,
            str(
              exc
            ),
          )
        )
        continue

      rendered_count += 1
      blocks = _display_math_blocks(
        rendered
      )
      display_block_count += len(
        blocks
      )

      findings = []

      for block_index, block in enumerate(
        blocks,
        start=1,
      ):
        last_line = _last_math_line(
          block
        )

        if last_line is None:
          continue

        if last_line.endswith(
          "."
        ):
          continue

        findings.append(
          (
            block_index,
            block,
            last_line,
          )
        )

      if not findings:
        continue

      missing_period_count += len(
        findings
      )
      affected_outputs.append(
        (
          label,
          len(
            findings
          ),
        )
      )

      print(
        "-" * 78
      )
      print(
        label
      )

      for block_index, block, last_line in findings:
        print(
          f"[display block {block_index}]"
        )
        print(
          block
        )
        print(
          "[last math line]"
        )
        print(
          last_line
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
    "rendered:",
    rendered_count,
  )
  print(
    "failed:",
    len(
      failed
    ),
  )
  print(
    "display blocks:",
    display_block_count,
  )
  print(
    "affected outputs:",
    len(
      affected_outputs
    ),
  )
  print(
    "missing-period display blocks:",
    missing_period_count,
  )

  if affected_outputs:
    print()
    print(
      "[AFFECTED LABELS]"
    )
    for label, count in affected_outputs:
      print(
        label,
        "missing_period_blocks=",
        count,
      )

  if failed:
    print()
    print(
      "[FAILURES]"
    )
    for label, error_type, message in failed:
      print(
        label,
        error_type,
        message,
      )

  print()
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
