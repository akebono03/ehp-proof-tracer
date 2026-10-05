Phase157-R3 - pi_6^3 fixed-statement Reference boundary
========================================================

Purpose
-------
Connect the Phase157-R2 Literature Statement Boundary to the current
pi_6^3 generic Narrative route only.

Production changes
------------------
1. toda_group_proof_narrative_references.py
   - import Phase157-R2 boundary API
   - add _phase157_r3_is_pi6_3_root()
   - add filter_phase157_r3_pi6_3_reference_entries()
   - update select_toda_group_proof_narrative_reference_statement_steps()
     so pi_6^3 selects FIXED_STATEMENT candidates only

2. toda_group_proof_narrative_contribution_renderer.py
   - import filter_phase157_r3_pi6_3_reference_entries
   - apply it immediately after building Reference entries and before
     Reference statement lines are selected/rendered

Tests
-----
New:
- tests/test_phase157_r3_pi6_3_reference_boundary.py

Focused regression only:
- tests/test_phase157_r2_literature_statement_boundary.py
- tests/test_phase157_r3_pi6_3_reference_boundary.py
- tests/test_phase153_r5_reference_selection.py
- tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py

Expected pi_6^3 Reference boundary
----------------------------------
- (5.3): fixed nu-prime membership/double facts actually needed
- Proposition 5.6: pi_5^2 only; target pi_6^3 and later components excluded
- Proposition 5.3: pi_5^3 fixed group fact; H-surjective is proof body
- Proposition 5.1: pi_6^5 as n=5 specialization of the fixed higher eta family

The existing concrete pi_6^5 ProofStep currently attributed to Lemma 5.4 is
used only as the concrete presentation of the Proposition 5.1 fixed family
specialization. This does not mutate its underlying proof provenance.

Phase boundary
--------------
- No representative-group expansion yet (Phase157-R4).
- No 112-group cross-audit yet (Phase157-R5).
- No repository-wide pytest yet (Phase157 closure only).
