# Phase 160-R5

Connect the existing `k=1` production stable-transport path to the generic finite-cyclic transport introduced in Phase 160-R4.

Scope:

- Modify only `_build_prop51_step()` usage in `toda_prop56_zero_bootstrap.py`.
- Replace the `pi_4^3`-specific transport rule call with the generic finite-cyclic transport rule.
- Keep the existing eta-family bridge and final eta normalization unchanged.
- Keep the old `pi_4^3`-specific transport rule available for compatibility and existing tests.
- Add a focused provenance test proving that Proposition 5.1 now uses the generic transport rule.
- Do not change public Narrative.
- Do not migrate other stems yet.
- Do not run the full test suite.
