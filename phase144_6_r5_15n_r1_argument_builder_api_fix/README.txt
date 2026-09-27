Phase 144-6-R5-15N-R1
=======================

Argument-builder API compatibility fix for the 15N audit.

Observed result
---------------
The 15M preflight passed:

5 passed

The 15N audit then failed before execution because it imported a non-existent
function:

extract_toda_group_proof_narrative_arguments

Current develop uses:

build_toda_group_proof_narrative_arguments(
  presentation,
  blocks,
  semantic_sidecar=semantic_sidecar,
)

R1 change
---------
Only the audit package is changed:
- audit_phase144_6_r5_15n.py uses the current argument-builder API.
- the runner performs an audit-module import preflight before executing the
  full audit.

Production changes
------------------
None.

Test changes
------------
None.

Project document changes
------------------------
None.

Phase boundary
--------------
R4 visibility, renderers, CLI, Web, ProofStep, InferenceRule, TodaProofEdge,
and the 15M contribution prototype are unchanged.

The full test suite is not run because Phase 144 is still in progress.
