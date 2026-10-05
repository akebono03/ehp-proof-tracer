Phase157-R20 repair51 — Residual display defect audit

Purpose
-------
Extend the 112-group audit after repair50 classification.

repair50 established that:
- the 18 missing-proof-section findings are output-route shape differences,
  not render failures;
- all affected outputs still contain a body and QED;
- pi_4^3 visibly contains a reflexive equality eta_3 = eta_3;
- pi_15^8 needs a direct check for isolated sentence fragments.

Production code changes
-----------------------
None.

pytest
------
Not run.

Scope
-----
- n = 2..15
- k = 0..7
- 112 groups
- replay depth = 2

Checks
------
1. Render exceptions.
2. Visible reflexive equality Relation steps:
   conclusion.lhs == conclusion.rhs.
3. Isolated sentence-fragment paragraphs:
   - である.
   - を得る.
   - を用いる.
   - となる.
4. Root statement repeated more than once in the public proof body.

Interpretation
--------------
This audit deliberately separates old no-reference route formatting from
actual semantic/prose defects.

Only findings confirmed here should become production repair52.

Output
------
- audit_output/findings.csv
- audit_output/exceptions.csv
- audit_output/report.txt
