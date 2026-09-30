from collections import Counter

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_latex,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)


CASES = (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _build_case(n: int, k: int):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_complete_toda_group_result_proof_replay(
    group_result
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    sidecar,
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
    rendered,
  )


def _block_text(block) -> str:
  parts = []
  for step in block.steps:
    latex = _render_group_proof_narrative_latex(
      step
    )
    if latex:
      parts.append(
        "$" + latex + "$"
      )
      continue
    parts.append(
      type(
        step.conclusion
      ).__name__
    )
  return " | ".join(
    parts
  )


def _argument_index_by_target_id(arguments):
  return {
    id(
      argument.conclusion_block
    ): index
    for index, argument in enumerate(
      arguments
    )
  }


def _visible_in_rendered(
  block,
  rendered: str,
) -> bool:
  for step in block.steps:
    latex = _render_group_proof_narrative_latex(
      step
    )
    if (
      latex
      and latex in rendered
    ):
      return True
  return False


def _classify_derivation(
  source_blocks,
  local_body_blocks,
  conclusion_block,
  rendered,
):
  local_ids = {
    id(
      block
    )
    for block in local_body_blocks
  }
  source_in_local = tuple(
    id(
      block
    ) in local_ids
    for block in source_blocks
  )
  source_visible = tuple(
    _visible_in_rendered(
      block,
      rendered,
    )
    for block in source_blocks
  )
  conclusion_visible = _visible_in_rendered(
    conclusion_block,
    rendered,
  )

  if (
    source_in_local
    and all(
      source_in_local
    )
    and conclusion_visible
  ):
    if any(
      source_visible
    ):
      return (
        "VISIBLE_LOCAL_DERIVATION"
      )
    return (
      "HIDDEN_SOURCE_LOCAL_DERIVATION"
    )

  if conclusion_visible:
    return (
      "PARTIAL_LOCAL_DERIVATION"
    )

  return (
    "NONVISIBLE_DERIVATION"
  )


def audit_case(
  label: str,
  n: int,
  k: int,
) -> Counter:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
    rendered,
  ) = _build_case(
    n,
    k,
  )

  transitions = (
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    )
  )
  argument_index_by_target_id = (
    _argument_index_by_target_id(
      arguments
    )
  )

  counts = Counter()

  print(
    "=" * 110
  )
  print(
    label
  )
  print(
    "=" * 110
  )
  print(
    f"blocks={len(blocks)}"
  )
  print(
    f"arguments={len(arguments)}"
  )

  derivation_number = 0

  for transition in transitions:
    if (
      transition.role
      is not TodaGroupProofNarrativeTransitionRole.DERIVATION
    ):
      continue

    argument_index = argument_index_by_target_id.get(
      id(
        transition.target_block
      )
    )
    if argument_index is None:
      continue

    argument = arguments[
      argument_index
    ]
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    classification = _classify_derivation(
      transition.source_blocks,
      local_body_blocks,
      transition.target_block,
      rendered,
    )
    counts[
      classification
    ] += 1

    local_ids = {
      id(
        block
      )
      for block in local_body_blocks
    }
    source_in_local = tuple(
      id(
        block
      ) in local_ids
      for block in transition.source_blocks
    )
    source_visible = tuple(
      _visible_in_rendered(
        block,
        rendered,
      )
      for block in transition.source_blocks
    )
    conclusion_visible = _visible_in_rendered(
      transition.target_block,
      rendered,
    )

    print()
    print(
      f"DERIVATION {label} D{derivation_number:02d}"
    )
    print(
      f"  CLASS={classification}"
    )
    print(
      f"  argument_index=A{argument_index:02d}"
    )
    print(
      f"  argument_role={argument.role.value}"
    )
    print(
      f"  source_count={len(transition.source_blocks)}"
    )
    print(
      f"  source_in_local_body={source_in_local}"
    )
    print(
      f"  source_visible={source_visible}"
    )
    print(
      f"  conclusion_visible={conclusion_visible}"
    )

    for source_number, source_block in enumerate(
      transition.source_blocks
    ):
      print(
        f"  SOURCE S{source_number:02d} "
        f"role={source_block.role.value} "
        f"text={_block_text(source_block)}"
      )

    print(
      "  LOCAL_BODY_BEGIN"
    )
    for local_number, block in enumerate(
      local_body_blocks
    ):
      marker = (
        "CONCLUSION"
        if block is transition.target_block
        else "BODY"
      )
      print(
        f"    L{local_number:02d} "
        f"{marker} "
        f"role={block.role.value} "
        f"visible={_visible_in_rendered(block, rendered)} "
        f"text={_block_text(block)}"
      )
    print(
      "  LOCAL_BODY_END"
    )
    print(
      "  CONCLUSION "
      + _block_text(
        transition.target_block
      )
    )

    derivation_number += 1

  print()
  print(
    f"CASE_DERIVATION_COUNT={derivation_number}"
  )
  print(
    f"CASE_CLASSIFICATION_COUNTS={dict(counts)}"
  )
  print(
    "RENDERED_HAS_GENERIC_GRAPH_CONNECTORS="
    + str(
      (
        "これらから" in rendered
        or "このことから" in rendered
      )
    )
  )
  print(
    "RENDERED_NARRATIVE_BEGIN"
  )
  print(
    rendered
  )
  print(
    "RENDERED_NARRATIVE_END"
  )
  print()

  return counts


def main() -> None:
  total = Counter()

  print(
    "Phase 150 RC4-7B-4 "
    "Local-Derivation Narrative Audit"
  )
  print(
    "Production changes: none"
  )
  print(
    "Audit existing DERIVATION transitions only."
  )
  print()

  for label, n, k in CASES:
    total.update(
      audit_case(
        label,
        n,
        k,
      )
    )

  visible_local = total[
    "VISIBLE_LOCAL_DERIVATION"
  ]
  hidden_source = total[
    "HIDDEN_SOURCE_LOCAL_DERIVATION"
  ]
  partial = total[
    "PARTIAL_LOCAL_DERIVATION"
  ]
  nonvisible = total[
    "NONVISIBLE_DERIVATION"
  ]

  print(
    "=" * 110
  )
  print(
    "CROSS-GROUP SUMMARY"
  )
  print(
    "=" * 110
  )
  print(
    f"CLASSIFICATION_COUNTS={dict(total)}"
  )
  print(
    f"VISIBLE_LOCAL_DERIVATION_TOTAL={visible_local}"
  )
  print(
    f"HIDDEN_SOURCE_LOCAL_DERIVATION_TOTAL={hidden_source}"
  )
  print(
    f"PARTIAL_LOCAL_DERIVATION_TOTAL={partial}"
  )
  print(
    f"NONVISIBLE_DERIVATION_TOTAL={nonvisible}"
  )

  if (
    visible_local > 0
    or hidden_source > 0
    or partial > 0
  ):
    decision = (
      "REVIEW_LOCAL_DERIVATION_RENDERING_"
      "BEFORE_PRODUCTION_CHANGE"
    )
  else:
    decision = (
      "NO_LOCAL_DERIVATION_RENDERING_"
      "CANDIDATE_FOUND"
    )

  print(
    f"AUDIT_DECISION={decision}"
  )


if __name__ == "__main__":
  main()
