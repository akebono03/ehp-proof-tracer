# Phase 173 最終 Gate R1：Phase 167 の Reference テスト境界修正

## 失敗の事実

Phase 173 最終 Gate のアクティブ `tests/` 全体 pytest は `3541 passed, 5 failed` で終了コード1となった。5失敗は以下の3ファイルに分布する。

- `tests/test_phase167_r2_range_dedup.py`（2件）
- `tests/test_phase167_r2_shared_reference.py`（1件）
- `tests/test_phase167_r2_unified_reference.py`（2件）

失敗箇所は `next(... is_section(line, "証明"))` による `StopIteration`。現行 `phase173_r4_r15r13_unified_presentation/layout.py::canonicalize_proof_layout()` は外側の Web が `Proof` 見出しを管理するため、内側の `証明` 行を消し、Reference と本文の間を `---` で分離する。`web_group_proof_common.py::_build_group_proof_rendered_lines()` はその `---` を `kind="separator"` に変換する。旧テストは現行契約と一致していない。

## 今回変更する対象

| 変更対象 | 完全な関数単位 |
|---|---|
| `tests/test_phase167_r2_range_dedup.py` | `_reference_text()` |
| `tests/test_phase167_r2_shared_reference.py` | `test_phase167_r2_pi43_reference_has_two_general_results()` |
| `tests/test_phase167_r2_unified_reference.py` | `_reference_text()` |

`import` の変更はない。新規クラス・関数は、本 ZIP 内の `patch.py`（`git`, `normalized`, `reviewed_snapshot`, `_read_original_line_ending`, `_write_same_line_ending`, `prepare_full_units`, `_digest`, `apply_tests`, `rollback_tests`, `main`）と `tests/test_patch_contract.py` に追加する。各ファイル全文は ZIP に収録する。

## 対応の正確さ

区切りとして最初の Reference 見出しの後に存在する `kind="separator"` をちょうど1つ要求する。これにより Reference に証明本文を混入させず、従来の一般形 `\pi_n^n` や `n\ge1`、出典名、重複回数などの既存 assertion を変更しない。

探索や Proof Tree、Renderer、Citation 作成処理は変更しない。群の `(n,k)` に依存する実装分岐を増やさない。既存 API は維持する。

## テストと完了境界

- 本 ZIP の純粋な patch contract：9件 PASS（作成環境）。
- Windows で実行すべき対象：既存3モジュールの限定 pytest（6テスト）。全体 pytest はこの R1 で実施しない。
- Git blob は7件（旧テスト3件、共通 Renderer と Web 経路4件）を固定検査し、遠隔の未審査変更を拒否する。
- 失敗時に3テストの元バイト列だけをバックアップから復元する。`git reset` / `clean` / `add` / `commit` は実行しない。
- 既存の `phase173_full_test_report.json` は失敗事実として保存する。これを上書きすることも、Phase 173 を終了済みと扱うこともしない。
- R1 PASS の後、失敗済み Gate を再実行せず、新規レポートに記録する修正版 Gate を別工程で用意する。全体 pytest を再実行するのは Phase 173 最終確認だけとする。
