Phase 164 R7-R1 test contract repair
変更対象: tests/test_phase164_r7_statement_resolution.py のみ
・make_bridge: 同一文献 source_id を設定
・ProofStep: 必須 premises=() を指定
Production API、数学的内容、引用の fail-closed 制約は変更しません。
全体 pytest は実行しません。
