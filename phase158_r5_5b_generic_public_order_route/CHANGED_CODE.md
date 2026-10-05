# Phase 158-R5-5b changed code

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - 新規関数 `_phase158_r5_5b_has_ordered_root_argument()`
    - 追加位置: `_is_phase150_rc4_generic_route_target()` の直前
  - 変更関数 `_phase134_24_render_pi15_8_narrative()`
  - 変更関数 `_is_phase150_rc4_generic_route_target()`

import の変更はありません。

## 新規関数

```python
def _phase158_r5_5b_has_ordered_root_argument(
  presentation: TodaGroupProofPresentation,
) -> bool:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if presentation.max_depth < 2:
    return False

  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return any(
    (
      argument.supporting_blocks
      and presentation.root_step
      in argument.conclusion_block.steps
    )
    for argument in arguments
  )
```

## 変更関数 `_is_phase150_rc4_generic_route_target`

```python
def _is_phase150_rc4_generic_route_target(
  presentation: TodaGroupProofPresentation,
) -> bool:
  if presentation.max_depth < 2:
    return False

  if _is_phase134_9_pi8_5_presentation(
    presentation
  ):
    return False

  if _phase158_r5_5b_has_ordered_root_argument(
    presentation
  ):
    return True

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  return (
    (
      target.group_dimension == 10
      and target.sphere_dimension == 4
    )
    or (
      target.group_dimension == 12
      and target.sphere_dimension == 5
    )
    or (
      target.group_dimension == 16
      and target.sphere_dimension == 9
    )
  )
```

`_phase134_24_render_pi15_8_narrative()` は関数全体を置換し、
structured root Argument が存在する場合に早期 `None` を返して generic route に譲る。
全文は `apply_phase158_r5_5b.py` の `PI15_RENDERER` に収録。

## Tests

新規テストの import とテスト関数全文は
`tests/test_phase158_r5_5b_public_generic_order_route.py`
として apply script 内に全文収録。

## Phase boundary

- proof graph は変更しない
- semantic dependency は変更しない
- block ordering algorithm は変更しない
- pi_8^5 dedicated route は変更しない
- repository-wide pytest は実行しない
