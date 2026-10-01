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


def main() -> None:
  targets = (
    ("pi4_2", 2, 2),
    ("pi8_5", 5, 3),
    ("pi15_8", 8, 7),
  )

  print(
    "=" * 72
  )
  print(
    "Phase 153 R13 syntax repair smoke audit"
  )
  print(
    "=" * 72
  )

  for label, n, k in targets:
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
    print(
      f"{label}: rendered chars={len(rendered)}"
    )

  print()
  print(
    "PASS"
  )


if __name__ == "__main__":
  main()
