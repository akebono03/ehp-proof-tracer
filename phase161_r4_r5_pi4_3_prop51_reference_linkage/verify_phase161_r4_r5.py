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
    "Phase 161-R4-R5 diagnostics"
  )
  print(
    "=" * 78
  )
  print(
    "Proposition 5.1 Reference:",
    "Proposition 5.1"
    in reference,
  )
  print(
    "(5.2) Reference:",
    "(5.2)"
    in reference,
  )
  print(
    "general higher-eta statement:",
    (
      r"\pi_{n + 1}^{n}"
      in reference
      or r"\pi_{n+1}^{n}"
      in reference
    ),
  )
  print(
    "pi_4^3 concrete body:",
    (
      r"\pi_{4}^{3} = "
      r"\mathbb{Z}/2\{\eta_{3}\}"
      in body
    ),
  )
  print(
    "pi_4^3 paragraph has Reference marker:",
    any(
      "[R"
      in paragraph
      and (
        r"\pi_{4}^{3} = "
        r"\mathbb{Z}/2\{\eta_{3}\}"
      )
      in paragraph
      for paragraph in body.split(
        "\n\n"
      )
    ),
  )
  print(
    "pi_4^2 conclusion:",
    (
      r"\pi_{4}^{2} = "
      r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
      in body
    ),
  )


if __name__ == "__main__":
  main()
