# Phase 171 Closeout R2R4 — 復元された R2 ソースの Guard 修正

## 監査結果と原因

- 現行 `develop`（2026-10-31 確認）: `3e74849bf90bc115c16503ddd46d49996baa0856`。
- R2R2 は実行引数修正に成功。R2R1 は文書更新処理における改行形式 (`CRCRLF`) で停止して元の R2 ソースを復元した。
- R2R3 は R2R1 適用後の SHA-256 のみを許可していたため、復元後の正当な R2 元ソースを拒否した。
- 数学的証明コード、Phase 169 R3Z テスト、５文書はこの原因とは無関係であり変更しない。

## 変更対象（唯一の既存ファイル）

`phase171_closeout_r2r3_mixed_line_ending_fix/install.py`

- 定数 `REVIEWED_R2_BASE_SHA256` を `REVIEWED_OLD_SHA256` の直前に追加する。
- `preflight()` 全体を更新し、対になった R2 元ソースと R2R1 ソースと R2R3 修正済みソースの正確な SHA-256 を受理する。
- 対応しない状態を混在させる操作・既知以外のファイル内容を拒否する。
- その他の import、メソッド、関数、演繹規則等は変更しない。

新規追加の `phase171_closeout_r2r4_restored_source_guard/repair.py` はガード付き補修・ロールバックと R2R3 の呼び出しを担当する。`tests/test_repair.py` は新規ファイル（`tests/__init__.py` の後）として追加する。変更の最小単位は上記モジュール全体である。

## 実行順

1. `run.ps1 -DryRun`: Git HEAD・変更状態・ファイル SHA-256 と対の整合性を確認。ファイル変更なし。
2. 通常実行で修正前 `install.py` を Recovery にバックアップし、修正後の全文で置換する。
3. R2R4 の追加 Guard テストを限定実行する。
4. R2R3 `install.py --dry-run` を実行し、安全検査を通す。
5. R2R3 本番を実行。R2R3 の内部で改行対応された R2 の全文文書生成と限定テストを実施。
6. 文書５ファイルだけが変更されたことを確認。全体 pytest は行わない。

## ロールバック

R2R4 の障害時には R2R3 installer の変更を復元する。文書書き込み開始後の障害は、R2R3 の既存ロールバックにより文書と R2 本体を復元する。`git reset`、`git pull`、全体 pytest は実行しない。

## 完了条件

- `PHASE171_CLOSEOUT_R2R4_R2_SOURCE_STATE=R2_BASE`（ユーザーの最新ログからの期待）
- `PHASE171_CLOSEOUT_R2R4_CONTENT_GUARD=PASS`
- R2R3/R2 の限定 pytest PASS
- `PHASE171_CLOSEOUT_R2_RESULT=PASS_FIVE_FULL_DOCUMENTS_PENDING_FULL_SUITE`
- `PHASE171_CLOSEOUT_R2R4_RESULT=PASS_FIVE_DOCUMENTS_PENDING_PHASE_END`
- `git diff --stat` が５文書だけ、`git diff --check` で問題なし

**次 Phase との境界**：Phase 171 の最後の Gate でのみ現行アクティブ `tests/` 全体 pytest を１回実行する。Phase 172 の表示修正は行わない。
