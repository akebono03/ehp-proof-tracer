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
  _phase158_baseline_render_toda_group_proof_narrative_markdown,
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


def _fresh_presentation():
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


def _manual_baseline(
  base,
) -> str:
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      base
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      closure
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      closure,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      closure,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )
  contribution = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      closure,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  wrapped = (
    _wrap_phase150_rc4_generic_public_narrative(
      closure,
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
  base_for_manual = _fresh_presentation()
  manual = _manual_baseline(
    base_for_manual
  )
  _print_stage(
    "1. MANUAL BASELINE ON FRESH PRESENTATION",
    manual,
  )

  base_for_baseline = _fresh_presentation()
  baseline = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      base_for_baseline
    )
  )
  _print_stage(
    "2. ACTUAL BASELINE FUNCTION ON FRESH PRESENTATION",
    baseline,
  )

  normalized_baseline = (
    _phase158_normalize_public_narrative_contract(
      base_for_baseline,
      baseline,
    )
  )
  _print_stage(
    "3. NORMALIZED ACTUAL BASELINE",
    normalized_baseline,
  )

  base_for_direct = _fresh_presentation()
  direct = (
    render_toda_group_proof_narrative_markdown(
      base_for_direct
    )
  )
  _print_stage(
    "4. DIRECT PUBLIC ON FRESH PRESENTATION",
    direct,
  )

  print("")
  print("=" * 78)
  print("EQUALITY SUMMARY")
  print("=" * 78)
  print(
    "manual == baseline:",
    manual == baseline,
  )
  print(
    "normalized baseline == direct:",
    normalized_baseline == direct,
  )

  base_for_closure_chain = _fresh_presentation()
  closure1 = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      base_for_closure_chain
    )
  )
  closure2 = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      closure1
    )
  )

  print("")
  print("=" * 78)
  print("SEMANTIC CLOSURE IDEMPOTENCE")
  print("=" * 78)
  print(
    "base nodes:",
    len(
      base_for_closure_chain.nodes
    ),
  )
  print(
    "closure1 nodes:",
    len(
      closure1.nodes
    ),
  )
  print(
    "closure2 nodes:",
    len(
      closure2.nodes
    ),
  )
  print(
    "closure1 is closure2:",
    closure1 is closure2,
  )

  closure1_contribution = _manual_baseline(
    base_for_closure_chain
  )
  closure2_contribution = _manual_baseline(
    closure1
  )

  _print_stage(
    "5. MANUAL BASELINE FROM BASE",
    closure1_contribution,
  )
  _print_stage(
    "6. MANUAL BASELINE FROM CLOSURE1",
    closure2_contribution,
  )


if __name__ == "__main__":
  main()
