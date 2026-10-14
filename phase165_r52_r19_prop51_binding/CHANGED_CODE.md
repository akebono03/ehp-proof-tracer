# R52-R19 変更一覧

- 新規 `phase165_r52_r19_prop51_binding.py`: `PROOF_PREREQUISITE_COMPONENTS`, `resolve_registered_proof_use_order`, `_component_key` を追加。
- 変更 `phase165_r52_r9_shared_math.py`: `search_shared_group_goal` 内で `proof_use_order="registered"` を R18 `ProofUseOrder` に変換する3行を追加。既存の R16/R17/R18 の処理は維持。
- 新規 `test_phase165_r52_r19_prop51_binding.py`: 5テスト。必要な import はファイル内に全文記載。
- 完了条件: 新規5件と R18/R9 回帰テスト PASS。
- 次の境界: `pi4^3` の別のターゲットへの自動依存登録や一般 `n` 特殊化は未実装。自動有効化せず opt-in とする。
