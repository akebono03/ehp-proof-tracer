# Phase 159 pi3_2 post-reference locality re-apply repair16

## 変更対象

1. `toda_group_proof_narrative_contribution_renderer.py`
   - `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()` を変更。

2. `tests/test_phase159_pi3_2_post_reference_locality_reapply.py`
   - 新規追加。

## import

import の変更はありません。

## audit15 で確認したこと

definition locality の全判定条件は成立していた。

- definition step: 1
- math spans: 2
- isomorphism premise: 1
- definition paragraph match: 1
- `H` isomorphism premise match: 1
- `pi_3^3 = Z{iota_3}` premise match: 1

したがって reason renderer の definition logic は変更しない。

## 原因

repair14 の locality ordering は、
まだ Reference/body filtering と reference restoration が残っている位置で実行されていた。

その後の処理が `[R1]より, pi_3^3 = Z{iota_3}.` を再配置するため、
最終 public narrative では definition locality が失われる。

## 修正

全ての Reference/body filtering と reference pruning が終了した後、
`reference_section` を生成する直前に次を1回追加する。

```python
  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )
```

この位置より後では本文 paragraph の順序を変更する処理はない。

## 変更後の該当部分

```python
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    prune_toda_group_proof_narrative_root_zero_direct_premise_references(
      presentation,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
```

## 関数全文

apply script 実行時に、変更後の
`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`
全体を次のファイルへ出力する。

`phase159_pi3_2_post_reference_locality_reapply_repair16/patched_render_function_after_apply.py.txt`

これによりユーザーの現在のローカル状態を含む、実際に適用された関数全文を確認できる。

## テスト関数全文

`payload/tests/test_phase159_pi3_2_post_reference_locality_reapply.py`
に全文を収録。

## 実行する pytest

```powershell
python -m pytest `
  ".\tests\test_phase159_pi3_2_post_reference_locality_reapply.py" `
  ".\tests\test_phase159_pi3_2_final_locality_reapply.py" `
  ".\tests\test_phase159_pi3_2_proofstep_premise_locality.py" `
  ".\tests\test_phase159_pi3_2_map_property_order.py" `
  ".\tests\test_phase159_pi3_2_visible_dependency_topological_order.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  -q
```

## 完了条件

- `pi_2^1=0 -> H injective` が隣接
- `Delta=0 -> H surjective` が隣接
- `H injective`, `H surjective` の後に `H isomorphism`
- `H isomorphism -> pi_3^3=Z{iota_3} -> eta_2 definition` が連続
- eta2 definition の後に final result
- QED が最後
- focused pytest 全 PASS

## 次 Phase との境界

- reason renderer は変更しない
- proof graph は変更しない
- semantic sidecar は変更しない
- fixed literature statement は変更しない
- Argument ordering は変更しない
- full suite は Phase 159 最後にのみ実行する
