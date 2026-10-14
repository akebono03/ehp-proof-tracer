# Phase 165-R57-R4 変更コード

## 変更ファイル・関数

`/toda_group_proof_narrative_renderer.py`

- **削除**: 最初の `render_toda_group_proof_narrative_markdown()` （GitHub 現行コードの 11279 行付近）。この定義は後続定義で上書きされ、エイリアス捕捉されていない。
- **条件付き削除**: `_phase159_render_pi_n_plus_1_n_stable_transport_narrative()` （11102 行付近）。他の本番ルートからの利用が確認された場合は残す。
- **変更しない**: 現に呼ばれる `render_toda_group_proof_narrative_markdown()` の関数全文、`_phase160_r7_previous_public_narrative_renderer`、`_phase160_r7_render_stable_finite_cyclic_transport_narrative`、すべての import。

削除前のコードは自動バックアップ `toda_group_proof_narrative_renderer.py.phase165_r57_r4_backup` に全文保持する。置換する既存関数はなく、最終公開 Renderer のコードは1文字も変更しない。

新規追加した `install.py` と `test_phase165_r57_r4_shadowed_branch_cleanup.py` が全文で ZIP に入っている。既存の API とテスト内容は変更しない。
