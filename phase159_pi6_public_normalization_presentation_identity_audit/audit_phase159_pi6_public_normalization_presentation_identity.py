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


def _render_pre_normalization(
  closure_presentation,
) -> str:
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      closure_presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      closure_presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      closure_presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  contribution = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      closure_presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  wrapped = (
    _wrap_phase150_rc4_generic_public_narrative(
      closure_presentation,
      contribution,
    )
  )

  return _finalize_toda_group_proof_narrative_markdown(
    wrapped
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

  for index, paragraph in enumerate(
    rendered.split(
      "\n\n"
    )
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


def main() -> None:
  base = _base_presentation()
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      base
    )
  )
  finalized = _render_pre_normalization(
    closure
  )

  _print_stage(
    "PRE-NORMALIZATION",
    finalized,
  )

  normalized_with_base = (
    _phase158_normalize_public_narrative_contract(
      base,
      finalized,
    )
  )
  _print_stage(
    "NORMALIZED WITH BASE PRESENTATION",
    normalized_with_base,
  )

  normalized_with_closure = (
    _phase158_normalize_public_narrative_contract(
      closure,
      finalized,
    )
  )
  _print_stage(
    "NORMALIZED WITH CLOSURE PRESENTATION",
    normalized_with_closure,
  )

  direct_public = (
    render_toda_group_proof_narrative_markdown(
      base
    )
  )
  _print_stage(
    "DIRECT render_toda_group_proof_narrative_markdown(BASE)",
    direct_public,
  )

  print("")
  print("=" * 78)
  print("IDENTITY SUMMARY")
  print("=" * 78)
  print(
    "base is closure:",
    base is closure,
  )
  print(
    "base node count:",
    len(
      base.nodes
    ),
  )
  print(
    "closure node count:",
    len(
      closure.nodes
    ),
  )
  print(
    "normalized(base) == direct public:",
    normalized_with_base
    == direct_public,
  )
  print(
    "normalized(closure) == direct public:",
    normalized_with_closure
    == direct_public,
  )


if __name__ == "__main__":
  main()
