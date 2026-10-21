# Phase 166 R3-AU-11 接続監査

変更対象は新規 `audit.py`（`audit`、`main`）、`test_r3au11.py`（3テスト）、`run.ps1`、`README.md`、`AUDIT.md` のみ。既存コードを変更しない。

既存の `registered_group_goal_candidates()` は `k >= 2` のとき DB 型付き候補を優先する。`search_group_from_registered_goal()` は登録目標を取得して共通の証明探索へ渡す。レンダラーは候補の生成元を LaTeX 表示できる。

実際の Web view は今回直接呼び出さないため、公開画面への接続と証明完了は認定しない。次は公開 Web の entrypoint とその限定テストを実行して確認する。全体 pytest は Phase 166 終了時のみ。
