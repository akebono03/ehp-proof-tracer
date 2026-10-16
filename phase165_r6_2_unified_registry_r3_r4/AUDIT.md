# Phase 165 R6-2 R3-4 変更記録

- 対象: `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` の4つの直接呼び出し。
- 新規: `context_provider_registry.py` の `build_context_expansion_provider_registry()`。
- 既存 `UnifiedExpansionProviderRegistry` を再利用し、Provider ID を付与。
- 適用条件と呼び出し順序、`available + prior_conclusions` および `available` の別を維持。
- 群別 Adapter は作成しない。証明完成は未確認。
- 全体 pytest は Phase の最後に実施。

## 次の境界

R4 では具体的な Goal に対し、候補生成と推論規則の適用可能性を検証する。
