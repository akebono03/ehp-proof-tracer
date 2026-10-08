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

  diagnostics = {
    "Prop.5.1 general Reference": (
      (
        r"\pi_{n + 1}^{n} = "
        r"\mathbb{Z}/2\{\eta_{n}\}"
      )
      in reference
    ),
    "Prop.5.1 general absent from body": (
      (
        r"\pi_{n + 1}^{n} = "
        r"\mathbb{Z}/2\{\eta_{n}\}"
      )
      not in body
    ),
    "Prop.5.1 marker on pi_4^3": (
      marker
      in pi4_3_paragraph
    ),
    "no Prop.4.4 public Reference": (
      "Proposition 4.4"
      not in reference
    ),
    "no nested R2/R1 marker": (
      "[R2]より, [R1]より"
      not in body
    ),
    "(5.2) Reference": (
      "(5.2)"
      in reference
    ),
    "i=4 specialization": (
      "$i=4$"
      in body
      and (
        r"\pi_{4}^{3} \to "
        r"\pi_{4}^{2}"
      )
      in body
    ),
    "generator transport": (
      (
        r"\eta_{3} \mapsto "
        r"\eta_{2}\eta_{3}"
      )
      in body
    ),
    "target conclusion": (
      (
        r"\pi_{4}^{2} = "
        r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
      )
      in body
    ),
    "QED": (
      "□"
      in body
    ),
  }

  print()
  print(
    "=" * 78
  )
  print(
    "Phase 161-R4-R5 repair6 diagnostics"
  )
  print(
    "=" * 78
  )

  for label, result in diagnostics.items():
    print(
      f"{label}: {result}"
    )

  failed = tuple(
    label
    for label, result in diagnostics.items()
    if not result
  )

  if failed:
    raise SystemExit(
      "Repair6 verification failed: "
      + ", ".join(
        failed
      )
    )


if __name__ == "__main__":
  main()
