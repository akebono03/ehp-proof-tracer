from pathlib import Path
import re
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
  bad_reference_derivation = re.compile(
    r"\[R[0-9]+\].{0,20}を得る[。.]"
  )

  print(
    "=" * 72
  )
  print(
    "Phase 153-R8 Reference-use prose normalization audit"
  )
  print(
    "=" * 72
  )

  for label, n, k in TARGETS:
    body = render_body(
      n,
      k,
    )
    matches = tuple(
      bad_reference_derivation.findall(
        body
      )
    )

    print(
      f"{label}: chars={len(body)} "
      f"reference-as-derived={len(matches)}"
    )

    if matches:
      failures.append(
        (
          label,
          matches,
        )
      )

    if label == "pi6_2":
      if "[R2]を用いる。" not in body:
        failures.append(
          (
            label,
            "missing normalized [R2] use",
          )
        )

      if (
        r"このことから、$γ \mapsto \eta_{2}γ$を得る。"
        not in body
      ):
        failures.append(
          (
            label,
            "non-reference derivation changed unexpectedly",
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
    "Reference markers are no longer rendered as derived results."
  )


if __name__ == "__main__":
  main()
