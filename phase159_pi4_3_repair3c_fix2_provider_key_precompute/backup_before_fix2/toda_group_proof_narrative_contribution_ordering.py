from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum

from proof import ProofStep
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChain,
  TodaGroupProofNarrativeProofChainProvider,
  TodaGroupProofNarrativeProofChainProviderKind,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)


class TodaGroupProofNarrativeContributionRole(Enum):
  EXPLICIT_PREREQUISITE = "explicit_prerequisite"
  BRIDGE = "bridge"


class TodaGroupProofNarrativeContributionPlacement(Enum):
  AT_PROVIDER_ANCHOR = "at_provider_anchor"
  BEFORE_DEPENDENT_CONTRIBUTION = "before_dependent_contribution"
  BEFORE_ARGUMENT_CONCLUSION = "before_argument_conclusion"


@dataclass(frozen=True)
class TodaGroupProofNarrativeOrderedContribution:
  proof_step: ProofStep
  owner_argument_index: int
  owner_argument_role: TodaGroupProofNarrativeArgumentRole
  contribution_role: TodaGroupProofNarrativeContributionRole
  placement: TodaGroupProofNarrativeContributionPlacement
  provider_anchor: bool
  distance_to_conclusion: int | None
  provider_keys: tuple[tuple[str, int], ...]

  def __post_init__(self) -> None:
    if not isinstance(self.proof_step, ProofStep):
      raise TypeError("proof_step must be a ProofStep")
    if (
      not isinstance(self.owner_argument_index, int)
      or isinstance(self.owner_argument_index, bool)
      or self.owner_argument_index < 0
    ):
      raise TypeError("owner_argument_index must be a non-negative integer")
    if not isinstance(
      self.owner_argument_role,
      TodaGroupProofNarrativeArgumentRole,
    ):
      raise TypeError(
        "owner_argument_role must be a "
        "TodaGroupProofNarrativeArgumentRole"
      )
    if not isinstance(
      self.contribution_role,
      TodaGroupProofNarrativeContributionRole,
    ):
      raise TypeError(
        "contribution_role must be a "
        "TodaGroupProofNarrativeContributionRole"
      )
    if not isinstance(
      self.placement,
      TodaGroupProofNarrativeContributionPlacement,
    ):
      raise TypeError(
        "placement must be a "
        "TodaGroupProofNarrativeContributionPlacement"
      )
    if not isinstance(self.provider_anchor, bool):
      raise TypeError("provider_anchor must be bool")
    if (
      self.distance_to_conclusion is not None
      and (
        not isinstance(self.distance_to_conclusion, int)
        or isinstance(self.distance_to_conclusion, bool)
        or self.distance_to_conclusion < 0
      )
    ):
      raise TypeError(
        "distance_to_conclusion must be a non-negative integer or None"
      )
    if not isinstance(self.provider_keys, tuple):
      raise TypeError("provider_keys must be a tuple")


@dataclass(frozen=True)
class _ContributionOccurrence:
  argument_index: int
  argument: TodaGroupProofNarrativeArgument
  proof_step: ProofStep
  provider_anchor: bool
  distance_to_conclusion: int | None
  provider_keys: tuple[tuple[str, int], ...]


def _validate_inputs(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[TodaGroupProofNarrativeBlock, ...],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[TodaGroupProofNarrativeArgument, ...],
  proof_chains: tuple[TodaGroupProofNarrativeProofChain, ...],
) -> None:
  if not isinstance(presentation, TodaGroupProofPresentation):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )
  if not isinstance(blocks, tuple):
    raise TypeError("blocks must be a tuple")
  if not isinstance(
    semantic_sidecar,
    TodaGroupProofNarrativeSemanticSidecar,
  ):
    raise TypeError(
      "semantic_sidecar must be a "
      "TodaGroupProofNarrativeSemanticSidecar"
    )
  if semantic_sidecar.presentation is not presentation:
    raise ValueError(
      "semantic_sidecar must belong to presentation"
    )
  if not isinstance(arguments, tuple):
    raise TypeError("arguments must be a tuple")
  if not isinstance(proof_chains, tuple):
    raise TypeError("proof_chains must be a tuple")
  if len(proof_chains) != len(arguments):
    raise ValueError(
      "proof_chains must contain one chain per argument"
    )
  for index, argument in enumerate(arguments):
    if not isinstance(argument, TodaGroupProofNarrativeArgument):
      raise TypeError(
        "arguments must contain only "
        "TodaGroupProofNarrativeArgument objects"
      )
    chain = proof_chains[index]
    if not isinstance(chain, TodaGroupProofNarrativeProofChain):
      raise TypeError(
        "proof_chains must contain only "
        "TodaGroupProofNarrativeProofChain objects"
      )
    if chain.argument_index != index or chain.argument is not argument:
      raise ValueError(
        "proof_chains must align with arguments by index and identity"
      )


def _premises_by_parent(
  presentation: TodaGroupProofPresentation,
) -> dict[int, list[ProofStep]]:
  result = defaultdict(list)
  for edge in presentation.edges:
    result[id(edge.parent_step)].append(edge.premise_step)
  return result


def _parents_by_premise(
  presentation: TodaGroupProofPresentation,
) -> dict[int, list[ProofStep]]:
  result = defaultdict(list)
  for edge in presentation.edges:
    result[id(edge.premise_step)].append(edge.parent_step)
  return result


def _reverse_distances(
  presentation: TodaGroupProofPresentation,
  conclusion_step: ProofStep,
) -> dict[int, int]:
  premises = _premises_by_parent(presentation)
  distances = {id(conclusion_step): 0}
  queue = deque([conclusion_step])
  while queue:
    parent = queue.popleft()
    distance = distances[id(parent)] + 1
    for premise in premises.get(id(parent), ()):
      premise_id = id(premise)
      if premise_id in distances:
        continue
      distances[premise_id] = distance
      queue.append(premise)
  return distances


def _provider_anchor_step_ids(
  proof_chain: TodaGroupProofNarrativeProofChain,
) -> frozenset[int]:
  return frozenset(
    id(step)
    for provider in proof_chain.providers
    if (
      provider.kind
      is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
    )
    for step in provider.supporting_block.steps
  )


def _anchored_chain_step_ids(
  presentation: TodaGroupProofPresentation,
  local_body: tuple[TodaGroupProofNarrativeBlock, ...],
  proof_chain: TodaGroupProofNarrativeProofChain,
  conclusion_step: ProofStep,
) -> tuple[frozenset[int], frozenset[int], dict[int, int]]:
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
  premises = _premises_by_parent(
    presentation
  )
  chain_ids = {
    id(
      conclusion_step
    )
  }

  downstream_queue = deque(
    step
    for block in local_body
    for step in block.steps
    if id(step) in anchors
  )
  downstream_visited = set(
    anchors
  )

  while downstream_queue:
    step = downstream_queue.popleft()
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

      if parent_id in downstream_visited:
        continue

      downstream_visited.add(
        parent_id
      )
      downstream_queue.append(
        parent
      )

  upstream_queue = deque(
    step
    for block in local_body
    for step in block.steps
    if id(step) in anchors
  )
  upstream_visited = set(
    anchors
  )

  while upstream_queue:
    step = upstream_queue.popleft()
    step_id = id(
      step
    )

    if step_id not in distances:
      continue

    for premise in premises.get(
      step_id,
      (),
    ):
      premise_id = id(
        premise
      )

      if premise_id not in local_ids:
        continue
      if premise_id not in distances:
        continue
      if (
        distances[
          premise_id
        ]
        <= distances[
          step_id
        ]
      ):
        continue

      chain_ids.add(
        premise_id
      )

      if premise_id in upstream_visited:
        continue

      upstream_visited.add(
        premise_id
      )
      upstream_queue.append(
        premise
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


def _can_reach_conclusion(
  start_id: int,
  conclusion_id: int,
  parents: dict[int, list[ProofStep]],
  allowed_ids: frozenset[int],
  removed_id: int | None = None,
) -> bool:
  if start_id == removed_id:
    return False
  if start_id == conclusion_id:
    return True
  queue = deque([start_id])
  visited = {start_id}
  while queue:
    current = queue.popleft()
    for parent in parents.get(current, ()):
      parent_id = id(parent)
      if parent_id == removed_id:
        continue
      if parent_id not in allowed_ids:
        continue
      if parent_id == conclusion_id:
        return True
      if parent_id in visited:
        continue
      visited.add(parent_id)
      queue.append(parent_id)
  return False


def _necessity_for_chain(
  presentation: TodaGroupProofPresentation,
  local_body: tuple[TodaGroupProofNarrativeBlock, ...],
  proof_chain: TodaGroupProofNarrativeProofChain,
  conclusion_step: ProofStep,
) -> tuple[
  frozenset[int],
  frozenset[int],
  dict[int, int],
  dict[int, tuple[int, ...]],
]:
  (
    chain_ids,
    anchors,
    distances,
  ) = _anchored_chain_step_ids(
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
    if _can_reach_conclusion(
      anchor_id,
      conclusion_id,
      parents,
      chain_ids,
    )
  )
  necessity = {}

  for step_id in chain_ids:
    required_by = []

    for anchor_id in reachable_anchors:
      if step_id == anchor_id:
        continue

      downstream_required = (
        not _can_reach_conclusion(
          anchor_id,
          conclusion_id,
          parents,
          chain_ids,
          removed_id=step_id,
        )
      )
      upstream_prerequisite = (
        _can_reach_conclusion(
          step_id,
          anchor_id,
          parents,
          chain_ids,
        )
      )

      if (
        downstream_required
        or upstream_prerequisite
      ):
        required_by.append(
          anchor_id
        )

    necessity[
      step_id
    ] = tuple(
      required_by
    )

  return (
    chain_ids,
    anchors,
    distances,
    necessity,
  )


def _effective_hidden_step_ids(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[TodaGroupProofNarrativeBlock, ...],
  local_body: tuple[TodaGroupProofNarrativeBlock, ...],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  argument: TodaGroupProofNarrativeArgument,
) -> frozenset[int]:
  hidden = set(
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      semantic_sidecar,
      argument,
    )
  )
  if (
    argument.role
    is not TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
  ):
    hidden.update(
      id(step)
      for block in local_body
      for step in block.steps
      if isinstance(
        step.conclusion,
        TodaEtaFamilyDefinitionStatement,
      )
    )
  return frozenset(hidden)


def _normalized(text: str) -> str:
  return "".join(text.split())


def _is_rendering_fallback(
  step: ProofStep,
  rendered: str,
) -> bool:
  rule = step.inference_rule
  if rule is not None and rendered == rule.name:
    return True
  return rendered == (
    "`" + type(step.conclusion).__name__ + "`"
  )


def _provider_key(
  provider: TodaGroupProofNarrativeProofChainProvider,
) -> tuple[str, int]:
  if provider.supporting_block is not None:
    return ("block", id(provider.supporting_block))
  return ("child_argument", provider.child_argument_index)


def _provider_keys_for_step(
  presentation: TodaGroupProofPresentation,
  local_body: tuple[TodaGroupProofNarrativeBlock, ...],
  proof_chain: TodaGroupProofNarrativeProofChain,
  conclusion_step: ProofStep,
  step_id: int,
) -> tuple[tuple[str, int], ...]:
  keys = []

  for provider in proof_chain.providers:
    if provider.supporting_block is None:
      continue

    provider_chain = TodaGroupProofNarrativeProofChain(
      argument_index=proof_chain.argument_index,
      argument=proof_chain.argument,
      providers=(
        provider,
      ),
    )

    (
      chain_ids,
      _anchors,
      _distances,
    ) = _anchored_chain_step_ids(
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


def _children_by_step_id(
  presentation: TodaGroupProofPresentation,
) -> dict[int, set[int]]:
  children = defaultdict(set)
  for edge in presentation.edges:
    children[id(edge.premise_step)].add(id(edge.parent_step))
  return children


def _reachable(
  source: int,
  target: int,
  children: dict[int, set[int]],
) -> bool:
  if source == target:
    return False
  stack = list(children.get(source, ()))
  seen = set()
  while stack:
    current = stack.pop()
    if current == target:
      return True
    if current in seen:
      continue
    seen.add(current)
    stack.extend(children.get(current, ()))
  return False


def _build_visibility_occurrences(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[TodaGroupProofNarrativeBlock, ...],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[TodaGroupProofNarrativeArgument, ...],
  proof_chains: tuple[TodaGroupProofNarrativeProofChain, ...],
  current_markdown: str | None = None,
) -> tuple[_ContributionOccurrence, ...]:
  if current_markdown is None:
    markdown = render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  else:
    if not isinstance(
      current_markdown,
      str,
    ):
      raise TypeError(
        "current_markdown must be a str or None"
      )
    markdown = current_markdown
  normalized_markdown = _normalized(markdown)
  rows = []

  for argument_index, argument in enumerate(arguments):
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
    hidden_ids = _effective_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      semantic_sidecar,
      argument,
    )
    chain_ids, anchors, distances, necessity = _necessity_for_chain(
      presentation,
      local_body,
      proof_chains[argument_index],
      conclusion_step,
    )
    step_by_id = {
      id(step): step
      for block in local_body
      for step in block.steps
    }

    for step_id in chain_ids & hidden_ids:
      if not necessity.get(step_id, ()):
        continue
      step = step_by_id.get(step_id)
      if step is None:
        continue
      rendered = _render_generic_narrative_step(step)
      if _normalized(rendered) in normalized_markdown:
        continue
      if _is_rendering_fallback(step, rendered):
        continue
      rows.append(
        _ContributionOccurrence(
          argument_index=argument_index,
          argument=argument,
          proof_step=step,
          provider_anchor=step_id in anchors,
          distance_to_conclusion=distances.get(step_id),
          provider_keys=_provider_keys_for_step(
            presentation,
            local_body,
            proof_chains[argument_index],
            conclusion_step,
            step_id,
          ),
        )
      )

  return tuple(rows)


def _group_key(
  occurrence: _ContributionOccurrence,
) -> tuple:
  rendered = _render_generic_narrative_step(
    occurrence.proof_step
  )
  return (
    type(
      occurrence.proof_step.conclusion
    ),
    _normalized(
      rendered
    ),
    occurrence.provider_keys,
  )

def _owner(
  occurrences: list[_ContributionOccurrence],
) -> _ContributionOccurrence:
  return sorted(
    occurrences,
    key=lambda row: (
      0 if row.provider_anchor else 1,
      (
        row.distance_to_conclusion
        if row.distance_to_conclusion is not None
        else 10**9
      ),
      row.argument_index,
    ),
  )[0]


def _stored_order_key(
  contribution: TodaGroupProofNarrativeOrderedContribution,
  argument: TodaGroupProofNarrativeArgument,
  local_body: tuple[TodaGroupProofNarrativeBlock, ...],
) -> tuple[int, int, int]:
  step_id = id(contribution.proof_step)
  supporting_block_rank = {
    id(block): index
    for index, block in enumerate(argument.supporting_blocks)
  }
  local_block_rank = {
    id(block): index
    for index, block in enumerate(local_body)
  }
  for block in local_body:
    for step_index, step in enumerate(block.steps):
      if id(step) != step_id:
        continue
      return (
        supporting_block_rank.get(id(block), 10**9),
        local_block_rank[id(block)],
        step_index,
      )
  return (10**9, 10**9, 10**9)


def _topological_order(
  contributions: tuple[
    TodaGroupProofNarrativeOrderedContribution,
    ...,
  ],
  presentation: TodaGroupProofPresentation,
  argument: TodaGroupProofNarrativeArgument,
  local_body: tuple[TodaGroupProofNarrativeBlock, ...],
) -> tuple[TodaGroupProofNarrativeOrderedContribution, ...]:
  children = _children_by_step_id(presentation)
  by_id = {
    id(contribution.proof_step): contribution
    for contribution in contributions
  }
  successors = {
    step_id: set()
    for step_id in by_id
  }
  indegree = {
    step_id: 0
    for step_id in by_id
  }

  for left_id in by_id:
    for right_id in by_id:
      if left_id == right_id:
        continue
      if _reachable(left_id, right_id, children):
        successors[left_id].add(right_id)

  for targets in successors.values():
    for target in targets:
      indegree[target] += 1

  remaining = set(by_id)
  ordered = []

  while remaining:
    ready = [
      step_id
      for step_id in remaining
      if indegree[step_id] == 0
    ]
    if not ready:
      raise ValueError(
        "explanatory contribution dependency graph contains a cycle"
      )
    ready.sort(
      key=lambda step_id: _stored_order_key(
        by_id[step_id],
        argument,
        local_body,
      )
    )
    chosen = ready[0]
    ordered.append(by_id[chosen])
    remaining.remove(chosen)
    for target in successors[chosen]:
      if target in remaining:
        indegree[target] -= 1

  return tuple(ordered)


def build_toda_group_proof_narrative_ordered_contributions(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[TodaGroupProofNarrativeBlock, ...],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[TodaGroupProofNarrativeArgument, ...],
  proof_chains: tuple[TodaGroupProofNarrativeProofChain, ...],
  current_markdown: str | None = None,
) -> tuple[
  tuple[
    TodaGroupProofNarrativeOrderedContribution,
    ...,
  ],
  ...,
]:
  _validate_inputs(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )

  occurrences = _build_visibility_occurrences(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
    current_markdown=current_markdown,
  )
  grouped = defaultdict(list)
  for occurrence in occurrences:
    grouped[_group_key(occurrence)].append(occurrence)

  owners = tuple(
    _owner(rows)
    for rows in grouped.values()
  )
  children = _children_by_step_id(presentation)
  occurrence_step_ids_by_argument = defaultdict(set)
  for occurrence in occurrences:
    occurrence_step_ids_by_argument[
      occurrence.argument_index
    ].add(
      id(occurrence.proof_step)
    )

  normalized_markdown = (
    _normalized(current_markdown)
    if current_markdown is not None
    else None
  )
  visible_step_ids_by_argument = defaultdict(set)

  if normalized_markdown is not None:
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

      for block in local_body:
        for proof_step in block.steps:
          rendered = _render_generic_narrative_step(
            proof_step
          )

          if not rendered:
            continue

          if (
            _normalized(rendered)
            in normalized_markdown
          ):
            visible_step_ids_by_argument[
              argument_index
            ].add(
              id(proof_step)
            )

  selected_owners = []
  for owner in owners:
    step_id = id(owner.proof_step)
    occurrence_peers = occurrence_step_ids_by_argument[
      owner.argument_index
    ]
    has_downstream_occurrence = any(
      peer_id != step_id
      and _reachable(step_id, peer_id, children)
      for peer_id in occurrence_peers
    )
    visible_peers = visible_step_ids_by_argument[
      owner.argument_index
    ]
    has_visible_downstream = any(
      peer_id != step_id
      and _reachable(step_id, peer_id, children)
      for peer_id in visible_peers
    )
    if (
      owner.provider_anchor
      or has_downstream_occurrence
      or has_visible_downstream
    ):
      selected_owners.append(owner)

  selected_step_ids_by_argument = defaultdict(set)
  for owner in selected_owners:
    selected_step_ids_by_argument[
      owner.argument_index
    ].add(
      id(owner.proof_step)
    )

  selected_by_argument = defaultdict(list)

  for owner in selected_owners:
    step_id = id(owner.proof_step)
    selected_peers = selected_step_ids_by_argument[
      owner.argument_index
    ]
    has_selected_successor = any(
      peer_id != step_id
      and _reachable(step_id, peer_id, children)
      for peer_id in selected_peers
    )

    if owner.provider_anchor:
      role = (
        TodaGroupProofNarrativeContributionRole
        .EXPLICIT_PREREQUISITE
      )
      placement = (
        TodaGroupProofNarrativeContributionPlacement
        .AT_PROVIDER_ANCHOR
      )
    else:
      role = TodaGroupProofNarrativeContributionRole.BRIDGE
      if has_selected_successor:
        placement = (
          TodaGroupProofNarrativeContributionPlacement
          .BEFORE_DEPENDENT_CONTRIBUTION
        )
      else:
        placement = (
          TodaGroupProofNarrativeContributionPlacement
          .BEFORE_ARGUMENT_CONCLUSION
        )

    selected_by_argument[owner.argument_index].append(
      TodaGroupProofNarrativeOrderedContribution(
        proof_step=owner.proof_step,
        owner_argument_index=owner.argument_index,
        owner_argument_role=owner.argument.role,
        contribution_role=role,
        placement=placement,
        provider_anchor=owner.provider_anchor,
        distance_to_conclusion=owner.distance_to_conclusion,
        provider_keys=owner.provider_keys,
      )
    )

  result = []

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
    ordered = _topological_order(
      tuple(selected_by_argument.get(argument_index, ())),
      presentation,
      argument,
      local_body,
    )
    result.append(ordered)

  return tuple(result)
