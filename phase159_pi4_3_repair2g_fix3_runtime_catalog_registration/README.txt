Phase 159 pi_4^3 repair2g fix3

Purpose
-------
Fix the remaining runtime catalog registration defect for Toda (5.1).

Observed failure
----------------
get_toda_fixed_statement_component(
  "(5.1)",
  "basic_sphere_group_relations",
)
still raised KeyError after fix2.

Root cause
----------
The previous fix attempted to edit the literal
_FIXED_COMPONENTS_BY_REFERENCE dictionary body.
In the cumulative local state, that did not affect the active runtime catalog.

Fix
---
Register the already-defined _EQUATION_51_COMPONENTS explicitly after
_FIXED_COMPONENTS_BY_REFERENCE is created:

_FIXED_COMPONENTS_BY_REFERENCE[
  "(5.1)"
] = _EQUATION_51_COMPONENTS

This happens before _TRACKED_REFERENCE_LOCATORS is constructed.

Scope
-----
Production change:
- toda_literature_statement_boundary.py only.

No test files are changed by fix3.
No EHP exactness reference metadata is added.
No pi_4^3 n/k renderer hard-code is added.
No repository-wide pytest is run.
