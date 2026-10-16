# R6-2 R4-A 実装前・実装監査

GitHub `akebono03/ehp-proof-tracer` の `phase165_r8_rule_provider.py`、`rule_catalog.py`、`phase165_r52_r9_shared_math.py`、`phase165_r52_r23_existing_rule_adapter.py`、`phase165_r57_r26_generic_search_connection.py`、`tests/test_phase165_r8_rule_provider.py` を確認した。

## 確認事項

- R8 は9モジュールの、引数なしかつ命名条件を満たす規則 factory を自動収集する。
- R57-R26 は規則候補の結論照合と前提生成を共通探索に接続する。
- 共通 `shared_expansion_provider()` は R57-R26、証人による逆向き、seeded 逆向きを併用する。
- `expand_existing_pi43_rules` が呼び出されるため、群専用 Adapter は残る。
- 静的な接続検出と特定 Goal の実行可能性は別の意味であり混同しない。

## 変更単位

- 新規 `inventory.py`：`audit()`、`markdown_report()`、`main()` および補助関数。
- 新規 `test_inventory.py`：5個の対象テスト。
- 新規 `run.ps1`：対象テスト実行後に監査ファイルを出力。
- 新規 `README.md`、`AUDIT.md`。
- 既存ソース・テスト・ドキュメント：変更なし。

## 境界

R4-A は AST で規則候補を収集し、確実に言える範囲に限定して報告する。自動収集に合致するだけでは Backward=True とみなさず、構文上の接続証拠のみでは動作保証を行わない。R4-B で実際の規則適用テストと分類、R5 以降で一般規則の不足解消を行う。
