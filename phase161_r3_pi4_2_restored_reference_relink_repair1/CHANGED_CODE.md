# Phase 161-R3 changed code

## 変更対象

### Production

- `toda_group_proof_narrative_contribution_renderer.py`
  - `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

import の変更はありません。

変更内容は、`restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()` の直後、最終 `filter_toda_group_proof_narrative_reference_entries_by_body_usage()` の前に、既存 helper を再適用することだけです。

```python
    rendered = (
      link_toda_group_proof_narrative_unmarked_reference_consumers(
        presentation,
        rendered,
        reference_entries,
      )
    )
```

適用後、この package の

`output/render_toda_group_proof_narrative_multi_argument_with_contributions_markdown.py.txt`

に変更後の関数全体を省略なしで出力します。

### Test

新規追加位置:

`tests/test_phase161_pi4_2_restored_reference_relink.py`

必要な import とテスト関数全体は、適用後に

`output/test_phase161_pi4_2_restored_reference_relink.py.txt`

へ省略なしで出力します。

## 完了条件

- `(5.2)` が `[R1]` として public Reference に残る。
- Proposition 4.4 が `[R2]` として残る。
- proof body に `[R1]`, `[R2]` の linkage が存在する。
- `pi_4^2 = Z/2{eta_2^2}` と QED を維持する。
- 関連 focused regression が PASS する。

## 次 Phase との境界

今回変更しないもの:

- Toda (5.2) の数学的 statement
- literature-statement boundary catalog
- pi_4^2 production proof graph
- generator notation policy
- pi_5^3
- stable transport
- documentation

全体 pytest は Phase 161 の最後にのみ行う。
