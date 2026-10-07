# Phase 161-R3 repair2 changed code

## Production

変更ファイル:

`toda_group_proof_narrative_contribution_renderer.py`

変更関数:

`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

import 変更なし。

追加する処理:

```python
    rendered = (
      link_toda_group_proof_narrative_unmarked_reference_consumers(
        presentation,
        rendered,
        reference_entries,
      )
    )
```

追加位置:

`restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(...)`
を含む statement の直後。

apply 後の関数全文は:

`output/render_toda_group_proof_narrative_multi_argument_with_contributions_markdown.py.txt`

へ出力する。

## Test

新規:

`tests/test_phase161_pi4_2_restored_reference_relink.py`

apply 後の test 全文は:

`output/test_phase161_pi4_2_restored_reference_relink.py.txt`

へ出力する。

## 完了条件

- `(5.2)` が public Reference に残る。
- Proposition 4.4 も残る。
- 本文にそれぞれの Reference marker がある。
- pi_4^2 の結論と QED を維持する。
- 関連 focused tests が PASS する。

全体 pytest は実行しない。
