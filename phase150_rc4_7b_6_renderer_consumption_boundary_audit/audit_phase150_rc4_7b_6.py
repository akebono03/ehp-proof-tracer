from collections import Counter

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_body_renderer import (
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_exposure import (
  classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
)
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)


CASES = (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _transition_by_conclusion_id(
  presentation,
  blocks,
  arguments,
):
  return {
    id(transition.target_block): transition
    for transition in extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    )
  }


def _block_contains_rendered_step(
  body: str,
  block,
) -> tuple[bool, ...]:
  return tuple(
    _render_generic_narrative_step(step) in body
    for step in block.steps
  )


def _classify_source_boundary(
  source_block,
  local_body_blocks,
  context_hidden_step_ids,
  seen_non_exact_block_ids,
  seen_non_exact_step_ids,
  direct_premises,
  direct_support_steps,
  body,
):
  local_ids = {
    id(block)
    for block in local_body_blocks
  }
  if id(source_block) not in local_ids:
    return "LOCAL_BODY_MISSING"

  visible_steps = tuple(
    step
    for step in source_block.steps
    if id(step) not in context_hidden_step_ids
  )
  if not visible_steps:
    return "CONTEXT_HIDDEN"

  if (
    source_block.role
    is not TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    and id(source_block) in seen_non_exact_block_ids
  ):
    return "SEEN_BLOCK_SUPPRESSED"

  remaining_steps = tuple(
    step
    for step in visible_steps
    if id(step) not in seen_non_exact_step_ids
  )
  if not remaining_steps:
    return "SEEN_STEP_SUPPRESSED"

  rendered_flags = tuple(
    _render_generic_narrative_step(step) in body
    for step in remaining_steps
  )
  if any(rendered_flags):
    return "BODY_RENDERED"

  direct_ids = {
    id(step)
    for step in direct_premises + direct_support_steps
  }
  if not any(
    id(step) in direct_ids
    for step in remaining_steps
  ):
    return "DIRECT_PREMISE_NOT_SELECTED"

  return "BODY_RENDERER_DROPPED"


def audit_case(label, n, k):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(n, k)

  transition_by_id = _transition_by_conclusion_id(
    presentation,
    blocks,
    arguments,
  )
  ordered_arguments = order_toda_group_proof_narrative_arguments(
    arguments
  )
  discourse_roles = classify_toda_group_proof_narrative_argument_discourse_roles(
    arguments
  )
  source_index_by_identity = {
    id(argument): index
    for index, argument in enumerate(arguments)
  }

  seen_non_exact_block_ids = set()
  seen_non_exact_step_ids = set()
  counts = Counter()
  derivation_count = 0

  print("=" * 110)
  print(label)
  print("=" * 110)
  print(f"blocks={len(blocks)}")
  print(f"arguments={len(arguments)}")

  for ordered_position, argument in enumerate(ordered_arguments):
    discourse_role = discourse_roles[ordered_position]
    if discourse_role is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED:
      continue

    argument_index = source_index_by_identity[id(argument)]
    transition = transition_by_id.get(id(argument.conclusion_block))
    if (
      transition is None
      or transition.role
      is not TodaGroupProofNarrativeTransitionRole.DERIVATION
    ):
      continue

    local_body_blocks = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )

    evidence = extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
    local_ids = {id(block) for block in local_body_blocks}
    evidence_ids = {id(block) for block in evidence}
    local_body_blocks = tuple(
      block
      for block in blocks
      if id(block) in local_ids or id(block) in evidence_ids
    )

    context_hidden_step_ids = frozenset(
      id(step)
      for block in local_body_blocks
      for step in block.steps
      if isinstance(step.conclusion, TodaEtaFamilyDefinitionStatement)
    )
    context_hidden_step_ids = (
      context_hidden_step_ids
      | _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_body_blocks,
        sidecar,
        argument,
      )
    )

    conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    direct_premises = (
      ()
      if conclusion_step is None
      else extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
        argument,
        arguments,
      )
    )
    direct_support_steps = tuple(
      support_step
      for premise_step in direct_premises
      for support_step in premise_step.premises
      if all(
        support_step is not existing_step
        for existing_step in direct_premises
      )
    )

    components = build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
    relevant_groups = extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
    exposure_by_id = {}
    for component in components:
      exposure = classify_toda_group_proof_narrative_exactness_component_exposure(
        relevant_groups,
        components,
        component,
      )
      for evidence_block in component.evidence_blocks:
        exposure_by_id[id(evidence_block)] = exposure

    primary_component = select_toda_group_proof_narrative_argument_primary_exactness_component(
      presentation,
      blocks,
      sidecar,
      arguments,
      argument_index,
    )
    connector = render_toda_group_proof_narrative_transition_connector(
      transition
    )

    body = render_toda_group_proof_narrative_argument_body_markdown(
      presentation,
      blocks,
      local_body_blocks,
      primary_component,
      exactness_exposure_by_block_id=exposure_by_id,
      excluded_non_exact_block_ids=frozenset(seen_non_exact_block_ids),
      excluded_non_exact_step_ids=frozenset(seen_non_exact_step_ids),
      connector_before_block_id=id(argument.conclusion_block),
      connector_text=connector,
      conclusion_step=conclusion_step,
      direct_derivation_premises=direct_premises,
      direct_derivation_support_steps=direct_support_steps,
      context_hidden_step_ids=context_hidden_step_ids,
      preserve_provenance_block_ids=frozenset(
        id(block)
        for block in transition.source_blocks
      ),
    )

    print()
    print(f"DERIVATION {label} D{derivation_count:02d}")
    print(f"  argument_index=A{argument_index:02d}")
    print(f"  argument_role={argument.role.value}")
    print(f"  discourse_role={discourse_role.value}")
    print(f"  connector={connector!r}")
    print(f"  local_body_count={len(local_body_blocks)}")
    print(f"  direct_premise_count={len(direct_premises)}")
    print(f"  direct_support_count={len(direct_support_steps)}")
    print(f"  context_hidden_step_count={len(context_hidden_step_ids)}")
    print(f"  seen_block_count_before={len(seen_non_exact_block_ids)}")
    print(f"  seen_step_count_before={len(seen_non_exact_step_ids)}")

    for source_number, source_block in enumerate(transition.source_blocks):
      boundary = _classify_source_boundary(
        source_block,
        local_body_blocks,
        context_hidden_step_ids,
        seen_non_exact_block_ids,
        seen_non_exact_step_ids,
        direct_premises,
        direct_support_steps,
        body,
      )
      counts[boundary] += 1
      print(
        f"  SOURCE S{source_number:02d} "
        f"role={source_block.role.value} "
        f"boundary={boundary} "
        f"in_local={id(source_block) in {id(b) for b in local_body_blocks}} "
        f"rendered_steps={_block_contains_rendered_step(body, source_block)}"
      )

    conclusion_rendered = (
      conclusion_step is not None
      and _render_generic_narrative_step(conclusion_step) in body
    )
    connector_rendered = connector in body
    print(f"  conclusion_rendered={conclusion_rendered}")
    print(f"  connector_rendered={connector_rendered}")

    derivation_count += 1

    for block in local_body_blocks:
      if block.role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS:
        continue
      visible_step_ids = {
        id(step)
        for step in block.steps
        if id(step) not in context_hidden_step_ids
      }
      seen_non_exact_step_ids.update(visible_step_ids)
      if len(visible_step_ids) == len(block.steps):
        seen_non_exact_block_ids.add(id(block))

  print()
  print(f"CASE_DERIVATION_COUNT={derivation_count}")
  print(f"CASE_BOUNDARY_COUNTS={dict(counts)}")
  print()
  return counts


def main():
  total = Counter()

  print("Phase 150 RC4-7B-6 Renderer Consumption Boundary Audit")
  print("Production changes: none")
  print("Scope: existing DERIVATION rendering boundaries only.")
  print()

  for label, n, k in CASES:
    total.update(audit_case(label, n, k))

  print("=" * 110)
  print("CROSS-GROUP SUMMARY")
  print("=" * 110)
  print(f"BOUNDARY_COUNTS={dict(total)}")

  actionable = sum(
    total[key]
    for key in (
      "LOCAL_BODY_MISSING",
      "CONTEXT_HIDDEN",
      "SEEN_BLOCK_SUPPRESSED",
      "SEEN_STEP_SUPPRESSED",
      "DIRECT_PREMISE_NOT_SELECTED",
      "BODY_RENDERER_DROPPED",
    )
  )
  print(f"ACTIONABLE_BOUNDARY_TOTAL={actionable}")

  dominant = (
    total.most_common(1)[0][0]
    if total
    else "NONE"
  )
  print(f"DOMINANT_BOUNDARY={dominant}")
  print("AUDIT_DECISION=IDENTIFY_MINIMAL_RENDERER_BOUNDARY_REPAIR")


if __name__ == "__main__":
  main()
