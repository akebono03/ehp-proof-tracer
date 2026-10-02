# GitHub baseline — Phase 155-R3-3C-r1

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

GitHub was re-inspected after the first R3-3C failure.

Confirmed source defect in:

`tests/test_phase109_14_decorated_sigma_finite_cyclic_fallback.py`

The function:

`test_phase109_14_sigma7_stable_specialization_boundary_remains_unsupported`

is defined twice at top level with the same body.

This explains the first R3-3C failure:
- R3-3B used set-based top-level test-name existence and correctly found the
  pytest test ID.
- R3-3C expected exactly one AST FunctionDef and rejected the duplicate
  source definitions.

R3-3C-r1 therefore treats one approved pytest test ID as potentially mapping
to one-or-more same-name top-level source definitions and removes all matching
definitions.

The already-proven R3-3A/R3-3B safety decisions are unchanged.
