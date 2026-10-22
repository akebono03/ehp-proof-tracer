# R3-5 変更一覧

- `phase165_r52_r3_web_adapter.py`: import を含む全ファイルを同梱。`build_partial_web_group_proof_view` の完全置換。末尾のオプション引数 `narrative_model` のみ追加。
- `phase168_r3_5_model_renderer.py`: 新規ファイル。`render_model_backed_narrative_markdown` をファイル先頭の import の後に追加。全文を同梱。
- `tests/test_phase168_r3_5_model_web_boundary.py`: 新規ファイル。import とテスト関数全文を同梱。
- `run.ps1`: Backup、配置、限定 pytest、診断 probe。既存 Web 経路は変えない。

完了条件: 限定3テストおよび pi_4^2 の実行時診断が PASS。次 R3-6 の境界: Search が使用した screened bridge を結果と一緒に受け渡す仕組みの追加と、デフォルト Web 経路の一本化。全体 pytest は Phase 最終時のみ。
