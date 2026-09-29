from dataclasses import dataclass
from enum import Enum

from audit_phase144_6_r5_22 import (
  _canonical_targets,
  _contains_equal,
)
from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
)
from toda_group_proof_narrative_proof_chain_renderer import (
  render_toda_group_proof_narrative_from_proof_chains_markdown,
)
from test_phase65_equation57_injectivity import (
  build_phase65_3_data,
)


FACT_KEYS = (
  "hopf_nu_prime",
  "pi5_3_group",
  "nu_eta6_membership",
  "hopf_nu_eta6",
  "pi7_5_group",
  "hopf_pi7_surjective",
  "delta_zero",
)


class VisibilityPath(Enum):
  SUPPORTING_PROVIDER_FRONTIER_HIDDEN = (
    "supporting_provider_frontier_hidden"
  )
  LOCAL_BODY_FRONTIER_HIDDEN = "local_body_frontier_hidden"
  SUPPORTING_PROVIDER_VISIBLE = "supporting_provider_visible"
  LOCAL_BODY_VISIBLE = "local_body_visible"
  EMBEDDED_PARENT_SUPPORTING_PROVIDER_FRONTIER_HIDDEN = (
    "embedded_parent_supporting_provider_frontier_hidden"
  )
  EMBEDDED_PARENT_LOCAL_BODY_FRONTIER_HIDDEN = (
    "embedded_parent_local_body_frontier_hidden"
  )
  EMBEDDED_PARENT_VISIBLE = "embedded_parent_visible"
  NOT_IN_LOCAL_BODY = "not_in_local_body"


@dataclass(frozen=True)
class VisibilityTrace:
  key: str
  canonical_type: str
  presentation_step_count: int
  block_roles: tuple[str, ...]
  supporting_provider_argument_indices: tuple[int, ...]
  child_provider_argument_indices: tuple[int, ...]
  local_body_argument_indices: tuple[int, ...]
  frontier_hidden_argument_indices: tuple[int, ...]
  visible_argument_indices: tuple[int, ...]
  embedded_parent_key: str | None
  path: VisibilityPath


def _canonical_fact_targets():
  phase65 = build_phase65_3_data()
  phase22 = _canonical_targets()

  pi5_3_group = next(
    premise.conclusion
    for premise in phase65["prop53_step"].premises
    if (
      hasattr(premise.conclusion, "lhs")
      and getattr(premise.conclusion.lhs, "group_dimension", None) == 5
      and getattr(premise.conclusion.lhs, "sphere_dimension", None) == 3
    )
  )

  return {
    "hopf_nu_prime": phase22["hopf_nu_prime"],
    "pi5_3_group": pi5_3_group,
    "nu_eta6_membership": phase22["nu_eta6_membership"],
    "hopf_nu_eta6": phase22["hopf_nu_eta6"],
    "pi7_5_group": phase22["pi7_5_group"],
    "hopf_pi7_surjective": phase65["expected_hopf_surjective"],
    "delta_zero": phase65["expected_delta_zero"],
  }


def _step_contains_target(step, target):
  return (
    step.conclusion == target
    or _contains_equal(step.conclusion, target)
  )


def _provider_blocks(chain, arguments):
  for provider in chain.providers:
    if (
      provider.kind
      is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
    ):
      yield "supporting", provider.supporting_block
      continue

    child = arguments[provider.child_argument_index]
    yield "child", child.conclusion_block


def build_visibility_path_traces():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)

  targets = _canonical_fact_targets()
  local_bodies = tuple(
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
    for argument_index in range(len(arguments))
  )
  hidden_ids = tuple(
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_bodies[argument_index],
      semantic_sidecar,
      arguments[argument_index],
    )
    for argument_index in range(len(arguments))
  )

  final_text = render_toda_group_proof_narrative_from_proof_chains_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )
  if not final_text:
    raise AssertionError("generic Narrative unexpectedly empty")

  traces = []

  for key in FACT_KEYS:
    target = targets[key]
    embedded_parent_key = (
      "hopf_nu_eta6"
      if key == "nu_eta6_membership"
      else None
    )

    matching_steps = tuple(
      dict.fromkeys(
        step
        for block in blocks
        for step in block.steps
        if _step_contains_target(step, target)
      )
    )
    matching_ids = {id(step) for step in matching_steps}

    block_roles = tuple(
      dict.fromkeys(
        block.role.value
        for block in blocks
        if any(id(step) in matching_ids for step in block.steps)
      )
    )

    supporting_provider_indices = []
    child_provider_indices = []
    for chain in proof_chains:
      for provider_kind, provider_block in _provider_blocks(chain, arguments):
        if any(
          id(step) in matching_ids
          for step in provider_block.steps
        ):
          if provider_kind == "supporting":
            supporting_provider_indices.append(chain.argument_index)
          else:
            child_provider_indices.append(chain.argument_index)

    local_body_indices = tuple(
      argument_index
      for argument_index, local_body in enumerate(local_bodies)
      if any(
        id(step) in matching_ids
        for block in local_body
        for step in block.steps
      )
    )
    frontier_hidden_indices = tuple(
      argument_index
      for argument_index in local_body_indices
      if any(
        step_id in hidden_ids[argument_index]
        for step_id in matching_ids
      )
    )
    visible_indices = tuple(
      argument_index
      for argument_index in local_body_indices
      if any(
        step_id not in hidden_ids[argument_index]
        for step_id in matching_ids
      )
    )

    supporting_provider_indices = tuple(
      dict.fromkeys(supporting_provider_indices)
    )
    child_provider_indices = tuple(
      dict.fromkeys(child_provider_indices)
    )

    if embedded_parent_key is not None:
      if supporting_provider_indices and frontier_hidden_indices:
        path = (
          VisibilityPath
          .EMBEDDED_PARENT_SUPPORTING_PROVIDER_FRONTIER_HIDDEN
        )
      elif frontier_hidden_indices:
        path = (
          VisibilityPath
          .EMBEDDED_PARENT_LOCAL_BODY_FRONTIER_HIDDEN
        )
      elif visible_indices:
        path = VisibilityPath.EMBEDDED_PARENT_VISIBLE
      else:
        path = VisibilityPath.NOT_IN_LOCAL_BODY
    elif supporting_provider_indices and frontier_hidden_indices:
      path = VisibilityPath.SUPPORTING_PROVIDER_FRONTIER_HIDDEN
    elif frontier_hidden_indices:
      path = VisibilityPath.LOCAL_BODY_FRONTIER_HIDDEN
    elif supporting_provider_indices and visible_indices:
      path = VisibilityPath.SUPPORTING_PROVIDER_VISIBLE
    elif visible_indices:
      path = VisibilityPath.LOCAL_BODY_VISIBLE
    else:
      path = VisibilityPath.NOT_IN_LOCAL_BODY

    traces.append(
      VisibilityTrace(
        key=key,
        canonical_type=type(target).__name__,
        presentation_step_count=len(matching_steps),
        block_roles=block_roles,
        supporting_provider_argument_indices=supporting_provider_indices,
        child_provider_argument_indices=child_provider_indices,
        local_body_argument_indices=local_body_indices,
        frontier_hidden_argument_indices=frontier_hidden_indices,
        visible_argument_indices=visible_indices,
        embedded_parent_key=embedded_parent_key,
        path=path,
      )
    )

  return tuple(traces)


def print_audit():
  traces = build_visibility_path_traces()

  print("=" * 78)
  print("Phase 144-6-R5-23 missing 7 facts generic visibility-path audit")
  print("production changes: none")
  print("=" * 78)

  for trace in traces:
    print(f"\\n{trace.key}")
    print("-" * 78)
    print(f"canonical_type={trace.canonical_type}")
    print(f"presentation_step_count={trace.presentation_step_count}")
    print(
      "block_roles="
      + (",".join(trace.block_roles) if trace.block_roles else "-")
    )
    print(
      "supporting_provider_arguments="
      + (
        ",".join(map(str, trace.supporting_provider_argument_indices))
        if trace.supporting_provider_argument_indices
        else "-"
      )
    )
    print(
      "child_provider_arguments="
      + (
        ",".join(map(str, trace.child_provider_argument_indices))
        if trace.child_provider_argument_indices
        else "-"
      )
    )
    print(
      "local_body_arguments="
      + (
        ",".join(map(str, trace.local_body_argument_indices))
        if trace.local_body_argument_indices
        else "-"
      )
    )
    print(
      "frontier_hidden_arguments="
      + (
        ",".join(map(str, trace.frontier_hidden_argument_indices))
        if trace.frontier_hidden_argument_indices
        else "-"
      )
    )
    print(
      "visible_arguments="
      + (
        ",".join(map(str, trace.visible_argument_indices))
        if trace.visible_argument_indices
        else "-"
      )
    )
    print(
      "embedded_parent_key="
      + (trace.embedded_parent_key or "-")
    )
    print(f"path={trace.path.value}")

  print("\\nVisibility-path summary")
  print("-" * 78)
  for path in VisibilityPath:
    keys = tuple(
      trace.key
      for trace in traces
      if trace.path is path
    )
    print(f"{path.value}: {len(keys)}")
    for key in keys:
      print(f"  - {key}")

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "This audit does not change frontier policy, ProofChain provider "
    "selection, local-body selection, embedded-expression expansion, "
    "or rendering."
  )
  print(
    "The next implementation should modify only the generic layer shared "
    "by facts that converge on the same visibility path."
  )


if __name__ == "__main__":
  print_audit()
