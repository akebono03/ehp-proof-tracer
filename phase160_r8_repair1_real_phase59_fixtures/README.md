# Phase 160-R8 Repair 1

Repair only the new Phase 160-R8 focused test.

The initial R8 test created synthetic `pi_4^2`, `pi_5^3`, and `pi_6^4` proof steps with matching conclusions but without the real Phase 59 provenance structure. The Proposition 5.3 integration path is provenance-sensitive, so those synthetic fixtures were not an adequate reproduction of the production branch.

This repair reuses the actual Phase 59 fixtures:

- `build_phase59_4_data()` for `pi_4^2` and `pi_5^3`
- `build_phase59_6_data()` for `pi_6^4`

It then calls the production `_build_higher_eta_transport()` and verifies that:

1. the transport rule is `Toda 4.5 generic finite-cyclic transport`;
2. the transported generator remains `E^(n-4)(eta_4 eta_5)` internally;
3. the existing Proposition 5.3 bridge normalizes it to the internal composition representing `eta_n^2`;
4. the normalized group depends directly on the generic transport step.

No production code is changed. Public Narrative is not changed in this repair. No full test suite is run.
