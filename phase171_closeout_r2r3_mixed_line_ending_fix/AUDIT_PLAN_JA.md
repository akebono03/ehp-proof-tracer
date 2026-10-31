# Phase 171 Closeout R2R3 — CRCRLF 混在文書の修正監査

## 前提と診断

GitHub `akebono03/ehp-proof-tracer`、`develop`、確認済み `HEAD=3e74849bf90bc115c16503ddd46d49996baa0856`。ユーザー側の実行ログで `R2R2_RESULT=PASS_RUNNER_CORRECTED` を確認した一方、R2R1 は `lf_text` の `ValueError("unknown line endings")` で復元された。

GitHub にある `docs/design.md` の本文には `\r\r\n` の連続した改行が 3,401 箇所あり、既存の `lf_text()` は `\r\n` のみ正規化するため残存 `\r` を不正扱いした。元の改行をすべて LF / CRLF に変換すると歴史的本文のバイト列を壊すため、比較時の正規化と保存時の追記を厳密に分離する。

## 変更対象（2ファイルのみ）

1. `phase171_closeout_r2_documentation_full_output/update_docs.py` — `import re` 追加、`lf_text()` 全体を置換、`document_newline()` を `lf_text()` の直後に追加、`updated_document()` と `current_files()` を全体置換。
2. `phase171_closeout_r2_documentation_full_output/tests/test_document_writer.py` — `test_guarded_full_document_end_to_end_on_local_fixture()` 全体を置換し、5つの独立した回帰テストをファイル末尾に追加。import は変更しない。

変更対象の2ファイルの全文は `replacements/` 下に収録。必要な import と全関数は `CODE_FULL_JA.md` にも収録する。既存の数学的コード、Proof Tree、Renderer、Web、5文書の Phase 171 節本文は変更しない。

## 動作と安全条件

- `-DryRun` は読み取り専用。旧版・新版2ファイルの SHA-256、混在状態の拒否、文書5件の Git blob、R1R1 証明回帰テスト blob、採用済み5節の SHA-256、Git 差分と HEAD の系譜を照合する。
- 本実行は修正前の2ファイルと文書5件を `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_closeout_r2r3_*\BEFORE` にバックアップし、2ファイルを原子的に置換する。
- `tests/test_install.py` と修正済み文書テストの限定 pytest を実行。その後、R2 文書更新の `--dry-run`、通常実行に進む。R2 は既存の4モジュールに限定した pytest を実行し、5文書の全文と ZIP を外部 recovery フォルダへ出力する。
- 途中失敗では今回の2ファイルと文書5件を元のバイト列へ復元する。Git の reset/pull/commit はしない。
- `docs/design.md` の歴史的本文は `\r\r\n` 等を含む元のバイト列のまま保持し、追記部分だけを現行文書末尾の改行方式で符号化する。

## 完了条件

通常実行で `PHASE171_CLOSEOUT_R2R3_RESULT=PASS_FIVE_DOCUMENTS_PENDING_PHASE_END` と R2 の `PASS_FIVE_FULL_DOCUMENTS_PENDING_FULL_SUITE` が両方出ること。`git diff --check` が成功し、追跡済み差分は5文書に限定されること。`README.md` は英語、`docs/` の4文書は日本語。`development_log.md` と `proof_records.md` は歴史本文を保持して追記する。

**Phase 171 の終了とはまだ判定しない。** 全体 pytest は最終 Gate に1回だけ実行する。Phase 172 の表示改善には着手しない。
