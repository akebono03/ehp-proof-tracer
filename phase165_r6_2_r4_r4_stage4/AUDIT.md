# R4-4 第4段階

- 変更対象: `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` に共通 Provider 1件を接続。
- 追加: `phase165_r6_2_r4_r4_stage4_binding.py` の `verified_exactness_from_bridge()` と `build_exactness_binding_provider()`。
- 既存数学規則・命題台帳・証明ステップ・群別 Adapter は変更しない。
- 対象テスト: `test_install.py`, `test_integration.py`, `tests/test_map_property_rules.py`, `tests/test_phase165_r8_rule_provider.py`。
- 完了条件: 引用された固定型付き完全性に限り、隣接写像を具体化した候補が得られる。未結合の場合は拒否し、Forward 検証可能。
- 境界: すべての EHP 文献を型付け・登録する作業、`KernelZeroStatement` 等の前提証明、実群の証明全体、全体 pytest は含まない。
