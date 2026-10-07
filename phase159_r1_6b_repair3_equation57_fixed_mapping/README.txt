Phase 159-R1-6b repair3

Cause
-----
The Phase157-R5-R3 diagnostic found exactly one mismatch:

- locator: Equation 5.7
- rule: Toda Equation 5.7 nu-prime eta_6 Hopf value
- expected: fixed_statement / nu_prime_eta6_hopf_relation
- actual: proof_internal / None

The fixed component already exists in the catalog. The missing pieces are the
rule-name mappings.

Changes
-------
toda_literature_statement_boundary.py only:

_FIXED_RULE_COMPONENT_KEYS:
  "Toda Equation 5.7 nu-prime eta_6 Hopf value"
  -> "nu_prime_eta6_hopf_relation"

_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME:
  "Toda Equation 5.7 nu-prime eta_6 Hopf value"
  -> "Equation 5.7"

Tests
-----
No test changes.

Full pytest
-----------
Not run.
