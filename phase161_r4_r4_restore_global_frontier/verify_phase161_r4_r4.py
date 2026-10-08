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
  pi4_2 = _render(
    2,
    2,
    2,
  )

  print(
    "=" * 78
  )
  print(
    "pi_4^2 public Narrative"
  )
  print(
    "=" * 78
  )
  print(
    pi4_2
  )

  reference, body = pi4_2.split(
    "---",
    1,
  )

  print()
  print(
    "Phase 161-R4-R4 pi_4^2 diagnostics"
  )
  print(
    "(5.2) Reference:",
    "**[R1] (5.2).**" in reference,
  )
  print(
    "Proposition 4.4 absent:",
    "Proposition 4.4" not in pi4_2,
  )
  print(
    "general Prop44 body absent:",
    (
      r"\pi_{i - 1}^{1} \oplus "
      r"\pi_{i}^{3} \to "
      r"\pi_{i}^{2}"
    )
    not in body,
  )
  print(
    "second summand absent:",
    "分解写像の第二成分"
    not in body,
  )
  print(
    "specialized map present:",
    (
      "[R1]" in body
      and "$i=4$" in body
      and r"\pi_{4}^{3} \to \pi_{4}^{2}"
      in body
    ),
  )


if __name__ == "__main__":
  main()
