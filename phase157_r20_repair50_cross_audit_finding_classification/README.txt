Phase157-R20 repair50 — Cross-audit finding classification

Purpose
-------
Classify the 20 findings reported by repair49.

repair49 result
---------------
- scanned groups: 112
- exceptions: 0
- review groups: 19
- total findings: 20
- exact_duplicate_paragraph: 2
- missing_proof_section: 18

This audit does not assume all 20 findings are defects.

Checks
------
For each affected group:
- re-render the public Narrative at depth 2;
- print the repair49 findings;
- classify the missing-proof-section shape;
- print first and last non-empty lines;
- preserve exact duplicate details.

Primary question
----------------
Are the 18 missing-proof-section findings:
- genuine renderer regressions;
- or legitimate reference-only/direct-result/stable/trivial outputs?

Secondary question
------------------
Which groups own the two exact duplicate paragraphs, and what text is
duplicated?

Production code changes
-----------------------
None.

pytest
------
Not run.

Output
------
- audit_output/classification.csv
- audit_output/report.txt

Next step
---------
Only confirmed defects should become repair51. Legitimate no-proof-section
outputs should instead be excluded from the repair49 invariant in the closure
audit.
