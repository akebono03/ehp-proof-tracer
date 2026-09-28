# Phase 144-6 R25-8 — Production Repair

## Changed files

- `toda_upstream_bootstrap.py`
  - `build_toda_53_nu_prime_steps()`
- `tests/test_phase144_6_r25_8_depth2_definition_provenance.py`
  - new focused regression tests

## Production change

`build_toda_53_nu_prime_steps()` already constructs the mathematical
definition provenance

`nu' in {eta_3, 2 iota_4, eta_4}_1`

as `bracket_membership_step`.

Before R25-8 that step was reachable only through the bracket-specialization
step, so it first appeared at recursive proof depth 3. The public CLI
`group-proof 3 3 --depth 2 --mode narrative` therefore could not build the
definition Argument.

R25-8 preserves the existing inferred membership conclusion and rule but
rebuilds the returned membership `ProofStep` with the already-existing bracket
membership as an additional direct provenance premise.

No new mathematical statement is invented. In particular,
`TodaNuFamilyDefinitionStatement` is not used for `nu'`; that statement belongs
to the `nu_n = E^(n-4) nu_4` family for n >= 4.

## Expected effect

At depth 2 the generic Narrative pipeline can now see the same definition
frontier that it already sees at depth 3. Existing generic suppression rules
should consequently:

- restore the `nu'` definition Argument;
- preserve the bracket-membership definition evidence;
- suppress the internal `pi_5^3` supporting group fact.

There is no `pi_6^3`-specific renderer change and no `pi_5^3` text hardcoding.

## Test boundary

The runner executes only focused regression tests. The full suite is
intentionally deferred until the end of Phase 144-6.
