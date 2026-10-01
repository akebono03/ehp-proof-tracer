Phase 153-R12
=============

Theme
-----
Root Reference exclusion across routes
(全 Narrative 経路での root 参照除外)

Problem
-------
Marker-bearing Narrative routes could still list the same LiteratureReference
as the theorem currently being proved. pi_11^4 exposed this as:

[R1] Proposition 5.15

even though the group proof itself has Toda Proposition 5.15 as its root
provenance.

General rule
------------
Reference-entry construction remains unchanged as structural proof data.

At Narrative display boundaries:
1. determine the LiteratureReference of presentation.root_step;
2. remove entries with the same LiteratureReference;
3. renumber the remaining entries contiguously;
4. remap statement-line dictionaries before any [Rk] marker map is built.

Changed production files
------------------------
toda_group_proof_narrative_references.py
toda_group_proof_narrative_contribution_renderer.py
toda_group_proof_narrative_renderer.py

New test
--------
tests/test_phase153_r12_root_reference_exclusion.py

Completion example
------------------
For pi_11^4 at depth 2:
- Proposition 5.15 does not appear as an external Reference;
- Proposition 5.8 becomes R1;
- Proposition 4.4 becomes R2;
- the proof body uses the renumbered external References.

Boundary
--------
This Phase does not fix prose ordering such as repeated "まず" or other
Narrative wording defects.

Punctuation normalization remains deferred.
The requested final prose style is "," and ".".

Full pytest remains deferred until the end of Phase 153.
