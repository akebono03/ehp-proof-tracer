# Phase 169 R10EE — One-stem regression audit

This package audits the current typed proof search against the historical Phase 168 frozen one-stem results. It performs **no production edits** and makes **no new mathematical inference**.

The historical Phase 168 closure reported complete proofs of pi_3^2 (18 ProofSteps), pi_4^3 (25 ProofSteps), and pi_5^4 (10 ProofSteps). A Phase 169 R10EC focused test observed pi_5^4 as `partial` with a diagnostic reporting two candidates. R10EE measures the present state rather than accepting either outcome unconditionally.

Run `run.ps1` from the extracted directory, while the repository remains on `develop`. The runner checks the Git commit ancestry and reviewed source blob identities, runs seven focused tests, audits three frozen one-stem cases and two controls, then verifies that tracked files were not changed. The JSON and Markdown reports are written to `output/`.

An audit may execute successfully while reporting `BLOCKED_ONE_STEM_REGRESSION`. That is deliberate. Incomplete proof search is never upgraded to a complete proof for display or closure purposes.

The suite-wide pytest is not run. Existing README.md and docs are not edited.

Even a matching status, step count, and trust result does not certify full-text or citation equality with the Phase 168 frozen narratives.
