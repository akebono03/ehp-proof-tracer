Phase 158-R5-5c-2 — audit-harness invariant repair

Purpose
=======
Repair only the R5-5c equation-chain audit invariant after the R5-5c-1 finding classification.

Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.

Changed / added files
=====================
1. audit_phase158_r5_5c_2.py
   - revised current-corpus equation-chain audit
   - accepts an untagged visible mathematical target after a numbered connector
   - still requires every referenced source tag to appear before the connector
   - still requires a visible mathematical target immediately after the connector

2. test_phase158_r5_5c_2_audit_harness.py
   - accepts untagged visible target
   - accepts tagged visible target
   - rejects missing/late source tag
   - rejects non-mathematical target

3. run_phase158_r5_5c_2.ps1
   - runs only the lightweight harness tests and revised current-corpus audit

Revised generic invariant
=========================
A numbered connector is valid when:

1. every equation number it references has already appeared visibly;
2. the connector is immediately followed by a visible mathematical target;
3. the target itself is not required to have a number unless later proof text needs to reference it.

Therefore both forms are valid:

  (1) より,
  $A=B$

and

  (1) より,
  $A=B\tag{2}$

The second form is required only when equation (2) must be referenced later.

Audit corpus
============
The script scans n=2..15 and k=0..7 because that is the repository's current historical cross-audit corpus.
This is not a 112-group architectural contract. The invariant is generic and independent of the number of groups in the repository.

Output
======
audit_output/summary.txt
audit_output/groups.csv
audit_output/equation_chain_defects.csv
audit_output/exceptions.csv

Completion condition
====================
- lightweight harness tests pass;
- all coordinates render without exception;
- revised equation-chain defects = 0.

Phase boundary
==============
This phase does not change the production renderer or production ordering rules.
If the revised audit passes with zero defects, the five R5-5c findings are closed as audit-harness overconstraint / false positives.
Repository-wide pytest remains deferred until the end of Phase 158.
