Phase 148 RC2-4 Repair R3 — Web / unit rendering-path parity audit

Purpose
-------
Compare the actual Web Narrative path with the RC2 unit-test path for the same
pi_6^3 target.

Production changes
------------------
None.

Existing production-test changes
--------------------------------
None.

Audit-only test
---------------
tests/test_phase148_rc2_4_repair_r3_web_unit_parity_audit.py

GitHub develop inspection
-------------------------
The current Web adapter does the following for mode="narrative":

1. Build a depth-limited replay for visible metadata / trace steps.
2. Replace the presentation replay with
   build_complete_toda_group_result_proof_replay(group_result).
3. Build the presentation from that complete replay.
4. Call render_toda_group_proof_narrative_markdown().

For pi_6^3, the public Narrative renderer then:

1. applies semantic closure;
2. builds semantic sidecar;
3. builds blocks;
4. builds arguments;
5. calls
   render_toda_group_proof_narrative_multi_argument_with_contributions_markdown().

The RC2 unit helper used in the recent repair tests instead builds a depth=3
replay and directly calls
render_toda_group_proof_narrative_multi_argument_markdown().

Therefore this audit measures both differences independently:
- replay / graph depth;
- contribution-layer insertion.

Measured values
---------------
For depth=3 unit, depth=2+closure, and complete+closure:
- input replay node count;
- input max depth;
- post-closure node count;
- post-closure max depth;
- block count and role distribution;
- argument count;
- TodaProp42ExactnessStatement count.

For final Narrative variants:
- character count;
- visible exactness phrase count.

Renderer variants:
- direct multi_argument;
- multi_argument_with_contributions;
- public render_toda_group_proof_narrative_markdown;
- actual build_standard_web_group_proof_view(... depth=2, narrative).

No fix is made in R3.
No repository-wide pytest is run.
RC3 ordering remains out of scope.
