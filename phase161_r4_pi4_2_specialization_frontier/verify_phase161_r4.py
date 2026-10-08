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
    "Phase 161-R4 diagnostics"
  )
  print(
    "=" * 78
  )
  print(
    "(5.2) general Reference:",
    (
      "**[R1] (5.2).**" in reference
      and r"\pi_{i}^{3}" in reference
      and r"\pi_{i}^{2}" in reference
    ),
  )
  print(
    "Proposition 4.4 pruned:",
    "Proposition 4.4" not in reference,
  )
  print(
    "specialized body map:",
    (
      r"\pi_{4}^{3} \to \pi_{4}^{2}"
      in body
    ),
  )
  print(
    "generic i removed from body:",
    (
      r"\pi_{i}^{3}" not in body
      and r"\pi_{i}^{2}" not in body
      and r"\pi_{i - 1}^{1}" not in body
    ),
  )
  print(
    "generator transport shown:",
    r"\eta_{3} \mapsto" in body,
  )


if __name__ == "__main__":
  main()
