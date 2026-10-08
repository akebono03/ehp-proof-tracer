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
    max_depth=3,
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

  prop51_number = next(
    number
    for number in range(
      1,
      5,
    )
    if (
      f"**[R{number}] Proposition 5.1.**"
      in reference
    )
  )
  marker = (
    "[R"
    + str(
      prop51_number
    )
    + "]"
  )

  pi4_3_paragraph = next(
    (
      paragraph
      for paragraph in body.split(
        "\n\n"
      )
      if (
        r"\pi_{4}^{3} = "
        r"\mathbb{Z}/2\{\eta_{3}\}"
        in paragraph
      )
    ),
    "",
  )

  print()
  print(
    "=" * 78
  )
  print(
    "Phase 161-R4-R5 repair3 diagnostics"
  )
  print(
    "=" * 78
  )
  print(
    "general Prop.5.1 in Reference:",
    (
      r"\pi_{n + 1}^{n} = "
      r"\mathbb{Z}/2\{\eta_{n}\}"
      in reference
    ),
  )
  print(
    "general Prop.5.1 absent from body:",
    (
      r"\pi_{n + 1}^{n} = "
      r"\mathbb{Z}/2\{\eta_{n}\}"
      not in body
    ),
  )
  print(
    "concrete pi_4^3 body marker:",
    marker in pi4_3_paragraph,
  )
  print(
    "pi_4^3 paragraph:",
    pi4_3_paragraph,
  )
  print(
    "(5.2) remains:",
    "(5.2)" in reference,
  )
  print(
    "target conclusion remains:",
    (
      r"\pi_{4}^{2} = "
      r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
      in body
    ),
  )


if __name__ == "__main__":
  main()
