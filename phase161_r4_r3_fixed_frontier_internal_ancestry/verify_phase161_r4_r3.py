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
    "Phase 161-R4-R3 diagnostics"
  )
  print(
    "=" * 78
  )
  print(
    "(5.2) Reference:",
    "**[R1] (5.2).**" in reference,
  )
  print(
    "Proposition 4.4 absent from Reference:",
    "Proposition 4.4" not in reference,
  )
  print(
    "Prop44 general map absent from body:",
    (
      r"\pi_{i - 1}^{1} \oplus "
      r"\pi_{i}^{3} \to "
      r"\pi_{i}^{2}"
    )
    not in body,
  )
  print(
    "second-summand restriction absent:",
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
      and "同型" in body
    ),
  )
  print(
    "generator transport present:",
    r"\eta_{3} \mapsto" in body,
  )


if __name__ == "__main__":
  main()
