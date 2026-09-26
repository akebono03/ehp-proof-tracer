Phase 143-75AP R9

Purpose:
Repair the two failures found by the canonical Phase 143 full regression.

Measured full-regression result before this repair:
- 9978 passed
- 2 failed

Both failures require the established transported-decomposition display:
pi_15^8 \cong Z/8{E sigma'} \oplus Z{sigma_8}

Cause:
The Phase 143-75AP semantic renderer used:
- "=" instead of the established "\cong" display contract;
- DirectSumGroup storage order directly, which rendered the two summands
  in the reverse order from the established narrative contract.

Production change:
- toda_proof_narrative_renderer.py
- render_toda_proof_statement_latex()
- only the Toda515Sigma8TransportedDecompositionStatement branch

No import changes.
No class changes.
No test changes.
No documentation changes.
No unrelated refactoring.

Focused pytest:
- tests/test_phase143_51a_r_provenance_semantic_catalog.py
- tests/test_phase143_51b_aggregate_statement_prose.py

After this focused check passes, rerun the canonical full suite:
pytest -q .\tests
