Phase 155-R3-2E — parameterized failure decomposition

Purpose
-------
Freshly execute only the unique base tests that R3-2D classified as
`parameterized with failure`.

Why a fresh run is necessary
----------------------------
R3-2 wrote one synthetic base-level row with outcome `missing` whenever an
exact lookup such as:

`tests/test_x.py::test_a`

did not match actual pytest parameterized node IDs such as:

`tests/test_x.py::test_a[value]`

The actual parameterized call-phase records were not written into that
base-level execution CSV.

R3-2D combined the saved synthetic `missing` row with fresh collection data.
That was sufficient to prove a node-ID mismatch, but not sufficient to prove
a real test failure.

R3-2E removes the ambiguity by capturing, in one fresh focused pytest run:
- collected node IDs,
- setup reports,
- call reports,
- teardown reports,
- exact outcomes for every parameterized instance.

Root-cause classes
------------------
- all_parameterized_instances_pass
- parameterized_instance_failure
- setup_or_teardown_failure
- not_collected
- collected_without_call_report
- unresolved

Boundary
--------
- production changes: none
- existing-test changes: none
- deleted tests: none
- repository-wide pytest: not run

Only the unique base tests referenced by R3-2D are executed.
