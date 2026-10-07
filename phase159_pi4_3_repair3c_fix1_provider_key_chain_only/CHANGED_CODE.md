# Phase 159 repair3c fix1 — changed code

## 変更対象

- `toda_group_proof_narrative_contribution_ordering.py`
  - `_provider_keys_for_step()`
- 新規テスト
  - `tests/test_phase159_pi4_3_repair3c_fix1_provider_key_chain_only.py`

import の変更はありません。

## `_provider_keys_for_step()` 全文

```python
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
```

## 新規テスト全文

```python
import inspect

import toda_group_proof_narrative_contribution_ordering as module


def test_phase159_repair3c_fix1_provider_keys_use_chain_membership_without_necessity_recomputation():
  source = inspect.getsource(
    module._provider_keys_for_step
  )

  assert (
    "_anchored_chain_step_ids("
    in source
  )
  assert (
    "_necessity_for_chain("
    not in source
  )
  assert (
    "if step_id in chain_ids:"
    in source
  )
```

## 変更理由

`_provider_keys_for_step()` は provider ごとの chain membership だけを必要とするが、
旧実装では `_necessity_for_chain()` を呼び、その高コストな reachability 計算まで
毎回再実行していた。

repair3c performance audit では、pi_12^5 の visibility 構築中に

`_provider_keys_for_step() -> _necessity_for_chain() -> _can_reach_conclusion()`

で KeyboardInterrupt となった。

新実装は同じ `chain_ids` を `_anchored_chain_step_ids()` から直接取得するため、
provider-key semantics を変えずに不要な necessity 再計算だけを除去する。
