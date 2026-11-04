# Phase 173 Final Gate R2R1 — 過去の失敗証拠の参照先修正

## 適用前の監査

2026-11-04 の R2 `-DryRun` は限定 Gate テスト14件を PASS した後、`verify_prior_failure()` が `Previous Phase 173 failure evidence is incomplete` で停止した。これは全体 pytest の再実行前である。R2 は `$env:LOCALAPPDATA` 配下に4ファイルがあることを要求する。一方、第1回の全体テストの失敗ログは `C:\Users\oomae\AppData\Local\EHPProofTracerRecovery\phase173_final_gate\` に記録され、今回の実行プロファイルは `C:\Users\user` になっている。原因候補は実際の保存先と検査先の不一致であり、前回記録の存在およびアクセス可能性は Windows 環境での検査が必要である。

GitHub `akebono03/ehp-proof-tracer` の `develop` について、修正前基準 `ac9149beaf91eeef382bc816234bd2d895398667` と、現行 `25b1ee1f7c848356604061991db06265cfccb296` の差分を確認した。追加対象は最終 Gate 補助ファイルと Phase 167 の3テストで、数学的な Proof Tree / Renderer の変更はない。R2 Gate の元コード・関連14テストを確認済みである。

## 変更対象

- `phase173_final_gate_r2_recovery/gate.py`
  - 既存 `validate_snapshot()`：ローカルとリモートの承認済み fast-forward（早送り）を、差分対象・既存の15 Source Blob・修正済み3テストの SHA-256 で検査する。divergence（履歴分岐）、未審査の変更は拒否する。
  - 既存 `finalize()`：テスト報告に `remote_head` を追加する。従来のテスト用 snapshot で未指定の場合はローカル HEAD を使い既存 API を維持する。
  - 既存 `main()`：remote HEAD をログに明示する。
  - 新規定数 `BASE_R1_TEST_BLOBS` と `APPROVED_REMOTE_R1_BLOBS`：上記承認済み3テストの Git Blob を保持する。
- `phase173_final_gate_r2_recovery/run.ps1`：`-PreviousEvidencePath` オプションを追加。元の失敗レポートが保存されたアカウントと現在のアカウントを区別し、完全な4ファイルが存在する場合だけ続行する。元の失敗証拠を直接読み取り、コピー・削除・上書きをしない。
- 新規 `phase173_final_gate_r2r1_evidence_path_recovery/patch.py`、`run.ps1`、`tests/test_patch_contract.py`：元 R2 ソースのバイト一致検査、バックアップ、安全な置き換え、限定テストを実装する。

既存数学実装、既存の5件の失敗内容、証明の Trust Boundary（信頼境界）、テストの集合、文書5件は変更しない。

## 実行境界

R2R1 の `DryRun` と通常適用は、Gate 補助ファイルの修復と関連 pytest のみ。**全体 pytest を実行しない。** 修復が成功した後に、元の `phase173_final_gate_r2_recovery/run.ps1` を `-DryRun`、通常実行の順に別途実行する。正常時には現行 `tests/` の 3,546件 PASS、終了コード0を期待するが、この ZIP の作成時点ではその実測結果をまだ確認していない。

失敗記録のファイル名は `phase173_full_test_report.json`、`phase173_full_test_attempt.json`、`active_suite_stdout.txt`、`active_suite_stderr.txt` である。存在確認に成功しても R2 の `verify_prior_failure()` で形式、5件の名前、件数まで検査する。ユーザーが元ファイルにアクセスできない場合、`-PreviousEvidencePath` で元の実在ディレクトリを指定する。ファイルを架空に生成して Gate を通さない。

新しい R2 結果は現在のプロファイルの `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_final_gate_r2\` に別保存し、以前の `phase173_final_gate` を変更しない。成功後も Phase 173 終了文書への追記と最終レビューが必要である。
