from dataclasses import dataclass

from audit_phase144_6_r5_20 import (
  ParityStatus,
  build_parity_audit,
  parity_requirements,
)
from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from audit_phase144_6_r5_32 import (
  _ordered_active_argument_rows,
  _visible_non_exact_steps,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_body_renderer import (
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)


MISSING6_KEYS = (
  "hopf_nu_prime",
  "pi5_3_group",
  "hopf_nu_eta6",
  "pi7_5_group",
  "hopf_pi7_surjective",
  "delta_zero",
)


@dataclass(frozen=True)
class SurvivalRecord:
  key: str
  ordered_position: int
  argument_index: int
  argument_role: str
  visible: bool
  block_kept: bool
  step_render: str | None
  step_render_in_body: bool
  body_has_requirement: bool
  final_has_requirement: bool


def _requirement_by_key():
  return {
    requirement.key: requirement
    for requirement in parity_requirements()
  }


def _all_needles(text, needles):
  return all(needle in text for needle in needles)


def _requirement_present(text, requirement):
  return any(
    _all_needles(text, alternative)
    for alternative in requirement.generic_alternatives
  )


def _argument_body(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  argument_index,
  argument,
  excluded_non_exact_block_ids,
):
  relevant_groups = extract_toda_group_proof_narrative_argument_relevant_groups(
    presentation,
    blocks,
    argument,
  )
  evidence = extract_toda_group_proof_narrative_argument_method_evidence(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    argument_index,
  )
  components = build_toda_group_proof_narrative_exactness_method_components(
    evidence
  )
  primary_component = select_toda_group_proof_narrative_primary_exactness_component(
    relevant_groups,
    components,
  )
  local = extract_toda_group_proof_narrative_argument_local_body_blocks(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    argument_index,
  )

  # This audit intentionally isolates the survival of currently visible
  # non-exact steps. The exact production connector/relocation path is not
  # reimplemented here; Phase 32 visibility is used as the source of truth.
  visible = _visible_non_exact_steps(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    argument_index,
    argument,
  )
  visible_ids = {id(step) for block, step in visible}
  context_hidden = frozenset(
    id(step)
    for block in local
    for step in block.steps
    if (
      block.role.value != "exactness"
      and id(step) not in visible_ids
    )
  )

  body = render_toda_group_proof_narrative_argument_body_markdown(
    presentation,
    blocks,
    local,
    primary_component,
    excluded_non_exact_block_ids=frozenset(excluded_non_exact_block_ids),
    excluded_exactness_contribution_keys=frozenset(),
    context_hidden_step_ids=context_hidden,
  )
  return body, local, visible


def build_survival_records():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_sidecar,
    proof_chains,
  ) = _context(3, 3)
  dedicated, generic, parity_results = build_parity_audit()
  final_by_key = {
    result.requirement.key: result.status is ParityStatus.PRESENT
    for result in parity_results
  }
  targets = _canonical_fact_targets()
  requirements = _requirement_by_key()
  matching_ids = {
    key: {
      id(step)
      for block in blocks
      for step in block.steps
      if _step_contains_target(step, targets[key])
    }
    for key in MISSING6_KEYS
  }

  records = []
  seen_non_exact_block_ids = set()

  for position, argument_index, argument in _ordered_active_argument_rows(arguments):
    body, local, visible = _argument_body(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
      argument,
      seen_non_exact_block_ids,
    )
    visible_by_key = {
      key: tuple(
        (block, step)
        for block, step in visible
        if id(step) in matching_ids[key]
      )
      for key in MISSING6_KEYS
    }

    for key in MISSING6_KEYS:
      matches = visible_by_key[key]
      block_kept = any(
        id(block) not in seen_non_exact_block_ids
        for block, step in matches
      )
      step = matches[0][1] if matches else None
      step_render = None if step is None else _render_generic_narrative_step(step)
      records.append(
        SurvivalRecord(
          key=key,
          ordered_position=position,
          argument_index=argument_index,
          argument_role=argument.role.value,
          visible=bool(matches),
          block_kept=block_kept,
          step_render=step_render,
          step_render_in_body=(
            False if step_render is None else step_render in body
          ),
          body_has_requirement=_requirement_present(
            body,
            requirements[key],
          ),
          final_has_requirement=final_by_key[key],
        )
      )

    for block in local:
      if block.role.value != "exactness":
        seen_non_exact_block_ids.add(id(block))

  return tuple(records)


def print_audit():
  records = build_survival_records()

  print("=" * 78)
  print("Phase 144-6-R5-33 visible step -> rendered Markdown survival audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 missing-6 survival by ordered Argument")
  print("-" * 78)
  for row in records:
    print(
      f"{row.key}: ordered_position={row.ordered_position} "
      f"argument={row.argument_index} role={row.argument_role} "
      f"visible={row.visible} block_kept={row.block_kept} "
      f"step_render_in_body={row.step_render_in_body} "
      f"body_has_requirement={row.body_has_requirement} "
      f"final_has_requirement={row.final_has_requirement}"
    )
    if row.visible:
      print(f"  step_render={row.step_render}")

  print("\\nB. First loss stage per missing fact")
  print("-" * 78)
  for key in MISSING6_KEYS:
    rows = tuple(row for row in records if row.key == key)
    visible = any(row.visible for row in rows)
    kept = any(row.visible and row.block_kept for row in rows)
    rendered = any(
      row.visible and row.block_kept and row.step_render_in_body
      for row in rows
    )
    body_requirement = any(row.body_has_requirement for row in rows)
    final_requirement = any(row.final_has_requirement for row in rows)

    if not visible:
      stage = "before_visibility"
    elif not kept:
      stage = "block_dedup"
    elif not rendered:
      stage = "body_render"
    elif not body_requirement:
      stage = "requirement_representation"
    elif not final_requirement:
      stage = "multi_argument_or_final_normalization"
    else:
      stage = "survives"

    print(
      f"{key}: first_loss={stage} "
      f"visible={visible} kept={kept} rendered={rendered} "
      f"body_requirement={body_requirement} final_requirement={final_requirement}"
    )

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "This audit traces existing facts through current visibility, current "
    "block-level dedup, generic single-step rendering, isolated Argument body "
    "rendering, and the frozen Phase-20 final generic parity result."
  )
  print(
    "It does not change production selection, rendering, deduplication, "
    "ProofChain, membership, or public routing."
  )


if __name__ == "__main__":
  print_audit()
