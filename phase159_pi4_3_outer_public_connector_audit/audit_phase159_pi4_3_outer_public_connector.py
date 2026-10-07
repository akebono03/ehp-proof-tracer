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


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
  _finalize_toda_group_proof_narrative_markdown,
  _phase158_normalize_public_narrative_contract,
  _wrap_phase150_rc4_generic_public_narrative,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


ROOT_FRAGMENT = (
  r"\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}"
)
CONNECTOR = "以上より,"


def build_data():
  report = build_standard_toda_report(
    n=3,
    k=1,
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
  raw_presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )


def record(
  records,
  name: str,
  markdown: str,
) -> None:
  root_paragraphs = tuple(
    paragraph
    for paragraph in markdown.split(
      "\n\n"
    )
    if ROOT_FRAGMENT in paragraph
  )

  records.append(
    (
      name,
      markdown.count(
        ROOT_FRAGMENT
      ),
      markdown.count(
        CONNECTOR
      ),
      root_paragraphs,
    )
  )


def main() -> int:
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  ) = build_data()

  records = []

  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  record(
    records,
    "00_base_multi_argument",
    base,
  )

  contributions = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  record(
    records,
    "01_with_contributions",
    contributions,
  )

  wrapped = (
    _wrap_phase150_rc4_generic_public_narrative(
      presentation,
      contributions,
    )
  )
  record(
    records,
    "02_public_wrapper",
    wrapped,
  )

  finalized = (
    _finalize_toda_group_proof_narrative_markdown(
      wrapped
    )
  )
  record(
    records,
    "03_finalizer",
    finalized,
  )

  normalized = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      finalized,
    )
  )
  record(
    records,
    "04_public_contract_normalization",
    normalized,
  )

  actual_public = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  record(
    records,
    "05_actual_public_renderer",
    actual_public,
  )

  lines = [
    "# Phase 159 pi4_3 outer public connector audit",
    "",
    "root_fragment: "
    + ROOT_FRAGMENT,
    "",
  ]

  previous_connector_count = None

  for (
    name,
    root_count,
    connector_count,
    root_paragraphs,
  ) in records:
    marker = ""

    if (
      previous_connector_count is not None
      and connector_count != previous_connector_count
    ):
      marker = (
        "  <-- CONNECTOR CHANGED FROM "
        + str(
          previous_connector_count
        )
      )

    lines.append(
      name
      + ": root="
      + str(
        root_count
      )
      + ", connector="
      + str(
        connector_count
      )
      + marker
    )

    for paragraph in root_paragraphs:
      lines.append(
        "  ROOT: "
        + repr(
          paragraph
        )
      )

    previous_connector_count = connector_count

  lines.extend(
    (
      "",
      "## Contributions output",
      "",
      contributions,
      "",
      "## Wrapped output",
      "",
      wrapped,
      "",
      "## Actual public output",
      "",
      actual_public,
      "",
    )
  )

  report = "\n".join(
    lines
  )
  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_outer_public_connector_audit.txt"
  )
  output_path.write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
