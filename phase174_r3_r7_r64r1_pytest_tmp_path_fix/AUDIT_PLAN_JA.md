# Phase 174 R64R1 — Windows pytest `tmp_path` 修正

## 事前監査

- GitHub `akebono03/ehp-proof-tracer` の `develop` とコミット `e5e392ddd2177fc4db70da48b1c1e6418b33c519` の一致を確認。
- R64 の監査コード・テスト・実行スクリプトを R64.zip から読み込み、現在の利用状況と pytest の失敗ログを照合。
- R63 の関連テストと既存 Renderer を確認。既存 Production file の変更なし。

## 変更対象

1. `phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py` の `test_source_guard_rejects_tamper()`：`target.parent.mkdir(parents=True, exist_ok=True)` に変更。
2. 新規 `phase174_r3_r7_r64r1_pytest_tmp_path_fix/install.py`：1関数の厳密検査・置換。関数 `git_blob_sha`, `normalized_contents`, `patch_test`, `review`, `git_local_head`, `main`。
3. 新規 `phase174_r3_r7_r64r1_pytest_tmp_path_fix/tests/test_install.py`：独立した適用・拒否・EOL のテスト。
4. 新規 `phase174_r3_r7_r64r1_pytest_tmp_path_fix/run.ps1`：DryRun、監査、限定 pytest。

`test_source_guard_rejects_tamper` の import 全文は変更なし。既存クラス・他関数・`audit.py`・Renderer・5主要文書は変更しない。

## テスト・完了条件

1. Reviewed file Source Guard PASS。新旧 R64 テスト SHA はともに固定。
2. DryRun でファイルは変更されない。
3. 本実行で元のテスト1関数のみ変更、同じ ZIP の再実行も許容。
4. R64 audit（14段落中3検証済み、6段落中2検証済み）PASS。
5. R64R1/R64/R63 限定 pytest PASS。pytest キャッシュを無効化。
6. `PASS_R64R1_FOCUSED_AND_R64_COVERAGE_FRONTIER` を出力。

## R65 との境界

この修正は純粋なテストの一時ディレクトリ生成条件の訂正。新規 GIVEN、数学規則、出典の追加・削除、未監査15段落の認定は一切行わない。全体 pytest は Phase 完了時のみ実施。
