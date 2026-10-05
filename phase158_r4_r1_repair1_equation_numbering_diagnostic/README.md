# Phase 158-R4-R1 repair1 — equation numbering diagnostic

This package is diagnostic-only.

It addresses the fact that the existing Phase 144.5 focused equation-numbering
tests currently fail before the Phase 158-R4 finding classification can run.

The package:

1. runs the existing focused test file but does not stop on its failure;
2. prints the current `pi_6^3` multi-argument Narrative;
3. reports duplicate visible equation tags;
4. reports distinct ProofStep objects that render to the same equation text;
5. classifies all 11 findings from the first Phase 158-R4 audit.

No production code is changed.
No existing test is changed.
Full pytest is not run.
