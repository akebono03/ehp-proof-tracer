Phase 155-R3-2F — verification repair and closure

Changes
-------
Existing tests only:

1. tests/test_phase143_1_generic_proof_order.py
   - test_phase143_1_generic_order_has_no_pi6_specific_hardcoding

2. tests/test_phase143_1b_semantic_proof_order.py
   - test_phase143_1b_generic_order_has_no_pi6_specific_hardcoding

The stale whole-module forbidden substring `"pi6"` is removed.

The remaining guards are retained:
- `(6, 3)`
- `nu_prime`
- `ν′`
- `Proposition 5.6`

This allows legitimate statement field access such as
`statement.pi6_4_group_relation` while continuing to reject the historical
group/generator/reference-specific hardcoding that Phase 143 intended to
prevent.

Closure verification
--------------------
The R3-2F audit re-runs every unique candidate base test referenced by the
332 R3-1 candidate pairs.

Runtime pytest node IDs such as:

`file.py::test_name[param]`

are normalized and aggregated under:

`file.py::test_name`

A base test passes only when:
- it collects,
- there is no setup/teardown failure,
- every call instance passes.

R3-2 is closed only when:
- focused pytest exit code is 0,
- all candidate base tests pass,
- final `needs_review` pair count is 0.

Boundary
--------
- production code changes: none
- existing test files changed: 2
- existing test functions changed: 2
- tests deleted: 0
- repository-wide pytest: not run

R3-3 is responsible for actual verified duplicate consolidation.
