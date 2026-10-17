# Phase 165 R6-2 R4-A-R2 実装前・実装後監査

## 対象の現行コード

- `phase165_r8_rule_provider.py`: `DEFAULT_RULE_MODULES`, `discover_inference_rules`、`create_rule_expansion_provider`
- `phase165_r57_r26_generic_search_connection.py`: `build_generic_backward_expansion_provider`
- `phase165_r57_r25_premise_generation.py`: `generate_discovered_premises`
- `phase165_r52_r9_shared_math.py`: `shared_expansion_provider`
- `rule_catalog.py`: `InferenceRuleCatalog`
- `tests/test_phase165_r8_rule_provider.py`: 既存の逆向き判定テスト
- R4-A ZIP 同梱の `inventory.py`: 静的監査ロジックの読み取り専用コピー

## 変更対象のファイル・クラス・関数

新規追加のみ：`inventory_r4a.py`（既存監査器の完全コピー）、`runtime_probe.py` の `run()`、`runtime_audit.py` の `collect()`、`markdown()`、`main()`、`test_runtime_audit.py` の5つのテスト、`run.ps1`、`README.md`、`AUDIT.md`。既存ファイルとクラスは変更しない。

## 監査範囲

R8 factory が実行時に生成した規則、除外 factory、構造的に逆向き候補となる結論・前提パターンを報告する。R4-A の AST 候補との数を比較するが、factory 識別子と規則名の対応を推定しない。適用可能 Goal、実際の再帰探索、完成 ProofStep、数学的正しさ、既存テストの PASS はこの Phase では主張しない。

## 実行対象 pytest

`python -B -m pytest -q -p no:cacheprovider phase165_r6_2_r4_a_r2_runtime/test_runtime_audit.py`

## 完了条件

JSON と Markdown を生成し、エラーを含む実行結果を表示し、未実証の件数を PASS と誤表示しないこと。全体 pytest は実施しない。

## 次 Phase 境界

R4-A-R3 で実行時 factory 識別と具体 Goal に対する接続確認を行う。R4-B は群専用 Adapter の分離監査。R5 以降で数学的規則を追加する。

## R4-A-R2 Python 3.10 修正（追記）

`runtime_audit.py` の `markdown()` 内の f-string 式でバックスラッシュを使用していたため、Python 3.10 のテスト収集時に SyntaxError が発生した。規則名の置換、表示値の組み立てを f-string の外へ移し、Markdown 行を生成する方式へ修正。回帰テスト `test_markdown_escapes_pipe_without_fstring_backslash()` を追加。既存の本番コード・探索ロジックは変更しない。
