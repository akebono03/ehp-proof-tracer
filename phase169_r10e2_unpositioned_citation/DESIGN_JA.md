# Phase 169 R10E2-R1 — 差し替え版の設計

R10E2 限定 pytest の 7 FAIL を受けた最小修正。新しい stem・系列のルールは増やさない。

## 原因と対応

1. `SEARCH_FAILED` のテスト fixture に `diagnostics` が欠けていた。テストのみ修正。
2. 二重適用試験がパッチ後の実ファイルを「パッチ前」と誤認。`output/*.before` を使い、二度目の適用拒否を確認。
3. 既存の掲載位置付き目標にも `derived_target_without_citing_id=False` を渡していたため、以前のモックと API 呼び出しが非互換。既存経路は従来のキーワード引数だけに戻し、未掲載の導出目標に限り `True` を付ける。
4. 完成証明の Reference に対する固定基準では `Chapter V, i)` のままである。Renderer に残っていた `η 系列の定義（Chapter V, i）` への特例書き換えを削除する。文献 locator はそのまま表示する。

## Proof Tree と引用の条件

未掲載 Goal は文献の掲載位置を持つ独立の `FIXED_STATEMENT` だけを候補にし、DB を `GIVEN` に昇格させない。目標自身と同一群構造の直接 `GIVEN` を拒否する。Toda (4.5) および各生成元の懸垂像は独立に証明する。`verify_proof_tree_for_narrative()` は既存の掲載順付き経路では変更前の呼び出し契約を維持する。

## 変更一覧と Phase 境界

本番ファイル 6 件の既存関数のみ変更。module-level import 変更なし。新規機能追加なし。限定 pytest と検索・Web 監査で既存の 1/2/3-stem を確認。全体 pytest は Phase 169 終了時にのみ実行する。

## R10E2-R2: 実行時の非対象追跡ファイル差分を可視化

R10E2-R1 は限定 pytest 115 PASS と監査を完了したが、実行前後の非対象追跡ファイル一覧に差異が検出され、6本の本番ファイルを復元した。原因はログに出ていなかった。

R10E2-R2 では Python の本番コード・テストを一切変更せず `run.ps1` だけを修正する。`git diff --name-only` をパッチ対象6本の pathspec を除外して実行前後で照合する。一覧が異なる場合、追加・消滅したファイル名を表示し、`output/r10e2r2_tracked_diff.json` に保存する。本番6ファイルを復元するが、その他のファイルは自動変更しない。`git checkout`、`git reset` は使わない。全体 pytest は実行しない。
