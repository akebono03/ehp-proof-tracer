Phase 159 — pi_4^3 repair 2e
pi_6^3 current-contract audit
================================

Purpose
-------
Earlier diagnostics established:
- Proposition 4.4 is not part of the later Phase 157 R19 public pi_6^3
  Reference contract.
- The current contract instead requires five public References:
  R1 Proposition 5.6
  R2 (5.3)
  R3 Proposition 5.3
  R4 Proposition 5.1
  R5 Proposition 2.2
- The current final output is missing R5 Proposition 2.2.
- The numbered "(4) と (5) より, " derivation is also missing.

This package runs the current repository tests that define those contracts.

No production code is changed.
No existing test is changed.
Repository-wide pytest is not run.

Interpretation
--------------
Phase157 reference failures:
  real current Reference regression.

Numbered derivation failures:
  real current numbered-derivation regression unless a later explicit
  replacement contract is found.

Phase159 repair1 failures:
  repair1 itself is no longer healthy and must be corrected first.
