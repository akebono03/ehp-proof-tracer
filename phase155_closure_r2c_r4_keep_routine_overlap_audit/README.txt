Phase 155 Closure-R2C-R4 — KEEP_ROUTINE_CANDIDATE overlap / redundancy audit

Purpose
-------
Statically review the exact 14 KEEP_ROUTINE_CANDIDATE nodeids from R2C-R1.

No repository test body is executed and no repository file is changed.

Classifications
---------------
KEEP
  A distinct current contract at a public/rendering boundary.

MERGE_CANDIDATE
  The invariant is useful, but another test repeats the same expensive
  population/integration traversal. Preserve the invariant in one merged test.

DELETE_CANDIDATE
  The same contract is already covered by a later/current lightweight or
  layer-specific test.

Expected result
---------------
KEEP: 3
MERGE_CANDIDATE: 5
DELETE_CANDIDATE: 6

R2C-R5 should perform actual merge/delete changes only after this audit passes.
