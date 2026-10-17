# R4-4 実装記録

対象: `map_property_rules.py` の import と `isomorphism_implies_injective_inference_rule()` 全体。新規: `r4_r4_patch.py`、対象テスト2ファイル、`run.ps1`。

## 内容

同型写像が単射である既存規則について、順向き `conclusion_builder` を維持しつつ、`PatternVariable` を用いた `conclusion_pattern` と `premise_patterns.statement_pattern` を追加する。共通の R8 / R26 はこれにより `InjectiveMapStatement(f)` を目標として `IsomorphismStatement(f)` を必要前提として提案可能となる。

これは一般的な規則であり、特定の $\pi_n^k$ をハードコードしない。前提が証明されたことを意味せず、新しい `GIVEN` を生成しない。

## 実行テスト

`test_r4_r4.py` の6件を導入前に実施し、導入後 `test_r4_r4_integration.py` の4件と `tests/test_phase165_r8_rule_provider.py` を実施する。全体 pytest は実施しない。

## 完了条件

R8 と R26 が実際に逆向き候補を生成でき、無関係な Goal に候補を出さず、順向き builder を保持すること。次段階で他の一般規則の逆向き能力を順次実証する。
