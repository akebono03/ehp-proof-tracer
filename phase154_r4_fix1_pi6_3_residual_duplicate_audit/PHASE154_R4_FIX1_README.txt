Phase 154-R4 Fix1 — pi6_3 residual duplicate audit

Purpose
-------
Inspect the two exact duplicate lines remaining in pi6_3 after Phase 154-R4.

Production changes
------------------
none

Files changed
-------------
none

New audit files in this package
-------------------------------
- audit_phase154_r4_fix1.py
- run_phase154_r4_fix1.ps1

What the audit records
----------------------
For every exact duplicate nonblank line in the public Narrative:

- duplicate text
- occurrence count
- line numbers
- previous nonblank line
- next nonblank line
- context-based audit classification

It also records the Narrative reason sidecar:

- reason kind
- rendered reason sentence
- conclusion statement type

This allows us to distinguish:

1. true semantic duplication from the same ownership path
2. identical prose used for different mathematical transitions
3. repeated transition connectors that are legitimate because targets differ

Related current tests reviewed before the audit
-----------------------------------------------
- tests/test_phase150_rc4_7b_production_repair.py
- tests/test_phase143_63a_r_exactness_repair.py

Current production renderer paths reviewed
------------------------------------------
- toda_group_proof_narrative_reason_renderer.py
- toda_group_proof_narrative_argument_multi_renderer.py
- toda_group_proof_narrative_argument_body_renderer.py

Baseline pytest executed
------------------------
- tests/test_phase154_r4_semantic_duplication_transition_refinement.py
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase150_rc4_7b_production_repair.py

Full suite
----------
not run; reserved for the end of Phase 154.

Completion conditions
---------------------
1. Baseline focused tests pass.
2. The exact two remaining duplicate texts are identified.
3. Each occurrence includes local context.
4. Reason-sidecar ownership information is recorded.
5. No production file is modified.

Next boundary
-------------
- If the duplicates are legitimate context-specific repeats: close R4 and proceed to R5.
- If they are true semantic duplicates from the same ownership path: implement only that upstream ownership/deduplication rule as R4 Fix2.
