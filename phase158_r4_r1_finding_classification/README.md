# Phase 158-R4-R1 finding classification

This package classifies the 11 findings produced by the preceding Phase 158-R4 audit.

It does not modify production code or existing tests.

The classification distinguishes:

- confirmed equation linkage defects;
- confirmed unused equation-number candidates;
- prose-review findings;
- audit false positives.

Before classification it runs only the focused existing equation-numbering test file:

`tests/test_phase144_5_generic_definition_order_equations.py`

The full pytest suite is intentionally not run.
