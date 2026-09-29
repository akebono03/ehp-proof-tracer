Phase 148 RC2-4
Post-repair six-group cross-group audit

Targets
-------
- pi_6^3
- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

GitHub develop inspection
-------------------------
Inspected before this audit:
- toda_group_proof_narrative_semantics.py
- web_group_proof.py
- toda_group_proof_narrative_exactness_exposure.py
- toda_group_proof_narrative_exactness_components.py
- toda_group_proof_narrative_argument_multi_renderer.py
- tests/test_phase148_rc2_4_cross_group_audit.py
- tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py
- tests/test_phase143_19_method_evidence.py

Audit source
------------
Unlike the older RC2-4 audit helper, this audit starts every case from the
same bounded replay used by Web Narrative:

max_depth=2
  -> presentation
  -> R4.2 semantic closure
  -> semantic sidecar
  -> blocks
  -> Arguments
  -> exactness method components/exposure
  -> Web Narrative

Checks
------
1. Semantic closure does not restore complete replay.
2. R4.2 calculation closure adds no exactness ProofStep.
3. Web Narrative contains no raw exactness phrase.
4. No sample develops AMBIGUOUS_RELEVANT exposure.
5. pi_6^3 retains numbered equations (1)-(3), connector, final group result,
   and the derived short exact sequence.

Production changes
------------------
None.

Existing production tests changed
---------------------------------
None.

Repository-wide pytest
----------------------
Not run. Full regression remains reserved for the end of Phase 148.

Next boundary
-------------
If this audit passes, proceed to RC2-5 final regression and documentation
closure. RC3 Narrative ordering remains outside Phase 148.
