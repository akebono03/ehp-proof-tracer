# Phase 150 RC4-7A Regression Repair R1

This package repairs two regressions confirmed by the RC4-7A diagnosis.

1. A literature-reference marker must not replace the mathematical content of
   a selected exactness statement. The exactness statement remains in the
   proof body while its literature source remains available in the Reference
   section.
2. The low-level multi-Argument renderer keeps its pre-RC4-7A contract: it
   renders Argument prose only. Reference-section composition is moved to the
   higher contribution-rendering layer used by the public generic Narrative
   route.

No group-specific pi_10^4, pi_12^5, or pi_15^8 condition is introduced.
No RC4-7B Argument-flow behavior is changed.
No repository-wide test suite is run.
