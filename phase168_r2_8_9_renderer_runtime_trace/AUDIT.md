# Phase 168 R2-8⑨ 実行時 Reference 経路監査

- 現行 `develop` の `toda_group_proof_narrative_references.py`、`toda_group_proof_narrative_contribution_renderer.py`、`phase165_r55_nk_only_goal.py` と R2-8⑧ の監査経路を確認した。
- 既存本体・既存 API・既存テストを変更しない。新規追加は `audit.py`、`tests/test_r2_8_9_renderer_runtime_trace.py`、`run.ps1`、本 README と AUDIT のみ。
- `sys.setprofile` を一時的に有効にし、実際の共通 Renderer 呼び出し中の関数 return とローカル変数を記録する。終了時は元の profiler に戻す。
- `generic_used_step_ids` と `frontier_step_ids` の実際の値が関数ローカルにある場合のみ記録する。存在しない値は推測しない。
- `exclude_toda_group_proof_narrative_root_reference()` と最終フィルタそれぞれの before/after を観測し、同じ出典の Root と GIVEN を区別する。
- テストは新規3件に限定し、全体 pytest は Phase 168 の末尾まで実行しない。
- R2-8⑩は本監査で消失経路を確定してから最小の修正を行う。現段階では原因・証明完成を先取りしない。
