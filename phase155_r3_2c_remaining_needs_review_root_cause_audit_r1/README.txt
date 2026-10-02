Phase 155-R3-2C-r1 — corrected remaining needs-review root-cause audit

Correction
----------
The original R3-2C filtered only `other_review_reason`.

However, Phase 155-R3-2B printed:

`other needs review = source_evidence_issue + other_review_reason`

Therefore an output of zero from the original R3-2C did not mean the six
remaining pairs had disappeared; it meant they were in the
`source_evidence_issue` class.

R3-2C-r1 includes both:
- source_evidence_issue
- other_review_reason

It skips only the already-separated `failure_linked` class.

Boundary
--------
- production changes: none
- existing-test changes: none
- deleted tests: none
- repository-wide pytest: not run
