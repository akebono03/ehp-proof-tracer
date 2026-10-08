from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
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


def main():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  print(rendered)

  reference, body = rendered.split(
    "---",
    1,
  )

  print()
  print("=" * 78)
  print("Phase 161-R4-R5 repair1 diagnostics")
  print("=" * 78)

  diagnostics = {
    "Proposition 5.1 Reference": (
      "Proposition 5.1" in reference
    ),
    "general pi_{n+1}^n form": (
      r"\pi_{n + 1}^{n}" in reference
      or r"\pi_{n+1}^{n}" in reference
    ),
    "general eta_n generator": (
      r"\mathbb{Z}/2\{\eta_{n}\}"
      in reference
    ),
    "concrete pi_4^3 absent from Reference": (
      (
        r"\pi_{4}^{3} = "
        r"\mathbb{Z}/2\{\eta_{3}\}"
      )
      not in reference
    ),
    "concrete pi_4^3 present in body": (
      (
        r"\pi_{4}^{3} = "
        r"\mathbb{Z}/2\{\eta_{3}\}"
      )
      in body
    ),
    "(5.2) Reference remains": (
      "(5.2)" in reference
    ),
    "pi_4^2 conclusion remains": (
      (
        r"\pi_{4}^{2} = "
        r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
      )
      in body
    ),
    "QED": (
      "□" in body
    ),
  }

  for label, value in diagnostics.items():
    print(f"{label}: {value}")

  failed = [
    label
    for label, value in diagnostics.items()
    if not value
  ]

  if failed:
    raise SystemExit(
      "Repair1 verification failed: "
      + ", ".join(failed)
    )


if __name__ == "__main__":
  main()
