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


def _render(
  n: int,
  k: int,
  depth: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def main():
  rendered = _render(
    2,
    2,
    2,
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  diagnostics = {
    "(5.2) general Reference": (
      "**[R1] (5.2).**"
      in reference
      and r"\pi_{i}^{3}"
      in reference
      and r"\pi_{i}^{2}"
      in reference
    ),
    "Proposition 4.4 absent": (
      "Proposition 4.4"
      not in rendered
    ),
    "general Prop44 map absent from body": (
      (
        r"\pi_{i - 1}^{1} \oplus "
        r"\pi_{i}^{3} \to "
        r"\pi_{i}^{2}"
      )
      not in body
    ),
    "second-summand prose absent": (
      "分解写像の第二成分"
      not in body
    ),
    "specialized (5.2) application": (
      "[R1]"
      in body
      and "$i=4$"
      in body
      and r"\pi_{4}^{3} \to \pi_{4}^{2}"
      in body
      and "同型"
      in body
    ),
    "source group shown": (
      r"\pi_{4}^{3} = "
      r"\mathbb{Z}/2\{\eta_{3}\}"
      in body
    ),
    "generator transport shown": (
      r"\eta_{3} \mapsto "
      r"\eta_{2}\eta_{3}"
      in body
    ),
    "target conclusion shown": (
      r"\pi_{4}^{2} = "
      r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
      in body
    ),
    "QED shown": (
      "□"
      in body
    ),
  }

  print(
    "=" * 78
  )
  print(
    "Phase 161-R4 closure - pi_4^2"
  )
  print(
    "=" * 78
  )
  print()
  print(
    rendered
  )
  print()
  print(
    "=" * 78
  )
  print(
    "Closure diagnostics"
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
      "Phase 161-R4 closure failed: "
      + ", ".join(
        failed
      )
    )

  print()
  print(
    "Phase 161-R4 completion criteria: PASS"
  )


if __name__ == "__main__":
  main()
