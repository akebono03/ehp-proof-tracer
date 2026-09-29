Phase 148 RC2-4 Repair R5
Two-group exactness exposure-path audit

Why this audit exists
---------------------
The post-R4.2 six-group audit found exactly one visible raw exactness phrase
in each of:
- pi_10^4
- pi_12^5

The other four representative groups passed that invariant.

This package does not change production code. It reverse-traces each
TodaProp42ExactnessStatement in the bounded depth=2 + semantic-closure
presentation and reports:
- whether the exact statement is visible in the final Web Narrative,
- block index and block role,
- Argument evidence ownership,
- RC2 exposure classification,
- supporting/conclusion ownership,
- surrounding final Narrative text.

GitHub develop inspection
-------------------------
Re-inspected before creating this audit:
- toda_group_proof_narrative_renderer.py
- toda_group_proof_generic_narrative_renderer.py
- toda_group_proof_narrative_argument_body_renderer.py
- toda_group_proof_narrative_argument_multi_renderer.py
- toda_group_proof_narrative_exactness_contribution_ownership.py
- toda_group_proof_narrative_exactness_display_contributions.py
- toda_group_proof_narrative_method_evidence.py
- tests/test_phase148_rc2_4_repair_r1_exposure_path_audit.py
- tests/test_phase148_rc2_4_repair_r2.py

Production changes
------------------
None.

Repository-wide pytest
----------------------
Not run.

Phase boundary
--------------
Do not weaken the six-group invariant.
Do not change Narrative ordering.
Do not add group-specific suppression.
Use this trace to select the next minimal general RC2 exposure repair.
