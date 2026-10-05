Phase 158-R5-5 closure repair1
===============================

Purpose
-------

Remove stale R5-5a defect-detection expectations from the R5-5 closure
verification path.

The historical R5-5a tests intentionally asserted that:

- pi_7^4 had OUT_OF_ORDER_DERIVATION
- pi_15^8 had OUT_OF_ORDER_DERIVATION

Those assertions described the pre-R5-5b defect state.  After R5-5b repaired
generic ordering, those expectations became stale for closure verification.

Boundary
--------

This package does NOT edit or delete the historical R5-5a test file.

The historical tests remain as phase artifacts recording what R5-5a detected.

The closure path instead verifies the current contract:

- the R5-5a normalization contract still works;
- Web Narrative remains depth=2;
- pi_7^4 has no OUT_OF_ORDER_DERIVATION;
- pi_15^8 has no OUT_OF_ORDER_DERIVATION;
- R5-5b generic-order and Web verification tests still pass;
- the 112-coordinate closure cross-check still passes.

Files
-----

- audit_phase158_r5_5_closure.py
- test_phase158_r5_5_closure_repair1.py
- run_phase158_r5_5_closure_repair1.ps1
- README.txt

Production code changes: none.
Existing R5-5a test changes: none.
Repository-wide pytest: not run.

Completion condition
--------------------

PASS requires:

- current-contract closure tests: PASS
- R5-5b focused tests: PASS
- rendered: 112
- exceptions: 0
- wrong Web mode/depth: 0
- connector findings: 0
- root/QED findings: 0
- R5-5 CLOSURE RESULT: PASS

The repository-wide pytest remains reserved for the end of Phase 158.
