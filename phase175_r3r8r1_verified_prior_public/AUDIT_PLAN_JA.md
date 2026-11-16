# Phase 175 R3R8R1R2 — 後続 Phase 作業ツリー検査の修正

## 実際に発生した停止

R3R8R1R1 の DryRun は、`R3_PROTECTED_TRACKED_CHANGE: phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md` で停止した。R3 の `audit_only_tracked_snapshot()` は R3 自身の6ファイルだけの変更を許可していた。R3R8R1 が Git に追跡された後の ZIP 再展開により、許可済みの後続文書が変更された状態を誤って拒否した。

これは数学的証明の失敗ではなく、本実行の公開接続判定は未実施である。

## 変更単位

1. 新規 `phase175_r3r8r1_verified_prior_public/worktree_guard.py` の `reviewed_tracked_snapshot()`：Git の `--porcelain=v1 -z` を使用し、` M` 状態の既知の監査ファイルだけを SHA256 付きで記録する。未知の追跡済みファイル、ステージ済み、削除、リネーム、事前の公開コード変更は不許可。
2. 既存 `phase175_r3r8r1_verified_prior_public/audit.py`：import 全文を更新し、`R3R8R1_REVIEWED_FILES` に2ファイルを追加し、`extended_scoped_preflight()` 全体を変更。R3R8R1 の監査ファイル変更がない場合は従来の R3.preflight を使用。ある場合は Source Guard の実体（R1/R2の確認と R3 の全 pin）を呼び直す。過去の R3/R3R7 の検査は変更しない。
3. 既存 `phase175_r3r8r1_verified_prior_public/install.py`：import 全文、`preflight()` 全体、`verify_postflight()` 全体を変更。改変許可の範囲が実行中に増加しないよう変更前・変更後 SHA256 を比較する。
4. 新規 `tests/test_worktree_guard.py`：一時 Git リポジトリで status、インストール、復元を検証する。既存 `tests/test_lineage.py` の追加ファイル試験を1件拡張。

## 数学・公開証明の境界

Source-first（出典優先）、First Successful Proof Search（最初の成功で終了）を維持する。今回の修正だけでは `π_7^3` を完成扱いとしない。R3R7 による6つの `INFERRED` と R3R8R1 の検証済み先行DB一般規則は変更しない。通常検索が `complete`、未解決 Goal 0、Trust True、Web `generic-complete-proof` であることを本実行で確認する。

`phase165_r52_r9_shared_math.py`、R3、R3R7、文献登録、既存 Renderer は直接変更しない。5文書（`README.md`、`design.md`、`development_log.md`、`roadmap.md`、`proof_records.md`）は今回変更しない。全体 pytest は Phase 175 終了時のみ実施する。
