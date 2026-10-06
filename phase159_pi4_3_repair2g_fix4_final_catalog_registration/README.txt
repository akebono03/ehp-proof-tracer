Phase 159 pi_4^3 repair2g fix4

Purpose
-------
Complete the active runtime registration of Toda (5.1).

Observed failure
----------------
fix3 still raised:

KeyError:
  unknown fixed statement component:
  (5.1) / basic_sphere_group_relations

Diagnosis
---------
In the cumulative local source, earlier registration points can be followed
by later construction or mutation of the reference catalog.

Fix
---
Insert the (5.1) registration immediately before:

_TRACKED_REFERENCE_LOCATORS = frozenset(
  _FIXED_COMPONENTS_BY_REFERENCE
)

This is the final active catalog boundary before the tracked locator set is
constructed.

Inserted block
--------------
_FIXED_COMPONENTS_BY_REFERENCE[
  "(5.1)"
] = _EQUATION_51_COMPONENTS

_TRACKED_REFERENCE_LOCATORS = frozenset(
  _FIXED_COMPONENTS_BY_REFERENCE
)

Scope
-----
Changed production file:
- toda_literature_statement_boundary.py

Changed classes:
- none

Changed functions:
- none

Changed tests:
- none in fix4

No EHP exactness literature metadata is added.
No pi_4^3 n/k renderer hard-code is added.
No repository-wide pytest is run.
