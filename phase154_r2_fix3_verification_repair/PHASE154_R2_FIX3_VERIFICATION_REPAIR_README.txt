Phase 154-R2 Fix3 — Verification Repair

Production changes
------------------
none

Reason
------
The previous Fix3 runner included:
  tests/test_phase153_r3_11_reference_body_ownership_repair.py

That file contains an expectation superseded by Phase 153-R8.

R3.11 expects:
  この結果として、[R2]を得る。

Phase 153-R8 explicitly requires reference-derived prose to be normalized to:
  [R2]を用いる。

Therefore the R3.11 expectation is not a valid current-contract baseline for Phase 154-R2.

Current-contract focused baseline
---------------------------------
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase153_r7_proof_body_relevance.py
- tests/test_phase153_r8_reference_use_prose_normalization.py
- tests/test_phase153_closure_repair_r13.py

Completion conditions
---------------------
1. All current-contract focused tests pass.
2. pi_11^4 contains:
     まず、[R2]を用いる。
3. pi_11^4 does not contain:
     まず、[R2]
   as an incomplete line.
4. Previous R2 repairs remain:
   - no source theorem metadata sentence
   - no \text{ is injective}
   - no \text{ is exact}
   - no である.を用いる。
5. Full suite is not run until Phase 154 end.

Next boundary
-------------
If this verification passes, Phase 154-R2 is complete.
Proceed to Phase 154-R3 cross-group re-audit.
