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
TARGET_PHRASE = "を示す."


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


def _context_lines(
  rendered: str,
  line_index: int,
) -> tuple[
  str,
  ...,
]:
  lines = rendered.splitlines()
  start = max(
    0,
    line_index - 2,
  )
  end = min(
    len(
      lines
    ),
    line_index + 3,
  )

  return tuple(
    lines[
      start:
      end
    ]
  )


def main() -> None:
  rendered_count = 0
  failed = []
  affected = []
  occurrence_count = 0

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 proof-target 'を示す.' audit1"
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
      lines = rendered.splitlines()
      matches = tuple(
        index
        for index, line in enumerate(
          lines
        )
        if TARGET_PHRASE in line
      )

      if not matches:
        continue

      occurrence_count += len(
        matches
      )
      affected.append(
        (
          label,
          matches,
        )
      )

      print(
        "-" * 78
      )
      print(
        label
      )

      for match_number, line_index in enumerate(
        matches,
        start=1,
      ):
        print(
          f"[occurrence {match_number}] line {line_index + 1}"
        )
        for context_line in _context_lines(
          rendered,
          line_index,
        ):
          print(
            context_line
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
    "affected outputs:",
    len(
      affected
    ),
  )
  print(
    "occurrences:",
    occurrence_count,
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

  if affected:
    print()
    print(
      "[AFFECTED LABELS]"
    )
    for label, matches in affected:
      print(
        label,
        "occurrences=",
        len(
          matches
        ),
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
