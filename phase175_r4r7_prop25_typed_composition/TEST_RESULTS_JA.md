# Phase 175 R4R7R1 — 限定テスト記録

## 先行するユーザー環境の結果（修正前）

- R4R7 限定 pytest: **135 passed**。
- DryRun Gate: `FAIL_R4R7_PROP25_TYPED_INFERENCE`。
- エラー: `R4R7_UNREVIEWED_HEAD: 11968d23724cee147520b5fa3fd5a6e89989003e`。
- 本実行: 未実行。

## GitHub 履歴確認

`c48fdc307ba67a5e21b0ef49d57953468f7b47e2` から `11968d23724cee147520b5fa3fd5a6e89989003e` への直系1コミット。差分は R4R6 監査パッケージ8ファイルで、本番コード更新なし。

## 修正版（作成環境）の検証

- 新規合成 Git 履歴テスト6件: 実際の一時 Git リポジトリを使い、正常な先行HEAD・異常ファイル・後続コミット・blob 漂流・監査 byte 改変・祖先不一致を確認する。
- 修正後の `tests/test_rule.py` + `tests/test_audit.py` を合成スタブ環境で実行：**66 passed**。
- `run.ps1` の限定 pytest 対象は R4R7 初版から変更しない。
- 全体 pytest は実行しない。
- 実環境の DryRun・本実行は未確認。

## 境界

新規 GIVEN 0、追加数学規則 0（R4R7 で導入済みの一般規則1件は維持）、本番変更 0、公開 Provider 未接続、`π_9^5` 未完成。
