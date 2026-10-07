from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


NEEDLES = (
  r"\ker \Delta",
  "零写像",
  r"\pi_{5}^{2} \to \pi_{6}^{3}",
)


def report(
  name: str,
  markdown: str,
) -> None:
  print(
    "=============================================================="
  )
  print(
    name
  )
  print(
    "=============================================================="
  )

  paragraphs = markdown.split(
    "\n\n"
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if any(
      needle in paragraph
      for needle in NEEDLES
    ):
      print(
        "P"
        + str(
          index
        )
        + ": "
        + repr(
          paragraph
        )
      )

  print()


def main() -> int:
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  contribution = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  public = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  report(
    "CONTRIBUTION",
    contribution,
  )
  report(
    "PUBLIC",
    public,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
