# Phase 165 R6-2 R4-4 第2段階

対象は `map_property_rules.py` のみ。既存クラス・関数は変更せず、末尾へ `KernelZeroStatement`、`ImageWholeStatement`、`SurjectiveMapStatement` および2つの一般規則 factory を追加する。追加位置はファイル末尾。

規則は既存 R8 の命名規約 `_inference_rule` で自動収集され、R26 で逆向き候補を生成する。`GIVEN` の自動生成は行わない。**既存 `KernelStatement` の構造が零群に等しいことや `ImageStatement` が終域全体に等しいことを証明する橋渡しは今回未実装**。型付き前提を文献事実などから供給する検証が次段階に必要である。

対象 pytest は `test_install.py` と `test_integration.py` および既存 `tests/test_map_property_rules.py`、`tests/test_phase165_r8_rule_provider.py`。全体 pytest は行わない。
