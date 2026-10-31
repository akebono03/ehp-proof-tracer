# Phase 172 R6R2R1 — 終了文書 Gate の HEAD 子孫判定訂正

## 監査結果

- R6 終了 Gate：`6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`、全体 pytest 3,546 PASS（107.52秒）、限定10セット、Web 5群 PASS。
- GitHub `akebono03/ehp-proof-tracer` の `develop` と R6 HEAD を比較：後続コミットは1件、変更は `phase172_r6_phase_closeout/` 内の監査ファイル7件の追加のみ。5文書、Renderer、Proof Tree の変更なし。
- 旧 R6R2 の `preflight()` は `HEAD == REVIEWED_HEAD` を要求していたため、検証済みの監査コミット後に失敗した。書き換えは行われていない。

## 変更対象と実装境界

1. `phase172_r6r2_document_closeout/install.py`（既存ファイル）：`ALLOWED_R6_AUDIT_BLOBS` 定数を追加。`reviewed_head_lineage()` を `preflight()` 直前に追加し、`preflight()` 関数全体の判定を置換。import は変更なし。ファイル全文を `payload/install.py` に収録。
2. `phase172_r6r2r1_head_lineage_fix/fix.py`（新規ファイル）：オリジナル Installer SHA-256・訂正版 SHA-256 の検査、修正内容の非破壊事前検査、原子置換、限定 pytest、既存文書 Installer の実行、失敗時の Installer 復元。
3. `phase172_r6r2r1_head_lineage_fix/tests/test_fix.py`（新規ファイル）：子孫・非子孫、許可された監査ファイル追加、範囲外ファイル、変更状態、異なる blob、欠落・重複、全文 payload を検査する8件。
4. `run.ps1`（新規ファイル）：DryRun／Apply を区別する PowerShell Runner。新規 README は英語、監査計画とコード説明は日本語。

変更する本番数学コード、Proof Tree、Renderer、テスト（既存）：なし。既存の5文書は従来の R6R2 Installer が全文を生成して適用する。`development_log.md` と `proof_records.md` は履歴を保持して追記する。

## Gate

- ローカル `develop` と `origin/develop` が一致し、R6 HEAD の子孫であること。
- R6 HEAD 以降に新規追加された7ファイルのパス・状態・Git blob がGitHubで確認した値と完全一致すること。対象外の差分は拒否。
- 5文書の旧 Git blob、Renderer の確定済み Git blob は従来どおり厳密に検証すること。
- R6 の `closeout.json`、全体 pytest ログ、Web 証明を再照合すること。全体 pytest は再実行しない。
- DryRun は既存ファイルを変更しない。Apply 成功時は従来の R6R2 文書のみ変更。失敗時は既存 Installer と必要に応じて文書を復元する。

## 完了条件と次 Phase 境界

`PASS_DOCUMENT_CLOSEOUT_CORRECTED` と `PASS_PHASE172_DOCUMENT_CLOSEOUT` の両方を確認する。`git diff --check` を通過させ、`README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` の全文出力を確認する。Phase 173 の機能や新たな数学的結論は実装しない。
