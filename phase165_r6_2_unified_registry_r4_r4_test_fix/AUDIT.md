# Phase 165 R6-2 R4-4 テスト修正

`test_forward_builder_kept` の `ProofStep` コンストラクタに必須の `premises=()` を追加する。既存の数理規則は変更しない。既存の `test_r4_r4_integration.py` 全文を置換する。対象 pytest のみを実施し、全体 pytest は実施しない。
