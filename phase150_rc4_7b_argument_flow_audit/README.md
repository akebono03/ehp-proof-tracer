# Phase 150 RC4-7B Argument-Flow Audit

Audit-only package. It does not change production code or existing tests.

Targets:
- pi_10^4 (primary)
- pi_12^5
- pi_15^8
- pi_16^9

The audit traces:
ProofStep -> NarrativeBlock -> Argument ownership -> local body -> rendered Narrative.

It reports visible blocks that have no Argument owner, detached Argument boundaries,
reference/source-style text still visible in the final Narrative, and the complete
rendered output for each representative group.

Repository-wide tests are intentionally not run because Phase 150 is not yet closing.
