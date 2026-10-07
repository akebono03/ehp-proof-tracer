# Phase 160-R6

Connect the production seven-stem sigma branch to the Phase 160 generic finite-cyclic transport while separating sigma-family generator normalization.

Scope:

- Add `toda_stable_generator_normalization.py`.
- Add a sigma-specific normalization inference rule.
- Replace the combined sigma_9 finite-cyclic transport rule in `toda_prop515_upper_bootstrap.py` with:
  1. the existing Toda (4.5) isomorphism rule,
  2. the Phase 160 generic finite-cyclic transport rule,
  3. the new sigma generator-normalization rule.
- Preserve the final symbolic result `pi_(n+7)^n = Z/16{sigma_n}`.
- Keep the old combined sigma_9 rule available for compatibility and historical focused tests.
- Do not modify public Narrative.
- Do not migrate other group structures.
- Do not run the full test suite.
