Phase 155-R3-3D — post-removal closure audit

Purpose
-------
Close Phase 155 R3 after the verified duplicate removals and the three stale
expectation repairs.

R3-3D changes no production code and no tests.

Closure checks
--------------
1. All 161 R3-3B-approved deletion test IDs are absent.
2. All 5 whole-file deletion targets are absent.
3. Every R3-3A graph survivor base test ID still exists.
4. Every test ID participating in an R3-2F-r1 `historical_keep` pair still
   exists.
5. No original `removable_duplicate` pair still has both endpoints present.
6. No `needs_review` pair reappears.
7. No `tests/test_*.py` file contains duplicate top-level `test_*` function
   names.
8. Remaining affected test files complete focused pytest collection.

Inventory note
--------------
R1/R2 observed a historical 843-vs-842 test-file inventory discrepancy.
R3-3D therefore records the current file/function inventory but does not use
the historical raw inventory count as a completion condition.

Candidate-universe note
-----------------------
R3-3D closes the R3-1 candidate universe rather than launching a new global
duplicate discovery pass.

Deleting tests cannot create a new pair of duplicate test bodies. The relevant
closure question is whether the previously proven 164 removable pairs have
been broken while survivors and historical compatibility tests remain.

A later Phase 155 collection/runtime audit remains separate.

Boundary
--------
- production changes: none
- existing-test changes: none
- additional deletions: none
- repository-wide pytest: not run

If all closure conditions pass, Phase 155 R3 duplicate/superseded cleanup is
complete.
