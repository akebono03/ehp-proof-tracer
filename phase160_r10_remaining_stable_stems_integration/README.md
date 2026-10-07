# Phase 160-R10

Integrate the remaining stable stems 3 through 6 into the Phase 160 generic stable transport architecture.

## Scope

- 3-stem:
  - keep the existing nu-family generator bridge;
  - replace only the theorem-specific group transport with the generic finite-cyclic transport.

- 4-stem and 5-stem:
  - add one generic Toda (4.5) zero-group transport rule;
  - use the same generic rule in both production paths.

- 6-stem:
  - use the generic finite-cyclic transport first;
  - add a separate nu-squared transported-generator normalization rule;
  - keep group transport and family normalization as separate proof steps.

- Public Narrative:
  - extend the existing stable wrapper to stems 3, 4, 5, and 6;
  - use `nu_n` for stem 3;
  - use zero-group prose for stems 4 and 5;
  - use canonical `nu_n^2` notation for stem 6;
  - preserve existing stems 1, 2, and 7.

## Canonical bases

- stem 3: `pi_8^5 = Z/8{nu_5}`
- stem 4: `pi_10^6 = 0`
- stem 5: `pi_12^7 = 0`
- stem 6: `pi_14^8 = Z/2{nu_8^2}`

No free-cyclic generic transport, direct-sum generic transport, generic stable database, or unrelated refactoring is added.

Only focused tests are run. The full test suite is reserved for Phase 160 closure.
