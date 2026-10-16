# Phase 165 R6-2 統一規則台帳 R3-3

## 変更対象

- 新規 `phase165_r6_2_unified_registry_r3_r3/provider_registry.py`: `RegisteredExpansionProvider`, `UnifiedExpansionProviderRegistry`, `build_shared_expansion_provider_registry()`。
- 既存 `phase165_r52_r9_shared_math.py`: `shared_expansion_provider()` の固定 Provider 4件と caller 追加 Provider を ID 付き台帳から取得するよう変更。import 一行を追加。
- 新規 `install.py`, `test_r3_r3.py`, `run.ps1`。

## 境界

R1 の Rule ID 台帳は変更しない。R26 / Witness / Seeded に供給する同じ規則集合を維持する。追加の Provider は明示指定のみ。規則と Provider の数学的同一性は断定しない。別の直接接続（`options.extend`）は今回変更しない。群専用 Adapter は復活させない。全体 pytest は実施しない。

## 完了条件

7件の対象テスト成功、インストーラーの idempotence、既存の共有モジュール import 成功。R3-4 で直接接続の Provider を分類・統合する。
