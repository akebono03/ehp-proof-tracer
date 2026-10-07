from collections import defaultdict
from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_ordering import (
  _build_visibility_occurrences,
  _can_reach_conclusion,
  _children_by_step_id,
  _effective_hidden_step_ids,
  _group_key,
  _is_rendering_fallback,
  _necessity_for_chain,
  _normalized,
  _owner,
  _parents_by_premise,
  _reachable,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
  build_toda_group_proof_narrative_proof_chains,
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


INTERESTING_RULE_FRAGMENTS = (
  "pi_4^3 finite cyclic quotient calculation",
  "Proposition 5.1 pi_3^2 group relation",
  "pi_4^3 exactness Delta image equals E kernel",
  "pi_4^3 E-H exactness zero-right suspension surjectivity",
  "free cyclic generator Delta image",
  "Proposition 5.1 Delta iota_5",
  "(5.1) sphere connectivity zero",
)

INTERESTING_TYPES = {
  "Relation",
  "TodaSuspensionKernelFreeCyclicStatement",
  "TodaSuspensionSurjectiveStatement",
  "TodaDeltaImageFreeCyclicStatement",
  "TodaPrimaryGroupZeroStatement",
  "TodaDeltaImageUpToSignStatement",
  "TodaProp42ExactnessStatement",
}


def _presentation():
  report = build_standard_toda_report(
    n=3,
    k=1,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  return (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )


def _rule_name(step):
  rule = step.inference_rule
  if rule is None:
    return None
  return rule.name


def _render(step):
  try:
    return _render_generic_narrative_step(
      step
    )
  except Exception as exc:
    return (
      "<render-error "
      + type(exc).__name__
      + ": "
      + str(exc)
      + ">"
    )


def _interesting(step):
  type_name = type(
    step.conclusion
  ).__name__
  if type_name in INTERESTING_TYPES:
    return True

  rule_name = (
    _rule_name(
      step
    )
    or ""
  )
  return any(
    fragment in rule_name
    for fragment in INTERESTING_RULE_FRAGMENTS
  )


def _step_label(step):
  return (
    type(
      step.conclusion
    ).__name__
    + " | rule="
    + repr(
      _rule_name(
        step
      )
    )
    + " | "
    + _render(
      step
    )
  )


def _provider_summary(provider):
  if (
    provider.kind
    is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
  ):
    block = provider.supporting_block
    return (
      "SUPPORTING_BLOCK "
      + "role="
      + str(
        block.role
      )
      + " "
      + "step_count="
      + str(
        len(
          block.steps
        )
      )
    )

  return (
    "CHILD_ARGUMENT "
    + "index="
    + str(
      provider.child_argument_index
    )
  )


def _visible_local_step_ids(
  local_body,
  base_markdown,
):
  normalized_base = _normalized(
    base_markdown
  )
  visible = set()

  for block in local_body:
    for step in block.steps:
      rendered = _render(
        step
      )
      if (
        rendered
        and _normalized(
          rendered
        )
        in normalized_base
      ):
        visible.add(
          id(
            step
          )
        )

  return frozenset(
    visible
  )


def _print_provider_details(
  proof_chain,
):
  print("=== PROOF CHAIN PROVIDERS ===")
  print(
    "provider_count=",
    len(
      proof_chain.providers
    ),
  )

  for provider_index, provider in enumerate(
    proof_chain.providers
  ):
    print(
      f"provider {provider_index}: "
      + _provider_summary(
        provider
      )
    )

    if provider.supporting_block is None:
      continue

    for step_index, step in enumerate(
      provider.supporting_block.steps
    ):
      print(
        f"  step {step_index}: "
        + _step_label(
          step
        )
      )

  print()


def _print_local_blocks(
  local_body,
):
  print("=== ARGUMENT 0 LOCAL BODY BLOCKS ===")
  print(
    "local_block_count=",
    len(
      local_body
    ),
  )

  for block_index, block in enumerate(
    local_body
  ):
    print(
      f"block {block_index}: "
      f"role={block.role} "
      f"step_count={len(block.steps)}"
    )
    for step_index, step in enumerate(
      block.steps
    ):
      if not _interesting(
        step
      ):
        continue
      print(
        f"  interesting step {step_index}: "
        + _step_label(
          step
        )
      )

  print()


def _print_anchor_reachability(
  presentation,
  chain_ids,
  anchors,
  conclusion_step,
):
  print("=== ANCHOR REACHABILITY ===")
  print(
    "anchor_count=",
    len(
      anchors
    ),
  )

  parents = _parents_by_premise(
    presentation
  )
  conclusion_id = id(
    conclusion_step
  )

  reachable_anchors = []

  for anchor_id in sorted(
    anchors
  ):
    reachable = _can_reach_conclusion(
      anchor_id,
      conclusion_id,
      parents,
      chain_ids,
    )
    print(
      f"anchor_id={anchor_id} "
      f"can_reach_conclusion={reachable}"
    )
    if reachable:
      reachable_anchors.append(
        anchor_id
      )

  print(
    "reachable_anchor_count=",
    len(
      reachable_anchors
    ),
  )
  print()

  return tuple(
    reachable_anchors
  )


def _print_selection_matrix(
  local_body,
  hidden_ids,
  chain_ids,
  anchors,
  distances,
  necessity,
  visible_ids,
):
  print("=== CONTRIBUTION SELECTION MATRIX ===")
  print(
    "Columns: hidden chain anchor necessary visible fallback "
    "candidate distance | step"
  )

  rows = []

  for block in local_body:
    for step in block.steps:
      step_id = id(
        step
      )
      rendered = _render(
        step
      )
      fallback = _is_rendering_fallback(
        step,
        rendered,
      )
      hidden = step_id in hidden_ids
      in_chain = step_id in chain_ids
      anchor = step_id in anchors
      necessary_anchor_ids = necessity.get(
        step_id,
        (),
      )
      necessary = bool(
        necessary_anchor_ids
      )
      visible = step_id in visible_ids
      candidate = (
        hidden
        and in_chain
        and necessary
        and not visible
        and not fallback
      )
      distance = distances.get(
        step_id
      )

      if (
        _interesting(
          step
        )
        or hidden
        or in_chain
        or anchor
        or necessary
      ):
        rows.append(
          (
            step,
            hidden,
            in_chain,
            anchor,
            necessary,
            visible,
            fallback,
            candidate,
            distance,
            necessary_anchor_ids,
          )
        )

  for (
    step,
    hidden,
    in_chain,
    anchor,
    necessary,
    visible,
    fallback,
    candidate,
    distance,
    necessary_anchor_ids,
  ) in rows:
    print(
      f"{int(hidden)} "
      f"{int(in_chain)} "
      f"{int(anchor)} "
      f"{int(necessary)} "
      f"{int(visible)} "
      f"{int(fallback)} "
      f"{int(candidate)} "
      f"{str(distance):>8} | "
      + _step_label(
        step
      )
    )
    if necessary_anchor_ids:
      print(
        "  necessary_for_anchor_ids=",
        necessary_anchor_ids,
      )

  print()

  return tuple(
    rows
  )


def _print_occurrences_and_owner_selection(
  presentation,
  occurrences,
  arguments,
  base_markdown,
  blocks,
  semantic_sidecar,
):
  print("=== VISIBILITY OCCURRENCES ===")
  print(
    "occurrence_count=",
    len(
      occurrences
    ),
  )

  for index, occurrence in enumerate(
    occurrences
  ):
    print(
      f"occurrence {index}: "
      f"argument={occurrence.argument_index} "
      f"provider_anchor={occurrence.provider_anchor} "
      f"distance={occurrence.distance_to_conclusion} "
      f"provider_keys={occurrence.provider_keys}"
    )
    print(
      "  "
      + _step_label(
        occurrence.proof_step
      )
    )

  print()

  grouped = defaultdict(
    list
  )
  for occurrence in occurrences:
    grouped[
      _group_key(
        occurrence
      )
    ].append(
      occurrence
    )

  owners = tuple(
    _owner(
      rows
    )
    for rows in grouped.values()
  )

  children = _children_by_step_id(
    presentation
  )
  occurrence_step_ids_by_argument = defaultdict(
    set
  )

  for occurrence in occurrences:
    occurrence_step_ids_by_argument[
      occurrence.argument_index
    ].add(
      id(
        occurrence.proof_step
      )
    )

  normalized_base = _normalized(
    base_markdown
  )
  visible_step_ids_by_argument = defaultdict(
    set
  )

  for argument_index, argument in enumerate(
    arguments
  ):
    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    for block in local_body:
      for proof_step in block.steps:
        rendered = _render(
          proof_step
        )
        if (
          rendered
          and _normalized(
            rendered
          )
          in normalized_base
        ):
          visible_step_ids_by_argument[
            argument_index
          ].add(
            id(
              proof_step
            )
          )

  print("=== OWNER SELECTION ===")
  print(
    "owner_count=",
    len(
      owners
    ),
  )

  selected_owner_count = 0

  for owner_index, owner in enumerate(
    owners
  ):
    step_id = id(
      owner.proof_step
    )
    occurrence_peers = (
      occurrence_step_ids_by_argument[
        owner.argument_index
      ]
    )
    has_downstream_occurrence = any(
      peer_id != step_id
      and _reachable(
        step_id,
        peer_id,
        children,
      )
      for peer_id in occurrence_peers
    )
    visible_peers = (
      visible_step_ids_by_argument[
        owner.argument_index
      ]
    )
    has_visible_downstream = any(
      peer_id != step_id
      and _reachable(
        step_id,
        peer_id,
        children,
      )
      for peer_id in visible_peers
    )
    selected = (
      owner.provider_anchor
      or has_downstream_occurrence
      or has_visible_downstream
    )

    if selected:
      selected_owner_count += 1

    print(
      f"owner {owner_index}: "
      f"argument={owner.argument_index} "
      f"provider_anchor={owner.provider_anchor} "
      f"downstream_occurrence={has_downstream_occurrence} "
      f"visible_downstream={has_visible_downstream} "
      f"selected={selected}"
    )
    print(
      "  "
      + _step_label(
        owner.proof_step
      )
    )

  print(
    "selected_owner_count=",
    selected_owner_count,
  )
  print()

  return (
    len(
      owners
    ),
    selected_owner_count,
  )


def _diagnosis(
  anchors,
  reachable_anchors,
  rows,
  occurrence_count,
  owner_count,
  selected_owner_count,
  ordered_count,
):
  chain_hidden_rows = tuple(
    row
    for row in rows
    if row[1] and row[2]
  )
  necessary_rows = tuple(
    row
    for row in chain_hidden_rows
    if row[4]
  )
  not_visible_rows = tuple(
    row
    for row in necessary_rows
    if not row[5]
  )
  non_fallback_rows = tuple(
    row
    for row in not_visible_rows
    if not row[6]
  )

  if not anchors:
    return (
      "NO_PROVIDER_ANCHORS: proof chain has no supporting-block anchors."
    )

  if not reachable_anchors:
    return (
      "ANCHORS_CANNOT_REACH_CONCLUSION: provider anchors exist, "
      "but none can reach the argument conclusion inside chain_ids."
    )

  if not chain_hidden_rows:
    return (
      "NO_CHAIN_HIDDEN_INTERSECTION: no local step is both in chain_ids "
      "and hidden_ids."
    )

  if not necessary_rows:
    return (
      "NECESSITY_FILTER_REMOVES_ALL: chain/hidden steps exist, but "
      "necessity is empty for all of them."
    )

  if not not_visible_rows:
    return (
      "ALREADY_VISIBLE_FILTER_REMOVES_ALL: all necessary candidates are "
      "already present in base markdown."
    )

  if not non_fallback_rows:
    return (
      "FALLBACK_FILTER_REMOVES_ALL: all remaining candidates render only "
      "as rule/type fallbacks."
    )

  if occurrence_count == 0:
    return (
      "OCCURRENCE_BUILD_UNEXPECTED_ZERO: matrix predicts candidates, "
      "but _build_visibility_occurrences returned none."
    )

  if owner_count == 0:
    return (
      "OWNER_GROUPING_ZERO: occurrences exist, but grouping/owner "
      "selection produced no owners."
    )

  if selected_owner_count == 0:
    return (
      "OWNER_SELECTION_REMOVES_ALL: owners exist, but none is a provider "
      "anchor and none has a downstream occurrence/visible step."
    )

  if ordered_count == 0:
    return (
      "ORDERING_RESULT_ZERO: selected owners exist, but ordered "
      "contributions are empty."
    )

  return (
    "CONTRIBUTIONS_EXIST: contribution selection is not the zero point; "
    "inspect later insertion/suppression stages."
  )


def main():
  print("=" * 78)
  print("Phase 159 - pi_4^3 repair3a audit")
  print("Contribution selection internals only")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()

  presentation = _presentation()
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  print("=== CONTEXT ===")
  print(
    "presentation nodes=",
    len(
      presentation.nodes
    ),
  )
  print(
    "blocks=",
    len(
      blocks
    ),
  )
  print(
    "arguments=",
    len(
      arguments
    ),
  )
  print(
    "proof_chains=",
    len(
      proof_chains
    ),
  )
  print()

  if not arguments:
    raise RuntimeError(
      "pi_4^3 produced no narrative arguments"
    )

  argument_index = 0
  argument = arguments[
    argument_index
  ]
  proof_chain = proof_chains[
    argument_index
  ]
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  if conclusion_step is None:
    raise RuntimeError(
      "argument 0 has no conclusion step"
    )

  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
  )

  print("=== ARGUMENT 0 CONCLUSION ===")
  print(
    _step_label(
      conclusion_step
    )
  )
  print()

  _print_provider_details(
    proof_chain
  )
  _print_local_blocks(
    local_body
  )

  hidden_ids = _effective_hidden_step_ids(
    presentation,
    blocks,
    local_body,
    semantic_sidecar,
    argument,
  )
  (
    chain_ids,
    anchors,
    distances,
    necessity,
  ) = _necessity_for_chain(
    presentation,
    local_body,
    proof_chain,
    conclusion_step,
  )

  print("=== SET COUNTS ===")
  print(
    "hidden_ids=",
    len(
      hidden_ids
    ),
  )
  print(
    "chain_ids=",
    len(
      chain_ids
    ),
  )
  print(
    "anchors=",
    len(
      anchors
    ),
  )
  print(
    "chain_hidden_intersection=",
    len(
      chain_ids
      & hidden_ids
    ),
  )
  print(
    "necessity_nonempty=",
    sum(
      1
      for anchor_ids in necessity.values()
      if anchor_ids
    ),
  )
  print()

  reachable_anchors = _print_anchor_reachability(
    presentation,
    chain_ids,
    anchors,
    conclusion_step,
  )

  visible_ids = _visible_local_step_ids(
    local_body,
    base_markdown,
  )

  rows = _print_selection_matrix(
    local_body,
    hidden_ids,
    chain_ids,
    anchors,
    distances,
    necessity,
    visible_ids,
  )

  occurrences = _build_visibility_occurrences(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=base_markdown,
  )

  (
    owner_count,
    selected_owner_count,
  ) = _print_occurrences_and_owner_selection(
    presentation,
    occurrences,
    arguments,
    base_markdown,
    blocks,
    semantic_sidecar,
  )

  ordered = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )

  ordered_count = (
    len(
      ordered[0]
    )
    if ordered
    else 0
  )

  print("=== ORDERED CONTRIBUTIONS ===")
  print(
    "argument 0 contribution_count=",
    ordered_count,
  )

  if ordered:
    for index, contribution in enumerate(
      ordered[0]
    ):
      print(
        f"[{index}] "
        f"role={contribution.contribution_role} "
        f"placement={contribution.placement} "
        f"provider_anchor={contribution.provider_anchor}"
      )
      print(
        "  "
        + _step_label(
          contribution.proof_step
        )
      )

  print()
  print("=== DIAGNOSIS ===")
  print(
    _diagnosis(
      anchors,
      reachable_anchors,
      rows,
      len(
        occurrences
      ),
      owner_count,
      selected_owner_count,
      ordered_count,
    )
  )
  print()

  print("=" * 78)
  print("repair3a contribution selection audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()
