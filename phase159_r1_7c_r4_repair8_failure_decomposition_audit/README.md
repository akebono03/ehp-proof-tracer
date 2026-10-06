# Phase 159 R1-7c R4 repair8 failure decomposition audit

This package makes no production or test changes.

It renders the current public Narrative for representative target groups and
separates three kinds of failures:

1. prose expectations that may be stale after R4 normalization,
2. reflexive-equality regressions,
3. Reference/body-marker attribution regressions.

Outputs are written under `output/`.

The audit explicitly reports:

- Reference headers,
- body Reference markers,
- missing markers,
- reflexive `eta_5 = eta_5`,
- residual old R4 prose fragments,
- repeated numeric equality.

Repository-wide pytest is not run.
