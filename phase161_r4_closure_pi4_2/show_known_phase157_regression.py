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


def main():
  report = build_standard_toda_report(
    n=3,
    k=3,
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
  reference = rendered.split(
    "---",
    1,
  )[0]

  print(
    "=" * 78
  )
  print(
    "Known pre-existing Phase157 pi_6^3 Reference regression"
  )
  print(
    "=" * 78
  )
  print(
    "Proposition 2.2 present:",
    "Proposition 2.2"
    in reference,
  )
  print(
    "(5.7) present:",
    "(5.7)"
    in reference,
  )
  print()
  print(
    "Expected current contract:"
  )
  print(
    "R1 Proposition 5.6"
  )
  print(
    "R2 (5.3)"
  )
  print(
    "R3 Proposition 5.3"
  )
  print(
    "R4 Proposition 5.1"
  )
  print(
    "R5 Proposition 2.2"
  )
  print()
  print(
    "This diagnostic is informational only and is not a Phase161-R4 gate."
  )


if __name__ == "__main__":
  main()
