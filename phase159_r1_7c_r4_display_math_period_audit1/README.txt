Phase 159 R1-7c R4 display-math period audit1

Purpose
-------
Audit the next unresolved public-display defect candidate:

  display-math equations without a trailing ASCII period.

The user previously requested a unified equation-period rule.

Scope
-----
Audit only.

The script renders current public Narrative output over:
  n=2..15
  k=0..7
  max_depth=2

This range is a reproducible audit sample only and is not a permanent
group-count contract.

For every \[ ... \] display-math block, the script checks the last non-empty
math line. If that line does not end with ".", the block is printed.

Summary fields:
- rendered outputs
- render failures
- total display blocks
- affected outputs
- missing-period display blocks

Production code changes: none.
Test code changes: none.
No full pytest.
