Phase 144-6-R5-15N
====================

Typed contribution x Narrative relevance coverage audit.

Files
-----
- audit_phase144_6_r5_15n.py
- run_phase144_6_r5_15n.ps1
- README.txt

Production changes
------------------
None.

Test changes
------------
None.

Document changes
----------------
None.

Purpose
-------
15M showed that 5117 / 9416 premise edges can be assigned a typed evidence
contribution using generic semantic information, while 4299 remain UNRESOLVED.

15N does not try to raise that global percentage.

Instead, it overlays the 15M contribution metadata with the current production
R4 argument-local visibility policy and measures:

- VISIBLE x resolved contribution
- VISIBLE x UNRESOLVED
- HIDDEN x resolved contribution
- HIDDEN x UNRESOLVED
- OUTSIDE_LOCAL_BODY

The primary metric is:

visible_resolution_ratio
  = visible_resolved_edges / visible_edges

The most important inventory is:

VISIBLE x UNRESOLVED

Those are edges that current production Narrative exposes but the 15M typed
metadata still cannot explain. They are the candidate population for the next
semantic extension.

Boundary
--------
The audit reuses the production R4 frontier-hidden-step helper. It does not
modify visibility.

No n/k-specific classification is used.
No inference-rule-name parsing is used.
Statement type names are printed only as an unresolved inventory and are not
used to classify edges.

The full test suite is not run because Phase 144 is still in progress.
