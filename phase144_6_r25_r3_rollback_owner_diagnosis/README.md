# Phase 144-6 R25-R3

R25-R2 の rollback 処理で生じた、関数間の空行1行だけを復元する runner 修正版です。

R25-R2 の実行結果から、残っている差分は次の1点だけと確認されています。

- `_toda_group_proof_narrative_argument_frontier_hidden_step_ids` と
  `render_toda_group_proof_narrative_multi_argument_markdown` の間の空行1行

R25-R3 はその空行だけを復元し、`main.py` と
`toda_group_proof_narrative_argument_multi_renderer.py` の双方が
Git HEAD と完全一致することを `git diff --exit-code` で確認します。

一致後に focused tests と、R25 から変更していない owner diagnosis を実行します。

production logic の変更はありません。
新しい regression repair もありません。
全体 pytest は実行しません。
