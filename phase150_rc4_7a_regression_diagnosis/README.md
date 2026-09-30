# Phase 150 RC4-7A Regression Diagnosis

Audit-only package.

It diagnoses two regressions that remain after the RC4-7B-1 experiment was
confirmed reverted:

1. Phase 148: pi_10^4 and pi_12^5 lost the one semantically selected visible
   exactness phrase.
2. Phase 143: the low-level multi-Argument renderer now prepends a Reference
   section before the single pi_15^8 Argument.

The audit reports, for every TodaProp42ExactnessStatement in pi_10^4 and
pi_12^5:

- whether the step is a leaf in the Narrative dependency traversal,
- whether RC4-7A assigns it a LiteratureReference,
- the assigned [R#] marker,
- whether the exactness statement itself remains visible,
- whether the [R#] marker is visible instead.

No production files or existing tests are changed.
The repository-wide test suite is intentionally not run.
