# Phase 155 Closure-R3-R3 changed code

## Changed repository files

- `tests/test_phase144_6_pi6_generic_production_route.py`
- `tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py`

## Top-level import changes

None.

## Deleted test

`test_phase144_6_pi6_production_branch_contains_no_legacy_renderer_call`

The behavioral test
`test_phase144_6_public_pi6_3_does_not_call_legacy_special_renderer`
remains and directly verifies the intended route contract.

## Updated depth-2 tests

The narrative and CLI tests still require:
- the nu-prime definition;
- the defining relation where applicable;
- the final pi_6^3 group result.

They no longer freeze the Phase144-era requirement that pi_5^3 must be absent
from the Reference section. Reference relevance/minimal-display policy belongs
to Phase156.
