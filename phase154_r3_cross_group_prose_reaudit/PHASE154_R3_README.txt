Phase 154-R3 — Cross-group Prose Re-audit

Purpose
-------
Re-audit the representative public Narrative output after Phase 154-R2.

Production changes
------------------
none

Representative groups
---------------------
Primary:
- pi6_3
- pi10_4
- pi11_4

Secondary:
- pi12_5
- pi16_9

Conditions
----------
- public Narrative
- depth 2
- same current local production state after Phase 154-R2 Fix3

Audit categories
----------------
1. internal_fallback
   Known raw rule-name / English / source-metadata leakage.
   Any finding is an R2 regression candidate.

2. bare_reference_marker
   Incomplete [R#] sentence.
   Any finding is an R2 regression candidate.

3. transition_repetition
   Repeated or locally contradictory transition leads.
   Candidate for Phase 154-R4.

4. semantic_duplication
   Repeated identical public prose or known aggregate repetition.
   Candidate for Phase 154-R4.

5. reference_body_linkage_candidate
   Bare "[R#]を用いる。" style sentences.
   A hit is not automatically a defect; it is a candidate for Phase 154-R5.

6. punctuation
   Lines ending in "." or malformed mixed punctuation.
   Candidate for Phase 154-R6.

Generated output
----------------
audit_output/phase154_r3_summary.md
audit_output/pi6_3.md
audit_output/pi10_4.md
audit_output/pi11_4.md
audit_output/pi12_5.md
audit_output/pi16_9.md

Focused verification before audit
---------------------------------
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase153_r7_proof_body_relevance.py
- tests/test_phase153_r8_reference_use_prose_normalization.py
- tests/test_phase153_closure_repair_r13.py

Full test suite
---------------
not run; reserved for the end of Phase 154.

Completion conditions
---------------------
1. R2 current-contract baseline passes.
2. All five representative Narratives are generated at depth 2.
3. Summary and per-group reports are written.
4. Remaining defect categories can be assigned to R4/R5/R6.
5. No production file is modified.

Next boundary
-------------
R3 is audit only.
Use the resulting report to choose exactly one upstream category for R4.
