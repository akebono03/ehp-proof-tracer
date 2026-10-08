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

  diagnostics = {
    "R1 is (5.2)": (
      "**[R1] (5.2).**"
      in reference
    ),
    "R2 is Proposition 5.1": (
      "**[R2] Proposition 5.1.**"
      in reference
    ),
    "R2 is general higher-eta statement": (
      (
        r"\pi_{n + 1}^{n} = "
        r"\mathbb{Z}/2\{\eta_{n}\}"
      )
      in reference
    ),
    "concrete pi4_3 absent from Reference": (
      (
        r"\pi_{4}^{3} = "
        r"\mathbb{Z}/2\{\eta_{3}\}"
      )
      not in reference
    ),
    "general higher-eta absent from body": (
      (
        r"\pi_{n + 1}^{n} = "
        r"\mathbb{Z}/2\{\eta_{n}\}"
      )
      not in body
    ),
    "R2 linked to concrete pi4_3": (
      any(
        (
          "[R2]"
          in paragraph
          and r"\pi_{4}^{3}"
          in paragraph
        )
        for paragraph in body.split(
          "\n\n"
        )
      )
    ),
    "(5.2) specialized at i=4": (
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
    "Phase 161-R4-R5 repair17 diagnostics"
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
      "Repair17 verification failed: "
      + ", ".join(
        failed
      )
    )


if __name__ == "__main__":
  main()
