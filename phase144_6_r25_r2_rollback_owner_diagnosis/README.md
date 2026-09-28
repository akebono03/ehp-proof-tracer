# Phase 144-6 R25-R2

R25 の rollback runner の anchor 判定だけを修正した版です。

R25 初回実行では `main.py` の rollback は成功しましたが、
`toda_group_proof_narrative_argument_multi_renderer.py` の文字列 anchor が
GitHub HEAD の実際の関数形と一致せず停止しました。

R25-R2 では GitHub `develop` HEAD で確認した
`_toda_group_proof_narrative_argument_frontier_hidden_step_ids`
関数全体を pre-R24 の canonical state として復元します。

その後、`main.py` と multi renderer の両方について `git diff --exit-code`
で Git HEAD と一致することを確認してから focused tests と owner diagnosis を実行します。

新しい production repair は行いません。
全体 pytest は実行しません。
