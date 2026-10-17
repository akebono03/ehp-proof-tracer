# Phase 165 規則台帳監査 R3

## 変更対象
- 本番コード：変更なし
- `audit.py`：新規 `classify_rule`, `_runtime_factories`, `_source_registry_mentions`, `main` を追加
- `test_audit.py`：新規テスト関数2件
- `run.ps1`：リポジトリ直下からモジュール実行

## 確認範囲
- Rule Factory の実装有無
- R8 標準探索の発見対象かどうか
- `conclusion_pattern` の有無と必須引数
- 指定した規則台帳ファイル中の参照有無（有効な登録の証明ではない）

## 完了条件
`audit_result.json` が出力され対象限定 pytest が成功すること。

## 次段階との境界
規則の追加・共通探索接続・証明完了は今回行わない。結果を受けて変更する。
