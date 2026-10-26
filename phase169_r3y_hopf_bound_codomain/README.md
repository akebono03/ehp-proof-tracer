# Phase 169 R3Y — Source-bound Hopf codomain proof

Use a provenance-scoped proof obligation for the Hopf codomain while retaining the unchanged canonical ambiguity check for ordinary proof goals. The mathematical inference rules are not changed. The source-bound obligation must resolve to a real verified `ProofStep` whose conclusion is the original typed relation.

The installer uses AST checks, backs up the five repository files it changes, runs only focused pytest and a live Proof Tree audit, and restores changes upon failure. Full pytest is deferred until the end of Phase 169.
