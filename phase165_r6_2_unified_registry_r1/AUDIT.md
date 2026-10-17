# Phase 165 R6-2 統一規則登録 R1

## 現行コード確認

2026-10-16 GitHub の `rule_catalog.py`、`phase165_r8_rule_provider.py`、`phase165_r57_r26_generic_search_connection.py`、`phase165_r6_2_r4_seeded_goals.py`、`phase165_r52_r9_shared_math.py` および R8 関連テストを参照。ユーザー環境では専用 pi4^3 Adapter の削除が報告済みであり、インストーラーは旧 import があれば停止する。

## 変更対象

- 新規 `phase165_r6_2_unified_registry_r1/unified_backward_rule_registry.py`：`RegisteredBackwardRule`、`UnifiedBackwardRuleRegistry`、`build_unified_backward_rule_registry()`。
- 新規 `install.py`：`transform()`、`main()`。
- 変更 `phase165_r52_r9_shared_math.py`：import に統一台帳入口を追加。`shared_expansion_provider()` 内にある3つの重複規則収集を単一スナップショットへ統合する。既存関数の他の部分は保持。
- 新規 `test_registry.py`、`run.ps1`、`README.md`、本監査記録。

## 境界

R1 は R8 の55件相当の収集を統一する最小接続段階である。引数必須 factory 22件や他 Provider 群を自動登録するものではない。登録は証明可能性・数学的健全性の証明ではない。次段階で factory の明示入力解決、ほかの Provider の一般化、実際の Goal 到達性を検査する。全体 pytest は Phase 末尾のみ。
