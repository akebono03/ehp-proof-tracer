from collections import Counter, defaultdict, deque
from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TESTS_DIR = REPO_ROOT / "tests"

for path in (
  REPO_ROOT,
  TESTS_DIR,
):
  if str(path) not in sys.path:
    sys.path.insert(
      0,
      str(path),
    )


from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
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
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_contribution_ordering import (
  _ContributionOccurrence,
  _effective_hidden_step_ids,
  _group_key,
  _is_rendering_fallback,
  _normalized,
  _owner,
  _parents_by_premise,
  _premises_by_parent,
  _provider_anchor_step_ids,
  _provider_key,
  _reachable,
  _reverse_distances,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChain,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


PI4_REQUIRED_TYPES = (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


def _legacy_anchored_chain_step_ids(
  presentation,
  local_body,
  proof_chain,
  conclusion_step,
):
  local_ids = {
    id(step)
    for block in local_body
    for step in block.steps
  }
  anchors = (
    _provider_anchor_step_ids(
      proof_chain
    )
    & local_ids
  )
  distances = _reverse_distances(
    presentation,
    conclusion_step,
  )
  parents = _parents_by_premise(
    presentation
  )
  chain_ids = {
    id(
      conclusion_step
    )
  }
  queue = deque(
    step
    for block in local_body
    for step in block.steps
    if id(step) in anchors
  )
  visited = set(
    anchors
  )

  while queue:
    step = queue.popleft()
    step_id = id(
      step
    )

    if step_id not in distances:
      continue

    chain_ids.add(
      step_id
    )

    for parent in parents.get(
      step_id,
      (),
    ):
      parent_id = id(
        parent
      )

      if parent_id not in local_ids:
        continue
      if parent_id not in distances:
        continue
      if (
        distances[
          parent_id
        ]
        >= distances[
          step_id
        ]
      ):
        continue

      chain_ids.add(
        parent_id
      )

      if parent_id in visited:
        continue

      visited.add(
        parent_id
      )
      queue.append(
        parent
      )

  return (
    frozenset(
      chain_ids
    ),
    frozenset(
      anchors
    ),
    distances,
  )


def _legacy_can_reach(
  start_id,
  conclusion_id,
  parents,
  allowed_ids,
  removed_id=None,
):
  if start_id == removed_id:
    return False
  if start_id == conclusion_id:
    return True

  queue = deque(
    [
      start_id,
    ]
  )
  visited = {
    start_id,
  }

  while queue:
    current = queue.popleft()

    for parent in parents.get(
      current,
      (),
    ):
      parent_id = id(
        parent
      )

      if parent_id == removed_id:
        continue
      if parent_id not in allowed_ids:
        continue
      if parent_id == conclusion_id:
        return True
      if parent_id in visited:
        continue

      visited.add(
        parent_id
      )
      queue.append(
        parent_id
      )

  return False


def _legacy_necessity_for_chain(
  presentation,
  local_body,
  proof_chain,
  conclusion_step,
):
  (
    chain_ids,
    anchors,
    distances,
  ) = _legacy_anchored_chain_step_ids(
    presentation,
    local_body,
    proof_chain,
    conclusion_step,
  )
  parents = _parents_by_premise(
    presentation
  )
  conclusion_id = id(
    conclusion_step
  )
  reachable_anchors = tuple(
    anchor_id
    for anchor_id in anchors
    if _legacy_can_reach(
      anchor_id,
      conclusion_id,
      parents,
      chain_ids,
    )
  )
  necessity = {}

  for step_id in chain_ids:
    necessity[
      step_id
    ] = tuple(
      anchor_id
      for anchor_id in reachable_anchors
      if (
        step_id != anchor_id
        and not _legacy_can_reach(
          anchor_id,
          conclusion_id,
          parents,
          chain_ids,
          removed_id=step_id,
        )
      )
    )

  return (
    chain_ids,
    anchors,
    distances,
    necessity,
  )


def _legacy_provider_keys_for_step(
  presentation,
  local_body,
  proof_chain,
  conclusion_step,
  step_id,
):
  keys = []

  for provider in proof_chain.providers:
    if provider.supporting_block is None:
      continue

    provider_chain = (
      TodaGroupProofNarrativeProofChain(
        argument_index=proof_chain.argument_index,
        argument=proof_chain.argument,
        providers=(
          provider,
        ),
      )
    )

    (
      chain_ids,
      _anchors,
      _distances,
    ) = _legacy_anchored_chain_step_ids(
      presentation,
      local_body,
      provider_chain,
      conclusion_step,
    )

    if step_id in chain_ids:
      keys.append(
        _provider_key(
          provider
        )
      )

  return tuple(
    keys
  )


def _legacy_visibility_occurrences(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  proof_chains,
):
  markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  normalized_markdown = _normalized(
    markdown
  )
  rows = []

  for argument_index, argument in enumerate(
    arguments
  ):
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    if conclusion_step is None:
      continue

    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    hidden_ids = (
      _effective_hidden_step_ids(
        presentation,
        blocks,
        local_body,
        semantic_sidecar,
        argument,
      )
    )
    (
      chain_ids,
      anchors,
      distances,
      necessity,
    ) = _legacy_necessity_for_chain(
      presentation,
      local_body,
      proof_chains[
        argument_index
      ],
      conclusion_step,
    )

    step_by_id = {
      id(step): step
      for block in local_body
      for step in block.steps
    }

    for step_id in (
      chain_ids
      & hidden_ids
    ):
      if not necessity.get(
        step_id,
        (),
      ):
        continue

      step = step_by_id.get(
        step_id
      )

      if step is None:
        continue

      rendered = (
        _render_generic_narrative_step(
          step
        )
      )

      if (
        _normalized(
          rendered
        )
        in normalized_markdown
      ):
        continue

      if _is_rendering_fallback(
        step,
        rendered,
      ):
        continue

      rows.append(
        _ContributionOccurrence(
          argument_index=argument_index,
          argument=argument,
          proof_step=step,
          provider_anchor=(
            step_id
            in anchors
          ),
          distance_to_conclusion=(
            distances.get(
              step_id
            )
          ),
          provider_keys=(
            _legacy_provider_keys_for_step(
              presentation,
              local_body,
              proof_chains[
                argument_index
              ],
              conclusion_step,
              step_id,
            )
          ),
        )
      )

  return tuple(
    rows
  )


def _selected_owner_occurrences(
  presentation,
  arguments,
  occurrences,
):
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
  children = defaultdict(
    set
  )

  for edge in presentation.edges:
    children[
      id(
        edge.premise_step
      )
    ].add(
      id(
        edge.parent_step
      )
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

  selected = []

  for owner in owners:
    step_id = id(
      owner.proof_step
    )
    occurrence_peers = (
      occurrence_step_ids_by_argument[
        owner.argument_index
      ]
    )
    has_downstream_occurrence = any(
      (
        peer_id
        != step_id
        and _reachable(
          step_id,
          peer_id,
          children,
        )
      )
      for peer_id
      in occurrence_peers
    )

    if (
      owner.provider_anchor
      or has_downstream_occurrence
    ):
      selected.append(
        owner
      )

  return tuple(
    selected
  )


def _current_selected_keys(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  proof_chains,
):
  ordered = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )

  return {
    (
      row.owner_argument_index,
      id(
        row.proof_step
      ),
    ): row
    for rows in ordered
    for row in rows
  }


def _legacy_selected_keys(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  proof_chains,
):
  occurrences = (
    _legacy_visibility_occurrences(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )
  selected = (
    _selected_owner_occurrences(
      presentation,
      arguments,
      occurrences,
    )
  )

  return {
    (
      row.argument_index,
      id(
        row.proof_step
      ),
    ): row
    for row in selected
  }


def _print_counter(
  title,
  counter,
  limit=20,
):
  print(
    title
  )

  for key, count in counter.most_common(
    limit
  ):
    print(
      f"  {count:5d}  {key}"
    )


def _pi4_fact_state(
  presentation,
  blocks,
  semantic_sidecar,
  arguments,
  proof_chains,
):
  current = _current_selected_keys(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )
  legacy = _legacy_selected_keys(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )
  markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  normalized_markdown = _normalized(
    markdown
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
      for step in block.steps:
        if not isinstance(
          step.conclusion,
          PI4_REQUIRED_TYPES,
        ):
          continue

        key = (
          argument_index,
          id(
            step
          ),
        )
        rendered = (
          _render_generic_narrative_step(
            step
          )
        )
        print(
          "argument="
          f"{argument_index} "
          "type="
          f"{type(step.conclusion).__name__} "
          "in_legacy_selected="
          f"{key in legacy} "
          "in_current_selected="
          f"{key in current} "
          "already_public="
          f"{_normalized(rendered) in normalized_markdown} "
          "render="
          f"{rendered}"
        )


def main():
  print("=" * 78)
  print("Phase 159 - repair3c fix4 audit")
  print("Legacy selection delta audit")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()

  grand_legacy = 0
  grand_current = 0
  grand_added = Counter()
  grand_removed = Counter()
  grand_added_roles = Counter()

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(
      n,
      k,
    )

    legacy = _legacy_selected_keys(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
    current = _current_selected_keys(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )

    legacy_keys = set(
      legacy
    )
    current_keys = set(
      current
    )
    added = (
      current_keys
      - legacy_keys
    )
    removed = (
      legacy_keys
      - current_keys
    )

    grand_legacy += len(
      legacy_keys
    )
    grand_current += len(
      current_keys
    )

    added_types = Counter(
      type(
        current[
          key
        ].proof_step.conclusion
      ).__name__
      for key in added
    )
    removed_types = Counter(
      type(
        legacy[
          key
        ].proof_step.conclusion
      ).__name__
      for key in removed
    )
    added_roles = Counter(
      (
        current[
          key
        ].owner_argument_role.value,
        current[
          key
        ].placement.value,
        current[
          key
        ].provider_anchor,
      )
      for key in added
    )

    grand_added.update(
      added_types
    )
    grand_removed.update(
      removed_types
    )
    grand_added_roles.update(
      added_roles
    )

    print(
      f"TARGET pi_{n+k}^{n}: "
      f"legacy={len(legacy_keys)} "
      f"current={len(current_keys)} "
      f"added={len(added)} "
      f"removed={len(removed)}"
    )
    _print_counter(
      "  added statement types:",
      added_types,
      limit=12,
    )
    _print_counter(
      "  removed statement types:",
      removed_types,
      limit=12,
    )
    _print_counter(
      "  added role/placement/provider_anchor:",
      added_roles,
      limit=12,
    )

  print()
  print("=" * 78)
  print("GRAND TOTAL")
  print("=" * 78)
  print(
    f"legacy_total={grand_legacy}"
  )
  print(
    f"current_total={grand_current}"
  )
  print(
    f"net_delta={grand_current - grand_legacy}"
  )
  _print_counter(
    "added statement types:",
    grand_added,
    limit=30,
  )
  _print_counter(
    "removed statement types:",
    grand_removed,
    limit=30,
  )
  _print_counter(
    "added role/placement/provider_anchor:",
    grand_added_roles,
    limit=30,
  )

  print()
  print("=" * 78)
  print("PI_4^3 FOUR-FACT STATE")
  print("=" * 78)

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    _aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(
    3,
    1,
  )

  _pi4_fact_state(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )

  print()
  print("=" * 78)
  print("repair3c fix4 legacy selection delta audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()
