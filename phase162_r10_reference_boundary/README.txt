Phase 162 R10: verified (5.3) Hopf citation boundary

Apply runs only if both expected functions and two Hopf assignments are present.
It backs up the Web integration source before modifying it.
Adds phase162_reference_boundary.py without replacing existing modules.
This implementation does not alter the common renderer or any existing proof rule.

IMPORTANT: Existing legacy prose may continue to contain Lemma 5.2; that is a
separate Web connection concern. This R10 package proves the boundary's effect
on the final group ProofStep graph, not an end-to-end prose cleanup.

Limitations: this package checks that the citation component is registered,
that the formal conclusion matches the independently derived witness, and that
its pre-collapse ancestry validates. It does not mechanically prove that
Toda's printed (5.3) implies the statement: the source catalog is trusted.

Run from repository root:
  powershell -ExecutionPolicy Bypass -File .\phase162_r10_reference_boundary\run.ps1

Focused tests only. No full pytest until phase closure.
