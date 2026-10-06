from pathlib import Path
import re
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

NUMBERED_MAP_PROPERTY = re.compile(
  r"(は単射|は全射)\.\s*\\qquad\s*\((\d+)\)"
)
CONCISE_MAP_PROPERTY = re.compile(
  r"(は単射|は全射)\."
)
ISOMORPHISM_PHRASES = (
  "は同型.",
  "は同型写像.",
  "は同型である.",
  "は同型写像である.",
)


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
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=MAX_DEPTH,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _proof_body(
  rendered: str,
) -> str:
  marker = "## 証明\n\n"
  parts = rendered.split(
    marker,
    1,
  )

  if len(
    parts
  ) != 2:
    return rendered

  return parts[
    1
  ]


def main() -> None:
  rendered_count = 0
  failed = []
  outputs_with_numbered = []
  outputs_with_unnumbered = []
  outputs_with_isomorphism = []
  numbered_count = 0
  unnumbered_count = 0
  isomorphism_count = 0

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property numbered-reasoning audit1"
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
      body = _proof_body(
        rendered
      )
      lines = body.splitlines()

      numbered_lines = []
      unnumbered_lines = []
      isomorphism_lines = []

      for line_number, line in enumerate(
        lines,
        start=1,
      ):
        if (
          "は単射."
          in line
          or "は全射."
          in line
        ):
          if NUMBERED_MAP_PROPERTY.search(
            line
          ):
            numbered_lines.append(
              (
                line_number,
                line,
              )
            )
          else:
            unnumbered_lines.append(
              (
                line_number,
                line,
              )
            )

        if any(
          phrase in line
          for phrase in ISOMORPHISM_PHRASES
        ):
          isomorphism_lines.append(
            (
              line_number,
              line,
            )
          )

      if numbered_lines:
        numbered_count += len(
          numbered_lines
        )
        outputs_with_numbered.append(
          (
            label,
            numbered_lines,
          )
        )

      if unnumbered_lines:
        unnumbered_count += len(
          unnumbered_lines
        )
        outputs_with_unnumbered.append(
          (
            label,
            unnumbered_lines,
          )
        )

      if isomorphism_lines:
        isomorphism_count += len(
          isomorphism_lines
        )
        outputs_with_isomorphism.append(
          (
            label,
            isomorphism_lines,
          )
        )

      if (
        unnumbered_lines
        or isomorphism_lines
      ):
        print(
          "-" * 78
        )
        print(
          label
        )

        if numbered_lines:
          print(
            "[NUMBERED MAP PROPERTY]"
          )
          for line_number, line in numbered_lines:
            print(
              f"line {line_number}: {line}"
            )

        if unnumbered_lines:
          print(
            "[UNNUMBERED MAP PROPERTY]"
          )
          for line_number, line in unnumbered_lines:
            print(
              f"line {line_number}: {line}"
            )

        if isomorphism_lines:
          print(
            "[ISOMORPHISM]"
          )
          for line_number, line in isomorphism_lines:
            print(
              f"line {line_number}: {line}"
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
    "outputs with numbered injective/surjective:",
    len(
      outputs_with_numbered
    ),
  )
  print(
    "numbered injective/surjective occurrences:",
    numbered_count,
  )
  print(
    "outputs with unnumbered injective/surjective:",
    len(
      outputs_with_unnumbered
    ),
  )
  print(
    "unnumbered injective/surjective occurrences:",
    unnumbered_count,
  )
  print(
    "outputs with isomorphism prose:",
    len(
      outputs_with_isomorphism
    ),
  )
  print(
    "isomorphism occurrences:",
    isomorphism_count,
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
