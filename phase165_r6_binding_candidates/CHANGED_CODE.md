# Phase 165 R6 — 変更一覧

新規:
- `phase165_r6_binding_candidates.py`: `BindingCandidate`, `BindingInventory`, `inventory_typed_source_bindings` を追加。
- `tests/test_phase165_r6_binding_candidates.py`: 4件の対象テストと fixture 作成関数。
- `phase165_r6_binding_candidates/audit.py`: 既存 R5 Bridge の読み取り専用監査。
- `phase165_r6_binding_candidates/run.ps1`: 対象 pytest と監査の実行。

既存 API・既存コードには変更なし。既存文献の同じ番号だけでは数学的意味の一致を認めない。
完了条件: 候補・曖昧・未照合の3分類が出て、証明使用資格0件を維持。
R7 境界: 型付き対応の数学的承認、ProofStep link、推論カタログの投入は今回行わない。
