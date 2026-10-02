Phase 155 Closure-R2B-R2 — assertion-level redundancy audit

Purpose
-------
Review the 9 SUPERSEDED_CANDIDATE Phase144 failures before deleting anything.

This step is static only:
- no heavy Phase144 test execution;
- no repository test execution;
- no repository file modification;
- no deletion.

Classification
--------------
FULLY_COVERED
  A later current-contract test directly covers the old assertion.

OBSOLETE_HISTORICAL
  The assertion describes historical audit scaffolding/design exploration or a
  contract superseded semantically by the final participating/DETACHED model.

UNIQUE_CURRENT_INVARIANT
  The assertion still protects current behavior not present in
  audit_phase144_6_r5_43_11d.completion_invariants_pass.

UNKNOWN
  No safe reviewed mapping exists; R2B-R2 fails rather than guessing.

Important finding encoded in the audit
--------------------------------------
The old 43_11 duplicate/order invariant and conclusion-placement invariant are
not part of 43_11d completion_invariants_pass. They must not be silently deleted.
