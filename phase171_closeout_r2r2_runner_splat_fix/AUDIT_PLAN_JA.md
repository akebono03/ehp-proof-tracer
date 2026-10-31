# Phase 171 Closeout R2R2 — PowerShell 引数展開修正

## 現況

- GitHub `akebono03/ehp-proof-tracer` の `develop` は 2026-10-31 の監査時点で `3e74849bf90bc115c16503ddd46d49996baa0856`。
- R1R1 の意味論テスト修正はコミット済みで、R2R1 はこの後続コミットを認めるように修正済み。
- しかし R2R1 の `run.ps1` が `$PythonArguments` を組み立てた後で `& python @Args` を実行するため、Python REPL が起動し、`install.py` が実行されない。
- Windows のユーザーログでは追跡済み Git 変更はなく、文書更新処理には到達していない。

## 変更対象

- **変更する既存ファイル**: `phase171_closeout_r2r1_committed_head_guard/run.ps1` のみ。
- **変更するスクリプトの単位**: `run.ps1` 全文（`@Args` を `@PythonArguments` に変更）。
- **新規追加位置**: リポジトリ直下の `phase171_closeout_r2r2_runner_splat_fix/` に `run.ps1`、`repair.py`、`replacements/run.ps1`、`tests/test_repair.py` と説明文書を追加。
- import の変更なし。本番 Python コード、数学的 Proof Tree、証明文、既存の5文書は修正しない。

## ガード

1. Git ブランチが `develop` でローカル HEAD がローカル `origin/develop` と一致すること。
2. staged 変更が存在しないこと。
3. 変更前後の `run.ps1` が内容ハッシュ・1トークン差分の検査に合格すること。
4. R2R1 の `install.py` と既存 R2 実行スクリプトの内容が検証済みであること。
5. R2 の `update_docs.py` が元の状態か、R2R1 修正済みの状態であること。
6. 修正前の `run.ps1` を `%LOCALAPPDATA%/EHPProofTracerRecovery/phase171_closeout_r2r2_*/run_before.ps1` に退避し、監査 JSON を保存すること。

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_Closeout_R2R2_Runner_Splat_Fix.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_closeout_r2r2_runner_splat_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_closeout_r2r2_runner_splat_fix\run.ps1"
git status -sb
git diff --check
git diff --stat
```

- `-DryRun` は何も置換せず、R2R2 と R2R1 のそれぞれの内容ガードを実行する。
- 通常実行は最小追加テストを実行後、R2R1 の `run.ps1` を1行修正してそのまま実行する。
- R2R1 は自身の4件の追加テストと R2 の文書全文生成・限定 pytest を実行する。
- 全体 pytest は一切実行しない。Phase 171 の最後の終了 Gate のみに留保する。

## 完了条件

- `PHASE171_CLOSEOUT_R2R2_RESULT=PASS_RUNNER_CORRECTED`
- `PHASE171_CLOSEOUT_R2R1_RESULT=PASS_R2_DOCUMENTS_PENDING_PHASE_END_FULL_SUITE`
- `PHASE171_CLOSEOUT_R2_RESULT=PASS_FIVE_FULL_DOCUMENTS_PENDING_FULL_SUITE`
- README と4文書の計5件だけが実際の文書更新として反映され、既存の Proof Tree とソースコードは変更されない。

## 次の Phase との境界

Phase 171 は文書の正式終了記録、現行アクティブ `tests/` の全体 pytest と最終 Git 監査後に終了と判定する。重複式・`DB prior` の表示改善は Phase 172 に留保する。
