# GitHub baseline — Phase 155-R6-R1

Repository: `akebono03/ehp-proof-tracer`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected:
- old Phase144 43_11 completion audit and its test,
- later Phase144 43_11d final completion audit and test,
- Phase150 pi16_9 Reference normalization test,
- Phase154 pi16_9 Narrative and representative re-audit.

Current contract:
- 43_11d distinguishes Narrative-participating contributions from DETACHED
  contributions. DETACHED contributions need not be inserted into Narrative.
- Phase154 pi16_9 visible References are Lemma 5.14, Theorem 3.6, Lemma 5.13.

Therefore the two R6 FAIL probes are stale test expectations.
Production behavior is not changed.
