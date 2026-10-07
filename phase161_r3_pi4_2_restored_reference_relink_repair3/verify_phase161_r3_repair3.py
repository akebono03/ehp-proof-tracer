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
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  print(
    rendered
  )

  reference, body = rendered.split(
    "---",
    1,
  )

  print()
  print(
    "=" * 78
  )
  print(
    "Phase 161-R3 diagnostics"
  )
  print(
    "=" * 78
  )
  print(
    "(5.2) reference:",
    "**[R1] (5.2).**" in reference,
  )
  print(
    "Proposition 4.4 reference:",
    "**[R2] Proposition 4.4.**"
    in reference,
  )
  print(
    "R1 body linkage:",
    "[R1]" in body,
  )
  print(
    "R2 body linkage:",
    "[R2]" in body,
  )


if __name__ == "__main__":
  main()
