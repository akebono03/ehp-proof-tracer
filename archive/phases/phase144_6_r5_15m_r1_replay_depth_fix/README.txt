Phase 144-6-R5-15M-R1
=======================

Replay-depth compatibility fix for the 15M prototype package.

Cause
-----
The original 15M test/audit helper passed max_depth=None to
build_toda_group_result_proof_replay(). The current API requires max_depth
to be a nonnegative int.

Fix
---
The test and audit helper now call
extract_toda_recursive_proof_provenance(group_result), compute the actual
maximum shortest_depth present in that provenance, and pass that integer to
build_toda_group_result_proof_replay().

This avoids inventing a fixed "full depth" such as 7, 20, or 32.

Production prototype
--------------------
toda_group_proof_narrative_evidence_contributions.py is unchanged from 15M.

No existing production file is modified.
No existing project document is modified.
R4 production visibility is unchanged.
The full test suite is not run because Phase 144 is still in progress.
