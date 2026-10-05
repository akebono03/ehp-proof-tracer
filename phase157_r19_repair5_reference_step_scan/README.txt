Phase157-R19 repair5

Scope
-----
Replace only _phase157_r19_finalize_pi6_3_public_narrative().

Why repair4 still returned unchanged output
-------------------------------------------
The finalizer still depended on reference-entry discovery.  The public
Reference pipeline may remove a locator before the finalizer sees it, and
Equation 5.7 is not guaranteed to be emitted as a Reference entry at depth 2.

Repair5 removes that dependency:
- scans presentation.nodes / ProofStep directly;
- reads LiteratureReference locators from the actual proof steps;
- reconstructs Proposition 5.6, (5.3), Proposition 5.3 and Proposition 5.1;
- uses the actual Equation 5.7 proof step as the provenance carrier for the
  public Proposition 2.2 entry;
- then finalizes the canonical pi_6^3 body after all usage filtering.

No import changes.
No test-file changes.
No documentation changes.
No repository-wide pytest.
