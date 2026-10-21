# Phase 166 R3-AF 変更内容

変更対象:
- `phase165_r55_nk_only_goal.py`: 末尾の `registered_group_goal_candidates()` 全体を変更。既存文献候補を優先し、空の場合のみ既存 CSV 由来候補を追加。
- 新規 `phase166_r3af_goal_adapter.py`: `_generator_for_target()` と `database_group_goal_candidates()` を追加。
- 新規 `phase166_r3af_goal_source/tests/test_r3af.py`: テスト3件。

**制限**: `SphereRepository` にある位数・生成元は証明対象のみ。文献引用、推論、完成証明とはみなさない。対応済みの単純な安定生成元の表記のみ変換。複合式 のような複雑な生成元や未対応群は fail-closed とする。既存命題台帳、ProofStep、Toda (4.5)、renderer は変更しない。掲載位置は捏造しないため、証明探索が COMPLETE になるとは限らない。

実行 pytest: `python -m pytest -q phase166_r3af_goal_source/tests/test_r3af.py`。
完了条件: 既存の2・3-stem安定基点について証明目標を構築でき、証明根拠として使用しないこと。
次 Phase: DB 由来目標の掲載順境界選択および複雑な生成元表現の型付け。
全体 pytest は Phase 166 最終時のみ。
