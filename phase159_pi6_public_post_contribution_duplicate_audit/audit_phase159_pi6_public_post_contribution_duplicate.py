from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(ROOT),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
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


TARGET = (
  r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
)


def _base_presentation():
  report = build_standard_toda_report(
    n=3,
    k=3,
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
  return build_toda_group_proof_presentation(
    replay
  )


def _print_stage(
  label: str,
  rendered: str,
) -> None:
  print("")
  print("=" * 78)
  print(label)
  print("=" * 78)
  print(
    "target occurrence count:",
    rendered.count(
      TARGET
    ),
  )

  paragraphs = rendered.split(
    "\n\n"
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if TARGET not in paragraph:
      continue

    print("")
    print(
      f"[paragraph {index}]"
    )
    print(
      paragraph.strip()
    )

    start = max(
      0,
      index - 2,
    )
    end = min(
      len(
        paragraphs
      ),
      index + 3,
    )

    print("")
    print("context:")
    for context_index in range(
      start,
      end,
    ):
      marker = (
        ">>"
        if context_index == index
        else "  "
      )
      print(
        f"{marker} [{context_index}] "
        + paragraphs[
          context_index
        ].strip().replace(
          "\n",
          " / ",
        )
      )


def main() -> None:
  base = _base_presentation()
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      base
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

  contribution = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  _print_stage(
    "1. CONTRIBUTION RENDERER",
    contribution,
  )

  wrapped = (
    _wrap_phase150_rc4_generic_public_narrative(
      presentation,
      contribution,
    )
  )
  _print_stage(
    "2. PUBLIC WRAPPER",
    wrapped,
  )

  finalized = (
    _finalize_toda_group_proof_narrative_markdown(
      wrapped
    )
  )
  _print_stage(
    "3. FINALIZER",
    finalized,
  )

  normalized = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      finalized,
    )
  )
  _print_stage(
    "4. PHASE158 PUBLIC NORMALIZATION",
    normalized,
  )


if __name__ == "__main__":
  main()
