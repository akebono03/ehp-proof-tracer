# Phase 161-R3 repair3 changed code

## 変更ファイル

- `toda_group_proof_narrative_contribution_renderer.py`
- `tests/test_phase161_pi4_2_restored_reference_relink.py`

## 変更関数

`toda_group_proof_narrative_contribution_renderer.py`

- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

import 変更なし。

## 追加処理

`restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(...)`
直後に次を追加する。

```python
    rendered = (
      link_toda_group_proof_narrative_unmarked_reference_consumers(
        presentation,
        rendered,
        reference_entries,
      )
    )
```

final body-usage filter は削除しない。

## 全文出力

apply 後に次へ変更後関数全文を出力する。

`output/render_toda_group_proof_narrative_multi_argument_with_contributions_markdown.py.txt`

新規 test 全文は次へ出力する。

`output/test_phase161_pi4_2_restored_reference_relink.py.txt`

## Phase 境界

今回修正しない:

- Phase157 repair12 の既知2 failures
- Proposition 2.2 / Equation (5.7) attribution
- pi_6^3
- pi_5^3
- stable transport
- documentation

全体 pytest は実行しない。
