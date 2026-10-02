Phase 155 Closure-R4-R2 — audit reclassification + final closure

Final audit-only boundary
-------------------------
KEEP, with current-contract updates:
1. Phase153 all-group public Reference structural audit.
2. Phase97 representative cross-layer provenance audit.

REMOVE from Phase155 closure:
1. Phase144 completion invariant audit — historical renderer-shape audit.
2. Phase144 source-shape generic-renderer audit — obsolete because current
   renderer legitimately uses structured inference_rule metadata.
3. Phase153 exact Reference/body duplicate population audit — observed 117
   duplicates and deferred them to Phase156 Reference relevance/minimal display.

Expected final collection
-------------------------
10384 total
10382 routine
2 audit-only

Routine Closure-R3 PASS evidence remains valid because only audit-only functions
are deleted/updated.

Documentation is updated only after the final two explicit audits PASS.
No production code changes.
No monolithic repository-wide pytest.
