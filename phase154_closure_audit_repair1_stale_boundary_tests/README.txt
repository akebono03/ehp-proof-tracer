Phase 154 Closure Audit Repair1 — stale boundary tests

初回 closure audit:
- Phase 154 focused regression: 44 passed
- ordering / reason boundary: 49 passed, 8 failed

失敗分類:
1. Phase 149 punctuation expectation 1件
   `より、` -> `より, `

2. Phase 150 visible reason count 5件
   Phase 154-R4 の current contract:
   同一 FINAL_RESULT_DERIVATION prose は public Narrative で1回だけ表示。

3. Phase 150 generic reason vocabulary punctuation 2件
   `、` -> `, `

production 変更:
- なし

変更する tests:
- tests/test_phase149_rc3_3_minimal_ordering.py
- tests/test_phase150_rc4_5_visible_reasons.py
- tests/test_phase150_rc4_7d_generic_reason_vocabulary.py

実行後:
- 元の phase154_closure_audit を最初から再実行
- full test suite はまだ実行しない
