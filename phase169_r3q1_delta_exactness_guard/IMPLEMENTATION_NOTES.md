# Phase 169 R3Q1 — 修正記録

## 変更対象

- `phase168_r3_5_model_renderer.py`: `render_model_backed_narrative_markdown()` の R3Q 共通経路への切替。
- `phase168_r3_27_typed_statement_projection.py`: `typed_sentence()`, `map_property_sentence()`, `map_symbol_tex()`。`map_property_sentence()` は `typed_sentence()` の直前に新規追加。
- 新規限定テスト `tests/test_phase169_r3q_unified_narrative.py`。3件を追加（合計12件）。

元の R3Q の「すべての ProofStep は `typed_sentence()` を優先する」という設計は維持。新規の別 Renderer 経路を追加しない。

π₃²の基準テストの失敗原因：`TodaDeltaZeroStatement` の推論前提が `TodaSuspensionIsomorphismStatement` と `TodaProp42ExactnessStatement` の場合、新 R3Q 共通写像文章生成が `ImΔ=ker E=0` を表示できず、固定基準が不一致となった。

修正後は `map_property_sentence()` の Delta 零写像処理で、E 同型を利用する場合と H 全射を利用する場合をいずれも型付き前提と完全列で検証する。球面次元または群名による分岐を追加せず、前提不一致の反例を限定テストに追加。

文献登録、証明木、検索、Reference、その他文書を変更しない。1-stem 10件と2-stem既存限定テストを含め、Phase末まで全体 pytest は行わない。
