from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
ROOT_TEXT = str(
  ROOT
)

if ROOT_TEXT not in sys.path:
  sys.path.insert(
    0,
    ROOT_TEXT,
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
  merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _context(
  n: int,
  k: int,
):
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
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
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
    blocks,
    semantic_sidecar,
    arguments,
  )


def _sequence_paragraphs(
  markdown: str,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    paragraph.strip()
    for paragraph in markdown.split(
      "\n\n"
    )
    if (
      r"\xrightarrow{"
      in paragraph
    )
  )


def _print_case(
  n: int,
  k: int,
  label: str,
) -> None:
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _context(
    n,
    k,
  )

  before = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  after = (
    merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
      presentation,
      before,
    )
  )

  print(
    "=" * 78
  )
  print(
    label
  )
  print(
    "=" * 78
  )

  print(
    "\n[BEFORE MERGE]"
  )
  before_sequences = (
    _sequence_paragraphs(
      before
    )
  )
  for index, paragraph in enumerate(
    before_sequences,
    start=1,
  ):
    print(
      f"{index:02d}: {paragraph}"
    )

  print(
    "\n[AFTER MERGE]"
  )
  after_sequences = (
    _sequence_paragraphs(
      after
    )
  )
  for index, paragraph in enumerate(
    after_sequences,
    start=1,
  ):
    print(
      f"{index:02d}: {paragraph}"
    )

  print(
    "\n[COUNTS]"
  )
  print(
    "before:",
    len(
      before_sequences
    ),
  )
  print(
    "after:",
    len(
      after_sequences
    ),
  )


def main() -> None:
  _print_case(
    2,
    1,
    "pi_3^2",
  )
  _print_case(
    3,
    3,
    "pi_6^3",
  )


if __name__ == "__main__":
  main()
