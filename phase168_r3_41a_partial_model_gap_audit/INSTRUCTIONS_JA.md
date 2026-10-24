# Phase 168 R3-41A — 未完成証明の表示経路監査

## 範囲

R3-40F1 により、標準 Web Narrative が共通 Renderer へ接続され、4群の依存逆転が0件であることが確定した。

R3-41A は未完成証明 `PARTIAL`、`SEARCH_FAILED`、`NOT_SEARCHED` の既存表示と、同一 `PartialProofResult` を入力した共通 Model Renderer の表示を比較する。新しい数学的な規則・出典・結論は追加しない。

## 新規ファイル・関数

- `phase168_r3_41a_partial_model_gap_audit/audit.py`
  - `_function`, `_named_calls`: AST の補助関数
  - `analyze_route_contract`: 現行 public Web / Flask / Adapter / Renderer の静的監査
  - `synthetic_cases`: 不完全な探索結果を3通り用意
  - `audit_incomplete_statuses`: 旧 fallback と共通 Model の表示項目を比較
  - `markdown_report`: 日本語監査結果生成
  - `run_audit`: 監査結果を JSON/MD/ZIP へ保存（ディレクトリは関数内で作成）
  - `main`: CLI の入口
- `phase168_r3_41a_partial_model_gap_audit/tests/test_audit.py`: 限定テスト4件
- `phase168_r3_41a_partial_model_gap_audit/run.ps1`: pytest と監査を実行

これらはすべて新規ファイル。既存ソースや既存テストは変更しない。ソースおよびテスト関数は各ファイル内に全文掲載しており、省略はない。

## 実行

リポジトリのルートから展開後、次を実行する。

```powershell
powershell -ExecutionPolicy Bypass -File .\phase168_r3_41a_partial_model_gap_audit\run.ps1
```

限定 pytest は、本パッケージの4件と既存の Web Adapter・標準 Web Model 既定・Flask 接続テストのみを実行する。全体 pytest は Phase 168 の最後のみ。

成功時：`output/audit.json`、`output/audit.md`、`output/review_bundle.zip` を生成する。結果の ZIP をアップロードする。

## 完了条件・次工程との境界

1. 現在の Web 既定が model であること。
2. カスタム探索入力の no-model fallback が実在すること。
3. 不完全な探索結果3状態の既存表示が失われていないこと。
4. 不完全な結果が直接共通 Renderer に渡された場合の表示差を記録すること。

次の R3-41B で共通 Narrative Model に未解決 Goal・探索状態・診断を含める設計を検討する。R3-41A では機能追加・旧 fallback 撤去を実施しない。
