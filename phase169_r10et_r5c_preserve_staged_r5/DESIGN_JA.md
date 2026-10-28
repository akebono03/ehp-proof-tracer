# Phase 169 R10ET-R5C — Git staging area を維持するガード修正

## 原因

R5B はコミット済み R4（HEAD `3a8014efb91ddf76060c4d07d73153e55ea52c75`）を正しく認識したが、旧 R5 監査フォルダの新規9ファイルが `git add` 済みのため拒否した。本体コードや既存テストに未コミット差分はない。エラーは実装前の安全確認に限定される。

## 修正対象

- 新規パッケージ `phase169_r10et_r5c_preserve_staged_r5/run.py`: `reviewed_index_snapshot`（新規、`verify_preconditions` 直前に追加）、`verify_preconditions` 全体、`main` 全体。
- `tests/test_r5c_head_guard.py`: R5B の確認テストを移植し、index 受容・拒否の限定テストを追加。
- `README.md`（英語）、`DESIGN_JA.md`（日本語）を全文作成。
- R5B の `patch.py`, `audit.py`, `tests/test_r5_patch.py`, `tests/test_r5_live.py` はパッケージ名以外の実装を変えない。

## 安全境界

Git index は空、または旧 R5 パッケージの9ファイル全てが status `A` の場合に限り許可。`git diff --cached --name-status` で許可ファイルを照合し、`git diff --cached --raw` を実行前後で比較する。`git add`、`git restore --staged`、`git reset` は一切実行しない。未知の index 変更、既存本体ファイルの stage、予定外の HEAD は拒否する。

既存 R4 2ファイルのバイト列と、R5 対象5ファイルの Git blob を従来どおり照合する。本体変更は `shared_expansion_provider()` 全文と関連4テストに限定。R2 で確認した共通 Definition の本番優先、16ケースの complete・Trust・Reference・Projection の一致を検証。失敗時は R5 の5ファイルのみ復帰、ステージされた旧 R5 9ファイルはそのまま保持。

## 完了条件

`R10ET_R5C_COMPLETE=PASS`、`R10ET_R5C_INDEX_PRESERVED=True`、限定 pytest PASS、16ケースの実証監査 PASS。全体 pytest は Phase 169 終了時だけ実行する。

## 次段階との境界

R5C は R5B のステージ領域の取り扱いだけを修正する。Definition の意味を拡張せず、台帳削除、未検証引用の省略、全体リファクタリングを行わない。
