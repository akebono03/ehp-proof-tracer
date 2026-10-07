# Phase 159 repair3c — changed code

## 変更対象

- `toda_group_proof_narrative_contribution_ordering.py`
  - `_anchored_chain_step_ids()`
  - `_necessity_for_chain()`
- `toda_group_proof_generic_narrative_renderer.py`
  - `toda_rules` import
  - `_render_generic_narrative_statement_prose()`
- `tests/test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py`
  - 新規テストファイル

`build_toda_group_proof_narrative_arguments()`、Reference 系、public renderer 本体は変更しない。

## `toda_group_proof_narrative_contribution_ordering.py`

### `_anchored_chain_step_ids()`

```python
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
```

### `_necessity_for_chain()`

```python
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
```

## `toda_group_proof_generic_narrative_renderer.py`

### 変更後の `toda_rules` import

```python
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda45IsomorphismStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaNuFamilyDefinitionStatement,
  TodaPi32Eta2DefinitionStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)
```

### `_render_generic_narrative_statement_prose()`

既存関数本体を維持し、`TodaProp42ExactnessStatement` 分岐の後、
generic map-property 分岐の前に次の2分岐を追加する。

```python
  if isinstance(
    statement,
    TodaDeltaImageFreeCyclicStatement,
  ):
    map_name = _generic_group_map_name(
      statement.map
    )

    if map_name is None:
      return None

    return (
      r"$\operatorname{Im}"
      + map_name
      + " = "
      + render_toda_raw_group_structure_latex(
        statement.image_group
      )
      + "$."
    )

  if isinstance(
    statement,
    TodaSuspensionKernelFreeCyclicStatement,
  ):
    map_name = _generic_group_map_name(
      statement.map
    )

    if map_name is None:
      return None

    return (
      r"$\ker "
      + map_name
      + " = "
      + render_toda_raw_group_structure_latex(
        statement.kernel_group
      )
      + "$."
    )

```

## 新規テスト

`payload/tests/test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py`
に全文を収録。
