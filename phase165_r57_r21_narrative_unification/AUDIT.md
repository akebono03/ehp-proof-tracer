# R57-R21 監査

GitHub の `toda_group_proof_generic_narrative_renderer.py`、`phase165_r52_partial_proof.py`、`phase165_r52_r3_web_adapter.py`、`toda_group_proof_narrative_renderer.py` を確認した。

従来の完成表示 `phase165_r56_presentation_adapter.py` は、旧 `build_complete_toda_group_result_proof_replay` から公開 Renderer を呼んでいた。一方、未完成表示は `render_toda_partial_proof_narrative_markdown` に入り、証明対象に `open_goals[0]` を選ぶ不具合があった。

今回の境界: 新しい数学的推論は追加しない。両入口を既存の共通関数に集約し、表示上の不整合を修正する。以前の長文 Narrative と同じ自然言語量の再現はこの Phase の完了条件としない。文献出典が欠ける GIVEN を架空の Reference として表示しない。

ユーザー環境での対象 pytest を実行してから完了判定する。全体 pytest は Phase 165 終了時のみ。
