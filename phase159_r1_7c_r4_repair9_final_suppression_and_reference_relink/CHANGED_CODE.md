# 変更コード

## 変更対象

- `toda_group_proof_narrative_contribution_renderer.py`
- 関数:
  `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

import 変更はありません。

今回は既存 helper の実装を変更しません。
同関数内の call order に次の2つを追加します。

### R9-A 追加位置

`order_toda_group_proof_narrative_injective_image_order_reason()` の直後、
`build_toda_group_proof_narrative_generic_used_step_ids()` の直前。

```python
  rendered = (
    suppress_toda_group_proof_narrative_reflexive_equalities(
      presentation,
      rendered,
    )
  )
```

これは最後の dependency insertion 後の final suppression です。

### R9-C 追加位置

`filter_toda_group_proof_narrative_reference_entries_by_step_usage()` を含む
Reference selection の `if/else` が終わった直後、
最後の `filter_toda_group_proof_narrative_reference_entries_by_body_usage()`
の直前。

```python
  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )
```

これは最終 Reference 集合に対する post-selection relink です。

## テストファイル全文

`test_phase159_r1_7c_r4_repair9.py` を参照してください。

## 注意

ローカル repository は Phase 159 repair8 後で GitHub main より進んでいるため、
package は関数全文を上書きせず、上記2つの既存 call sequence を厳密に検証してから
最小置換します。

anchor が一致しない場合は勝手に書き換えず停止します。
