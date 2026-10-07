# Phase 159 repair3c fix2 — changed code

## 変更対象

- `toda_group_proof_narrative_contribution_ordering.py`
  - 新規 `_provider_keys_by_step_id()`
  - `_build_visibility_occurrences()`
- 新規テスト
  - `tests/test_phase159_pi4_3_repair3c_fix2_provider_key_precompute.py`

import の変更はありません。

## 新規関数

追加位置:
`_provider_keys_for_step()` の直後、`_children_by_step_id()` の直前。

```python
def _provider_keys_by_step_id(
  presentation: TodaGroupProofPresentation,
  local_body: tuple[TodaGroupProofNarrativeBlock, ...],
  proof_chain: TodaGroupProofNarrativeProofChain,
  conclusion_step: ProofStep,
) -> dict[int, tuple[tuple[str, int], ...]]:
  keys_by_step_id = defaultdict(
    list
  )

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

    provider_key = _provider_key(
      provider
    )

    for step_id in chain_ids:
      keys_by_step_id[
        step_id
      ].append(
        provider_key
      )

  return {
    step_id: tuple(
      provider_keys
    )
    for step_id, provider_keys
    in keys_by_step_id.items()
  }
```

## `_build_visibility_occurrences()` の変更箇所

`step_by_id` 構築直後に以下を追加:

```python
    provider_keys_by_step_id = (
      _provider_keys_by_step_id(
        presentation,
        local_body,
        proof_chains[
          argument_index
        ],
        conclusion_step,
      )
    )
```

Occurrence 構築時は以下に置換:

```python
          provider_keys=provider_keys_by_step_id.get(
            step_id,
            (),
          ),
```

## 新規テスト全文

```python
import inspect

import toda_group_proof_narrative_contribution_ordering as module


def test_phase159_repair3c_fix2_provider_keys_are_precomputed_once_per_argument():
  source = inspect.getsource(
    module._build_visibility_occurrences
  )

  assert (
    "_provider_keys_by_step_id("
    in source
  )
  assert (
    "provider_keys=provider_keys_by_step_id.get("
    in source
  )
  assert (
    "provider_keys=_provider_keys_for_step("
    not in source
  )


def test_phase159_repair3c_fix2_precompute_uses_one_chain_build_per_provider():
  source = inspect.getsource(
    module._provider_keys_by_step_id
  )

  assert (
    "for provider in proof_chain.providers:"
    in source
  )
  assert (
    "_anchored_chain_step_ids("
    in source
  )
  assert (
    "_necessity_for_chain("
    not in source
  )


def test_phase159_repair3c_fix2_legacy_provider_key_contract_is_unchanged():
  source = inspect.getsource(
    module._provider_keys_for_step
  )

  assert (
    "if step_id in chain_ids:"
    in source
  )
  assert (
    "_anchored_chain_step_ids("
    in source
  )
  assert (
    "_necessity_for_chain("
    not in source
  )
```

## 境界

`_provider_keys_for_step()` は既存 API と inspection test のため維持する。
production visibility path では使用せず、argument ごとの precompute を用いる。
