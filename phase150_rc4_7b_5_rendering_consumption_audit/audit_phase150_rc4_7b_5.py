from collections import Counter

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
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
  _render_group_proof_narrative_latex,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
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

GENERIC_CONNECTORS = frozenset((
  "このことから、",
  "これらから、",
  "このことから",
  "これらから",
))


def _build_case(n: int, k: int):
  report = build_standard_toda_report(n=n, k=k)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_complete_toda_group_result_proof_replay(group_result)
  presentation = build_toda_group_proof_presentation(replay)
  presentation = build_toda_group_proof_narrative_semantic_closure_presentation(
    presentation
  )
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(presentation, sidecar)
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    sidecar,
  )
  base_markdown = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )
  contribution_markdown = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )
  public_markdown = render_toda_group_proof_narrative_markdown(presentation)
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
    base_markdown,
    contribution_markdown,
    public_markdown,
  )


def _step_token(step) -> str | None:
  latex = _render_group_proof_narrative_latex(step)
  if not latex:
    return None
  return latex


def _block_tokens(block) -> tuple[str, ...]:
  return tuple(
    token
    for token in (_step_token(step) for step in block.steps)
    if token
  )


def _block_text(block) -> str:
  tokens = _block_tokens(block)
  if tokens:
    return " | ".join("$" + token + "$" for token in tokens)
  return " | ".join(type(step.conclusion).__name__ for step in block.steps)


def _block_visible(block, markdown: str) -> bool:
  tokens = _block_tokens(block)
  return any(token in markdown for token in tokens)


def _all_blocks_visible(blocks, markdown: str) -> bool:
  return bool(blocks) and all(_block_visible(block, markdown) for block in blocks)


def _classify_consumption(
  source_blocks,
  conclusion_block,
  connector,
  base_markdown,
  contribution_markdown,
):
  source_in_base = _all_blocks_visible(source_blocks, base_markdown)
  conclusion_in_base = _block_visible(conclusion_block, base_markdown)
  source_in_contribution = _all_blocks_visible(
    source_blocks,
    contribution_markdown,
  )
  conclusion_in_contribution = _block_visible(
    conclusion_block,
    contribution_markdown,
  )
  connector_in_base = bool(connector and connector in base_markdown)

  if source_in_base and conclusion_in_base and connector_in_base:
    if connector in GENERIC_CONNECTORS:
      return "FULLY_CONSUMED_GENERIC_CONNECTOR"
    return "FULLY_CONSUMED_SPECIFIC_CONNECTOR"

  if (
    source_in_contribution
    and conclusion_in_contribution
    and not (source_in_base and conclusion_in_base)
  ):
    return "CONTRIBUTION_COMPLETES_DERIVATION"

  if source_in_contribution or conclusion_in_contribution:
    return "PARTIALLY_CONSUMED"

  return "NOT_CONSUMED"


def audit_case(label: str, n: int, k: int) -> Counter:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
    base_markdown,
    contribution_markdown,
    public_markdown,
  ) = _build_case(n, k)

  transitions = extract_toda_group_proof_narrative_transitions(
    presentation,
    blocks,
    arguments,
  )
  argument_index_by_target_id = {
    id(argument.conclusion_block): index
    for index, argument in enumerate(arguments)
  }
  counts = Counter()
  visible_local_count = 0

  print("=" * 110)
  print(label)
  print("=" * 110)
  print(f"blocks={len(blocks)}")
  print(f"arguments={len(arguments)}")

  derivation_number = 0
  for transition in transitions:
    if transition.role is not TodaGroupProofNarrativeTransitionRole.DERIVATION:
      continue

    argument_index = argument_index_by_target_id.get(id(transition.target_block))
    if argument_index is None:
      continue

    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    local_ids = {id(block) for block in local_body_blocks}
    source_in_local = tuple(
      id(block) in local_ids for block in transition.source_blocks
    )
    source_visible_public = tuple(
      _block_visible(block, public_markdown)
      for block in transition.source_blocks
    )
    conclusion_visible_public = _block_visible(
      transition.target_block,
      public_markdown,
    )

    is_visible_local = (
      bool(source_in_local)
      and all(source_in_local)
      and any(source_visible_public)
      and conclusion_visible_public
    )
    if not is_visible_local:
      continue

    visible_local_count += 1
    connector = render_toda_group_proof_narrative_transition_connector(
      transition
    )
    classification = _classify_consumption(
      transition.source_blocks,
      transition.target_block,
      connector,
      base_markdown,
      contribution_markdown,
    )
    counts[classification] += 1

    print()
    print(f"DERIVATION {label} D{derivation_number:02d}")
    print("  RC4_7B_4_CLASS=VISIBLE_LOCAL_DERIVATION")
    print(f"  CONSUMPTION_CLASS={classification}")
    print(f"  argument_index=A{argument_index:02d}")
    print(f"  argument_role={arguments[argument_index].role.value}")
    print(f"  connector={connector!r}")
    print(
      "  connector_is_generic="
      + str(connector in GENERIC_CONNECTORS)
    )
    print(
      "  connector_in_base="
      + str(bool(connector and connector in base_markdown))
    )
    print(
      "  source_in_base="
      + str(tuple(
        _block_visible(block, base_markdown)
        for block in transition.source_blocks
      ))
    )
    print(
      "  source_in_contribution="
      + str(tuple(
        _block_visible(block, contribution_markdown)
        for block in transition.source_blocks
      ))
    )
    print(
      "  conclusion_in_base="
      + str(_block_visible(transition.target_block, base_markdown))
    )
    print(
      "  conclusion_in_contribution="
      + str(_block_visible(transition.target_block, contribution_markdown))
    )
    print(
      "  conclusion_in_public="
      + str(_block_visible(transition.target_block, public_markdown))
    )

    for source_number, source_block in enumerate(transition.source_blocks):
      print(
        f"  SOURCE S{source_number:02d} "
        f"role={source_block.role.value} "
        f"text={_block_text(source_block)}"
      )
    print("  CONCLUSION " + _block_text(transition.target_block))
    derivation_number += 1

  print()
  print(f"CASE_VISIBLE_LOCAL_DERIVATION_COUNT={visible_local_count}")
  print(f"CASE_CONSUMPTION_COUNTS={dict(counts)}")
  print(
    "CASE_GENERIC_CONNECTOR_TOTAL="
    + str(counts["FULLY_CONSUMED_GENERIC_CONNECTOR"])
  )
  print(
    "CASE_SPECIFIC_CONNECTOR_TOTAL="
    + str(counts["FULLY_CONSUMED_SPECIFIC_CONNECTOR"])
  )
  print(
    "CASE_CONTRIBUTION_COMPLETES_TOTAL="
    + str(counts["CONTRIBUTION_COMPLETES_DERIVATION"])
  )
  print(
    "CASE_PARTIAL_OR_MISSING_TOTAL="
    + str(
      counts["PARTIALLY_CONSUMED"]
      + counts["NOT_CONSUMED"]
    )
  )
  print()
  return counts


def main() -> None:
  total = Counter()

  print("Phase 150 RC4-7B-5 Rendering Consumption Audit")
  print("Production changes: none")
  print("Scope: RC4-7B-4 VISIBLE_LOCAL_DERIVATION cases only.")
  print()

  for label, n, k in CASES:
    total.update(audit_case(label, n, k))

  generic = total["FULLY_CONSUMED_GENERIC_CONNECTOR"]
  specific = total["FULLY_CONSUMED_SPECIFIC_CONNECTOR"]
  completed = total["CONTRIBUTION_COMPLETES_DERIVATION"]
  partial = total["PARTIALLY_CONSUMED"]
  missing = total["NOT_CONSUMED"]

  print("=" * 110)
  print("CROSS-GROUP SUMMARY")
  print("=" * 110)
  print(f"CONSUMPTION_COUNTS={dict(total)}")
  print(f"FULLY_CONSUMED_GENERIC_CONNECTOR_TOTAL={generic}")
  print(f"FULLY_CONSUMED_SPECIFIC_CONNECTOR_TOTAL={specific}")
  print(f"CONTRIBUTION_COMPLETES_DERIVATION_TOTAL={completed}")
  print(f"PARTIALLY_CONSUMED_TOTAL={partial}")
  print(f"NOT_CONSUMED_TOTAL={missing}")
  print(
    "VISIBLE_LOCAL_DERIVATION_RECOUNT="
    + str(sum(total.values()))
  )

  if partial or missing:
    decision = "REPAIR_RENDERING_CONSUMPTION_BEFORE_REASON_PROSE"
  elif generic:
    decision = "GENERIC_CONNECTOR_IS_PRIMARY_RC4_7B_REPAIR_TARGET"
  elif completed:
    decision = "REVIEW_CONTRIBUTION_INSERTION_PROSE"
  else:
    decision = "NO_GENERIC_RENDERING_CONSUMPTION_GAP_FOUND"

  print(f"AUDIT_DECISION={decision}")


if __name__ == "__main__":
  main()
