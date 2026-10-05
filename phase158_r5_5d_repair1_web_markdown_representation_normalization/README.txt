Phase 158-R5-5d repair1
========================

Purpose
-------

Repair only the R5-5d audit harness representation matching.

The original R5-5d audit compared:

- generic renderer strings containing Markdown math delimiters, such as
  "$A=B$", and
- Web Narrative segment values where the parser has already removed "$".

That representation mismatch caused almost all generic steps and all root
targets to appear invisible to the audit harness.

This package does NOT modify production code.

Files
-----

- audit_phase158_r5_5d_repair1.py
- test_phase158_r5_5d_repair1.py
- run_phase158_r5_5d_repair1.ps1
- README.txt

Normalization boundary
----------------------

The audit-only canonicalizer:

1. removes Markdown "$" delimiters;
2. removes Markdown "**" strong delimiters;
3. removes display-only "\tag{N}" equation labels;
4. collapses whitespace.

It does NOT rewrite mathematical LaTeX, proof prose, Argument ownership,
renderer output, or production data.

Audit scope
-----------

Current historical audit corpus only:

  n = 2..15
  k = 0..7
  Web Narrative depth = 2

This is not an architectural group-count contract.

Completion interpretation
-------------------------

The key diagnostic from repair1 is whether visible Argument intervals recover
from the clearly-invalid previous value of 1 and whether the 112 target/QED
findings disappear.

Remaining findings must still be classified before any production repair.

Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.
