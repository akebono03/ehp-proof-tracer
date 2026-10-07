
Phase 159 pi_4^3 repair2g fix7

Purpose
-------
1. Complete the missing fixed-statement mapping for the already-existing
   Toda (5.1) component sphere_connectivity_zero.
2. Audit the late Reference usage filter without changing it.

Changed production file
-----------------------
toda_literature_statement_boundary.py

Added mapping
-------------
Toda (5.1) sphere connectivity zero
  -> (5.1) / sphere_connectivity_zero / FIXED_STATEMENT

No other production behavior is changed.

Audit
-----
During the actual pi_4^3 public Narrative render, the audit prints:

- Reference entries before fixed-boundary filtering,
- Reference entries after fixed-boundary filtering,
- used_step_ids presented to the no-marker step-usage filter,
- per-reference used flags,
- Reference entries after step-usage filtering,
- final public Narrative.

This determines whether the empty public Reference section is caused by
the generic no-marker step-usage filter.

Boundary
--------
EHP exactness remains proof-internal and is not made a Reference.
No n/k-specific public renderer hard-code is added.
Repository-wide pytest is not run.
