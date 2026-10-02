Phase 155-R3-2D — missing execution record audit

Purpose
-------
Investigate the six `missing_execution_record` pairs identified by
Phase 155-R3-2C-r1.

The audit compares:
1. the unparameterized candidate test ID,
2. saved R3-2 execution node IDs, and
3. fresh `pytest --collect-only` node IDs.

This determines whether an apparent missing result is caused by pytest
parameterization such as:

`tests/test_x.py::test_a`

becoming:

`tests/test_x.py::test_a[value]`

Root-cause classes
------------------
- parameterized_nodeid_all_pass
- parameterized_nodeid_has_failure
- collected_but_not_recorded
- nonparameterized_execution_match
- not_collected
- unresolved

Boundary
--------
- production changes: none
- existing-test changes: none
- deleted tests: none
- repository-wide pytest: not run

Only the missing candidate tests are collected with `--collect-only`.
