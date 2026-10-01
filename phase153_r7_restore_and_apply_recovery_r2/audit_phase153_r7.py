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


def render_group(
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

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def proof_body(
  rendered,
):
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
    "Phase 153-R7 — Proof-body relevance / aggregate suppression"
  )
  print(
    "=" * 72
  )

  for label, n, k in TARGETS:
    rendered = render_group(
      n,
      k,
    )
    body = proof_body(
      rendered
    )

    print()
    print(
      f"{label}: chars={len(body)}"
    )

    if label == "pi6_2":
      forbidden_fragments = (
        r"\pi_{5}^{2}",
        r"\pi_{7}^{4}",
        r"\pi_{8}^{5}",
        r"\pi_{n + 3}^{n}",
        r"n \ge 6",
        "Toda Proposition 5.6 の有限次元結果",
      )

      for fragment in forbidden_fragments:
        if fragment in body:
          failures.append(
            (
              label,
              fragment,
            )
          )

      if "[R2]" not in body:
        failures.append(
          (
            label,
            "missing [R2] use",
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
    "The pi6_2 proof body no longer expands unconsumed "
    "Proposition 5.6 aggregate ancestry."
  )


if __name__ == "__main__":
  main()
