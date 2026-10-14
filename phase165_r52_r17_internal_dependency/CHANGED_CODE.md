# R17 変更内容

- 新規 `phase165_r52_r17_internal_dependency.py`: `CompletedInternalProof`, `same_statement`, `validate_ancestry`, `find_reusable_internal_proof`, `depends_on`。
- 変更 `phase165_r3_recursive_search.py`: `reconstruct_registered_goal` に `completed_internal_proofs` を追加し、サブゴールの内部証明を探索候補として再利用。
- 変更 `phase165_r52_r2_search_adapter.py`: `search_registered_partial_proof` を通して同引数を伝播。
- 変更 `phase165_r52_r9_shared_math.py`: `search_shared_group_goal` を通して同引数を伝播。
- 新規 `test_phase165_r52_r17_internal_dependency.py`: 6つのテスト関数（import 全文は同ファイルに記載）。
- 既存関数の全文は `install.py` が実際の導入済みコードに適用し、変更前バックアップを生成します。GitHub の基線と Windows の R16 適用後の内容に相違があるため、基線版による上書きはしません。
- 完了条件: 関連 targeted pytest がすべて PASS。内部証明の汎用 Registry 自動登録は次段階。
