# Phase 168 文書更新 — 実行説明

## 対象

- `README.md`：英語で全文を書き直す。
- `docs/design.md`：現在の構造・信頼境界を追記する。履歴本文は保持する。
- `docs/development_log.md`：Phase 168 の完了と実行ログの根拠を追記する。
- `docs/roadmap.md`：末尾の「Phase 168 未着手」という古い予定を確定した完了範囲と次の計画に更新する。
- `docs/proof_records.md`：3群の出典・ProofStep 数・検証結果を追記する。

既存の本文を抜粋やダイジェストで置き換えない。ZIP 実行時、利用者の checkout にある**完全な元文書**を読み込み、各文書の全文を生成して保存する。GitHub 現行コードと異なる古い文書・カスタム文書を誤って上書きしないよう、見出し・終了マーカー・既存アンカーを確認する。不一致なら編集せず停止する。

## PowerShell

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_documentation_closeout_20261025.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_documentation_closeout_20261025\run.ps1"
```

## 更新後の全文とバックアップ

実行後に `phase168_documentation_closeout_20261025/output/full_files/README.md` と `output/full_files/docs/` 以下の4文書を出力する。各ファイルは**省略のない全文**である。ZIP `output/phase168_documentation_full_files_review.zip` に更新後の5全文・元の5全文・SHA-256 manifest を含める。

バックアップは `output/backups/` に格納し、2回目実行は SHA-256 を検証して冪等的に終了する。実行後にユーザーが編集したファイルがある場合、復元は上書きを拒否する。

元へ戻す場合：

```powershell
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_documentation_closeout_20261025\restore.ps1"
```

## 注意

文書だけを変更する。実装・既存テスト・固定全文基準・数学的根拠には触れない。Phase 168 の最終 pytest はすでにログで合格（現行 3546 / 限定 86 PASS）しているため、**ここでは再実行しない**。無制限の歴史的テストや全112群の数学的完全性を認定しない。GitHub への commit / push は自動実行しない。
