# Phase 168 R2-4 — 既存テスト期待値更新

R2-4 により `resolve_specialized_goal_citing_id()` が π₄³ と π₃² の対応命題を返すようになったため、以前の `None` 期待を更新する。

- 本体実装は変更しない。
- `phase166_r3t_goal_source_binding/test_connection.py` のテスト3関数を全文置換する。
- π₄³・π₃² の命題 ID と、自己参照・後続命題の不採用を検証する。
- テストファイルは置換前にバックアップする。
- 限定 pytest のみ実施する。

実行方法：

```powershell
Expand-Archive -Path "$HOME\Downloads\phase168_r2_4_test_expectation_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r2_4_test_expectation_fix\run.ps1"
```

注: 当該リポジトリの実環境での pytest は未検証。コードは構文検査済み。
