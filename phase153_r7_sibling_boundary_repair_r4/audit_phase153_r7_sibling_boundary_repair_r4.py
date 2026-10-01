from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
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


TARGETS = (
  ("pi4_2", 2, 2),
  ("pi5_2", 2, 3),
  ("pi6_2", 2, 4),
  ("pi7_2", 2, 5),
  ("pi8_2", 2, 6),
  ("pi9_2", 2, 7),
  ("pi10_6", 6, 4),
  ("pi12_7", 7, 5),
)


def render_body(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  marker = "## 証明\n\n"

  if marker not in rendered:
    return rendered

  return rendered.split(
    marker,
    1,
  )[1]


def main():
  failures = []

  print(
    "=" * 72
  )
  print(
    "Phase 153-R7 sibling-boundary repair R4 audit"
  )
  print(
    "=" * 72
  )

  for label, n, k in TARGETS:
    body = render_body(
      n,
      k,
    )

    print(
      f"{label}: chars={len(body)}"
    )

    if label != "pi6_2":
      continue

    for forbidden in (
      r"\pi_{5}^{2}",
      r"\pi_{7}^{4}",
      r"\pi_{8}^{5}",
      r"\pi_{n + 3}^{n}",
      r"n \ge 6",
      "Toda Proposition 5.6 の有限次元結果",
    ):
      if forbidden in body:
        failures.append(
          (
            label,
            forbidden,
          )
        )

    if "[R2]" not in body:
      failures.append(
        (
          label,
          "missing [R2]",
        )
      )

  print()

  if failures:
    print(
      "FAIL"
    )

    for failure in failures:
      print(
        "  ",
        failure,
      )

    raise SystemExit(
      1
    )

  print(
    "PASS"
  )
  print(
    "Unselected sibling branches no longer keep shared branch-only "
    "premises visible in the proof body."
  )


if __name__ == "__main__":
  main()
