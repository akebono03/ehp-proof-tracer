# Phase 175 R4R12R13R4 — Explicit zero-Hopf inference in shared search

This package connects two **generic**, typed backward-inference rules to the existing shared search:

1. A proved injective Delta map and cited H–Delta exactness imply that the corresponding Hopf map is the zero homomorphism.
2. A proved zero Hopf map and cited E–H exactness imply that the suspension map is surjective.

The new intermediate proof goal is a **zero map**, not the false assertion that the Hopf codomain group vanishes. The R13R3 conditional Delta-injectivity provider and older, independent search alternatives remain unchanged. The two new rule connectors require every premise to be independently proved by the regular source-first recursive search.

Run `run.ps1 -DryRun`, then `run.ps1` from the repository root. Both runs execute only the focused tests. The installer saves the full updated `shared_expansion_provider` function to `output/shared_expansion_provider_FULL.py`. This package does not run the full test suite, create a new literature GIVEN, or certify the target group. The remaining Delta injectivity source/type mismatch, if any, will be reported as an open frontier.

## R13R4R1 test collection correction

The focused test runner uses `pytest --import-mode=importlib` to prevent module-name collisions between R13R2 and R13R4 `tests/test_rule.py` files. This changes neither mathematical inference rules nor production integration. DryRun and execution still invoke the same focused tests.
