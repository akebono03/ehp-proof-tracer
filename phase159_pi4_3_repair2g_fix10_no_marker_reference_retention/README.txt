
Phase 159 pi_4^3 repair2g fix10

Purpose
-------
Remove the local cumulative no-marker Reference clearing that contradicts
the already-existing generic no-marker step-usage Reference filter.

Confirmed failure mechanism
---------------------------
Before the faulty block:

- R1 (5.1) survives fixed-boundary filtering.
- R2 Proposition 5.1 survives fixed-boundary filtering.
- Both Reference entries have selected statement lines.
- All four fixed source steps are used.
- Both Reference entries survive the no-marker step-usage filter.

The local renderer then executed:

  if "[R" not in rendered:
    reference_entries = ()
    statement_lines_by_reference_number = {}

This unconditionally discarded the already-validated Reference entries.

Changed file
------------
toda_group_proof_narrative_contribution_renderer.py

Changed function
----------------
render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Change
------
Delete only the unconditional no-marker clearing block.

Preserved behavior
------------------
- fixed-statement boundary filtering
- root Reference exclusion
- no-marker step-usage filtering
- body-usage filtering
- prune_toda_group_proof_narrative_root_zero_direct_premise_references()
- EHP exactness remains excluded from public Reference
- no n/k-specific renderer branch is added

Tests
-----
Focused Phase159 repair2g tests.
Repair1 / repair1c health checks.
pi_3^2 Narrative regression.

Repository-wide pytest is not run.

Full function
-------------
The apply script writes the complete patched function to:

  patched_render_function_after_apply.py.txt

inside this extracted package directory.
