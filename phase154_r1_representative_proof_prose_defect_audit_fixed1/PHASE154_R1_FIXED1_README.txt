Phase 154-R1 — Representative proof prose defect audit — Fixed1

修正理由
--------
初版の実行スクリプトが、Phase 153-R8 以後に supersede（置換）された
Phase 153-R3 の期待値を baseline test に含めていた。

確認した具体例:
- 旧: 「また、[R2]を用いる。」
- 現行 Phase 153-R8: 「[R2]を用いる。」

したがって production code は変更せず、
R1 実行前の focused baseline tests だけを現行 Phase 153 契約へ差し替える。

production code の変更
----------------------
なし。

変更ファイル
------------
- run_phase154_r1_representative_proof_prose_defect_audit_fixed1.ps1
- PHASE154_R1_FIXED1_README.txt

監査コード
----------
audit_phase154_r1_representative_proof_prose_defects.py は初版と同内容。

実行する focused pytest
-----------------------
- tests/test_phase144_6_public_route_cutover.py
- tests/test_phase153_r7_proof_body_relevance.py
- tests/test_phase153_r8_reference_use_prose_normalization.py
- tests/test_phase153_closure_repair_r13.py

全体テストは実行しない。

完了条件
--------
1. focused current-baseline tests が PASS
2. 代表5群の Narrative が生成される
3. phase154_r1_defect_report.md / .json が生成される
4. production code に変更がない

次 Phase との境界
-----------------
R1 は監査のみ。
R2 で監査結果から最も根本的な defect category を1つだけ選び、
全群に効く一般規則として修正する。
Test Suite Consolidation には触れない。
