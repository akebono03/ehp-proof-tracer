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

TAG = re.compile(
  r"\\tag\{(\d+)\}"
)
LEADING_REFERENCES = re.compile(
  r"^((?:\(\d+\)(?:,\s*|\s+と\s+)?)+)\s*より,"
)
PAREN_NUMBER = re.compile(
  r"\((\d+)\)"
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
  outputs_with_forward_refs = []
  forward_ref_count = 0
  valid_ref_count = 0

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 equation-reference order repair1 closure audit"
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
      proof = _proof_body(
        rendered
      )
      lines = proof.splitlines()

      tag_line_by_number = {}

      for line_number, line in enumerate(
        lines,
        start=1,
      ):
        for match in TAG.finditer(
          line
        ):
          number = int(
            match.group(
              1
            )
          )
          tag_line_by_number.setdefault(
            number,
            line_number,
          )

      findings = []

      for line_number, line in enumerate(
        lines,
        start=1,
      ):
        stripped = line.strip()
        match = LEADING_REFERENCES.match(
          stripped
        )

        if match is None:
          continue

        numbers = tuple(
          int(
            value
          )
          for value in PAREN_NUMBER.findall(
            match.group(
              1
            )
          )
        )

        if not numbers:
          continue

        for number in numbers:
          target_line = tag_line_by_number.get(
            number
          )

          if (
            target_line is not None
            and target_line < line_number
          ):
            valid_ref_count += 1
            continue

          forward_ref_count += 1
          findings.append(
            (
              line_number,
              number,
              target_line,
              line,
            )
          )

      if findings:
        outputs_with_forward_refs.append(
          (
            label,
            findings,
          )
        )

  if outputs_with_forward_refs:
    print(
      "[FORWARD REFERENCES]"
    )
    for label, findings in outputs_with_forward_refs:
      print(
        label
      )
      for (
        line_number,
        number,
        target_line,
        line,
      ) in findings:
        print(
          "  reference line:",
          line_number,
        )
        print(
          "  referenced number:",
          number,
        )
        print(
          "  tag line:",
          target_line,
        )
        print(
          "  text:",
          line,
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
    "outputs with forward equation references:",
    len(
      outputs_with_forward_refs
    ),
  )
  print(
    "forward equation-reference occurrences:",
    forward_ref_count,
  )
  print(
    "valid backward equation-reference occurrences:",
    valid_ref_count,
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
