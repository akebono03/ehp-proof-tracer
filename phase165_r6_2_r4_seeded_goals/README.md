# Phase 165 R6-2 R4

型付きの結論パターンを持つ共通規則について、文献 Registry の固定された `GIVEN` 命題で未束縛変数を確定し、未証明の前提を `GoalExpansion` として生成する。未証明の前提を `GIVEN` として登録しない。

## 変更

- 追加：`phase165_r6_2_r4_seeded_goals.py`、`generate_seeded_backward_goals()`。
- 変更：`phase165_r52_r9_shared_math.py` の `shared_expansion_provider()`。
- テスト：`test_r624.py` の4件。

**制約：** 結論パターンを持たない旧 Toda 専用規則は依然として逆向きに適用できない。この変更だけでは `expand_existing_pi43_rules()` を撤去できず、$\pi_4^3$ の全証明完成も確認していない。

全体 pytest は Phase 165 の最後に限る。
