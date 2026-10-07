Phase 159 R1-7c R4 exact-sequence subsequence suppression audit2

Purpose
-------
Diagnose why the strict-prefix suppression still removes the required pi_6^3
exactness sequence.

This audit prints exact-sequence paragraphs for pi_3^2 and pi_6^3:
- before merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows()
- after the merge helper

It then re-runs only the two focused regression files.

No production code changes.
No test code changes.
No full pytest.
