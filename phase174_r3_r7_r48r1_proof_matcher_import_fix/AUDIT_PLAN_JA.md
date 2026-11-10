# Phase 174 R3-R7-R48R1 — import 漏れ修正

## 監査済みの状況

- GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD: `398ad86615ec8484e5a9fe04143e367c059d4c85`。
- R48 `Source Guard` と `DryRun` は PASS、本監査は `NameError: name 'find_inference_matches_for_rule' is not defined` で停止。
- `proof.py` には `find_inference_matches_for_rule` の定義が存在し、R36 の監査コードも同じ関数を import している。
- `inspect_integrated_lower_kernel_frontier()` 内の既存 `from proof import` に当該名が欠けていた。

## 変更ファイル・関数

1. `phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/audit.py` の `inspect_integrated_lower_kernel_frontier()`：既存関数内の import 部分のみを変更。
2. `phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_static.py`：`test_kernel_diagonal_matcher_is_imported_in_the_audit_function()` をファイル末尾に新規追加。
3. 新規修正用ディレクトリ `phase174_r3_r7_r48r1_proof_matcher_import_fix/`：ガード付きパッチ、修正前後の完全ファイル、限定テスト、文書、PowerShell 実行スクリプト。

## 証明上の境界

- 今回は `R48` 監査の例外を解消するための import 修正のみ。
- 数学的命題、出典、GIVEN、Provider、Canonical Proof Search の順序、共通 Renderer を一切変更しない。
- DryRun はハッシュ検証のみでファイルを変更しない。実実行では2ファイルだけを検証して置換し、R48 の本監査と限定 pytest を再実行。
- R48 の核の推論が検証されるかは、修正後の本監査ログにより判断する。`pi_12^7=0` の完成は宣言しない。
- 全体 pytest は Phase 174 の最後のみ。
