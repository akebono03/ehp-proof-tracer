Phase 144-6-R5-15M-R2
=======================

Audit replay-depth fix only.

R1 result
---------
The focused test set passed:

17 passed

Therefore the 15M production prototype and its focused regression tests are
already passing.

R1 audit failure
----------------
The audit script still contained one remaining call:

build_toda_group_result_proof_replay(
  group_result,
  max_depth=None,
)

The current replay API requires max_depth to be an int.

R2 fix
------
Only audit_phase144_6_r5_15m.py is logically corrected.

It now:
1. extracts the recursive proof provenance,
2. computes max(node.shortest_depth),
3. passes that integer as max_depth.

This is the same full-provenance-depth method already used successfully by
the R1 focused tests.

Production boundary
-------------------
No production prototype logic is changed.
No existing project production file is changed beyond what 15M already adds.
No renderer, CLI, Web, R4 visibility, ProofStep, InferenceRule, or
TodaProofEdge behavior is changed.
No full pytest is run because Phase 144 is still in progress.
