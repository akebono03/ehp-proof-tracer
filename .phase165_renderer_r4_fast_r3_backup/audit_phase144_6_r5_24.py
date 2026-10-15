from dataclasses import dataclass
from enum import Enum

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
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
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
)
from toda_group_proof_narrative_proof_chain_renderer import (
  render_toda_group_proof_narrative_from_proof_chains_markdown,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)


class BodyLossStage(Enum):
  FRONTIER = "frontier"
  BODY_RENDERER = "body_renderer"
  MULTI_ARGUMENT_ASSEMBLY = "multi_argument_assembly"
  FINAL_PRESENT = "final_present"


@dataclass(frozen=True)
class GroupProtectionImpact:
  n: int
  k: int
  argument_count: int
  baseline_frontier_hidden_steps: int
  protected_supporting_provider_steps: int
  newly_released_steps: int
  newly_released_roles: tuple[str, ...]


@dataclass(frozen=True)
class VisibleFactBodyTrace:
  key: str
  local_body_arguments: tuple[int, ...]
  frontier_hidden_arguments: tuple[int, ...]
  baseline_body_arguments: tuple[int, ...]
  final_text_has_step: bool
  loss_stage: BodyLossStage


def _supporting_provider_step_ids(chain):
  return frozenset(
    id(step)
    for provider in chain.providers
    if (
      provider.kind
      is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
    )
    for step in provider.supporting_block.steps
  )


def build_group_protection_impacts():
  impacts = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)

    baseline_hidden_union = set()
    protected_union = set()
    released_union = set()
    released_roles = []

    for argument_index, argument in enumerate(arguments):
      local_body = (
        extract_toda_group_proof_narrative_argument_local_body_blocks(
          presentation,
          blocks,
          semantic_sidecar,
          arguments,
          argument_index,
        )
      )
      baseline_hidden = (
        _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
          presentation,
          blocks,
          local_body,
          semantic_sidecar,
          argument,
        )
      )
      provider_step_ids = _supporting_provider_step_ids(
        proof_chains[argument_index]
      )
      released = baseline_hidden & provider_step_ids

      baseline_hidden_union.update(baseline_hidden)
      protected_union.update(provider_step_ids)
      released_union.update(released)

      for block in local_body:
        if any(id(step) in released for step in block.steps):
          released_roles.append(block.role.value)

    impacts.append(
      GroupProtectionImpact(
        n=n,
        k=k,
        argument_count=len(arguments),
        baseline_frontier_hidden_steps=len(baseline_hidden_union),
        protected_supporting_provider_steps=len(protected_union),
        newly_released_steps=len(released_union),
        newly_released_roles=tuple(dict.fromkeys(released_roles)),
      )
    )

  return tuple(impacts)


def _primary_component(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  argument_index,
):
  argument = arguments[argument_index]
  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
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
  return select_toda_group_proof_narrative_primary_exactness_component(
    relevant_groups,
    components,
  )


def build_visible_fact_body_traces():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  targets = _canonical_fact_targets()
  final_text = render_toda_group_proof_narrative_from_proof_chains_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )

  traces = []

  for key in ("hopf_nu_prime", "hopf_nu_eta6"):
    target = targets[key]
    matching_steps = tuple(
      dict.fromkeys(
        step
        for block in blocks
        for step in block.steps
        if _step_contains_target(step, target)
      )
    )
    matching_ids = {id(step) for step in matching_steps}
    rendered_steps = tuple(
      dict.fromkeys(
        _render_generic_narrative_step(step)
        for step in matching_steps
      )
    )

    local_body_arguments = []
    hidden_arguments = []
    body_arguments = []

    for argument_index, argument in enumerate(arguments):
      local_body = (
        extract_toda_group_proof_narrative_argument_local_body_blocks(
          presentation,
          blocks,
          semantic_sidecar,
          arguments,
          argument_index,
        )
      )
      if not any(
        id(step) in matching_ids
        for block in local_body
        for step in block.steps
      ):
        continue

      local_body_arguments.append(argument_index)
      hidden = (
        _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
          presentation,
          blocks,
          local_body,
          semantic_sidecar,
          argument,
        )
      )
      if any(step_id in hidden for step_id in matching_ids):
        hidden_arguments.append(argument_index)

      body = render_toda_group_proof_narrative_argument_body_markdown(
        presentation,
        blocks,
        local_body,
        _primary_component(
          presentation,
          blocks,
          semantic_sidecar,
          arguments,
          argument_index,
        ),
        context_hidden_step_ids=hidden,
      )
      if any(rendered in body for rendered in rendered_steps):
        body_arguments.append(argument_index)

    final_has = any(rendered in final_text for rendered in rendered_steps)

    if hidden_arguments:
      stage = BodyLossStage.FRONTIER
    elif not body_arguments:
      stage = BodyLossStage.BODY_RENDERER
    elif not final_has:
      stage = BodyLossStage.MULTI_ARGUMENT_ASSEMBLY
    else:
      stage = BodyLossStage.FINAL_PRESENT

    traces.append(
      VisibleFactBodyTrace(
        key=key,
        local_body_arguments=tuple(local_body_arguments),
        frontier_hidden_arguments=tuple(hidden_arguments),
        baseline_body_arguments=tuple(body_arguments),
        final_text_has_step=final_has,
        loss_stage=stage,
      )
    )

  return tuple(traces)


def print_audit():
  impacts = build_group_protection_impacts()
  traces = build_visible_fact_body_traces()

  print("=" * 78)
  print("Phase 144-6-R5-24 generic visibility policy correction design audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. Hypothetical supporting-provider frontier protection")
  print("-" * 78)
  total_released = 0
  for impact in impacts:
    total_released += impact.newly_released_steps
    print(
      f"pi_{impact.n + impact.k}^{impact.n}: "
      f"arguments={impact.argument_count} "
      f"baseline_hidden={impact.baseline_frontier_hidden_steps} "
      f"provider_steps={impact.protected_supporting_provider_steps} "
      f"newly_released={impact.newly_released_steps} "
      f"roles={','.join(impact.newly_released_roles) or '-'}"
    )
  print(f"total_newly_released_across_groups={total_released}")

  print("\\nB. Already-visible Phase 23 facts through body renderer")
  print("-" * 78)
  for trace in traces:
    print(f"{trace.key}")
    print(
      "  local_body_arguments="
      + ",".join(map(str, trace.local_body_arguments))
    )
    print(
      "  frontier_hidden_arguments="
      + (
        ",".join(map(str, trace.frontier_hidden_arguments))
        if trace.frontier_hidden_arguments
        else "-"
      )
    )
    print(
      "  baseline_body_arguments="
      + (
        ",".join(map(str, trace.baseline_body_arguments))
        if trace.baseline_body_arguments
        else "-"
      )
    )
    print(f"  final_text_has_step={trace.final_text_has_step}")
    print(f"  loss_stage={trace.loss_stage.value}")

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "A production change is justified only if supporting-provider protection "
    "has a bounded cross-group effect and matches the direct ProofChain "
    "provider semantics."
  )
  print(
    "The two already-visible Hopf facts must be fixed at their observed "
    "post-frontier loss stage; they must not be addressed by widening "
    "frontier visibility."
  )
  print(
    "Embedded nu-prime eta_6 membership remains outside this production "
    "change and requires a separate generic expression-to-membership rule."
  )


if __name__ == "__main__":
  print_audit()
