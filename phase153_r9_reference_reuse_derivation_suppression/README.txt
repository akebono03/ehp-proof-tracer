Phase 153-R9
============

Theme
-----
Reference reuse / derivation suppression
(既存参照結果の再利用・再導出抑制)

General rule
------------
A Reference step becomes a reusable proof boundary only when that exact step
is selected as a displayed statement in the Reference section.

When such a selected Reference step has premises:
- use [Rk] directly;
- do not recursively expand its ancestry in the proof body;
- keep the Proof graph unchanged.

This avoids using title-only Reference entries as reusable statement
boundaries.

Changed production files
------------------------
1. toda_group_proof_narrative_contribution_renderer.py
   Added:
   build_toda_group_proof_narrative_reference_reuse_marker_by_step_id()

2. toda_group_proof_narrative_renderer.py
   Import added:
   build_toda_group_proof_narrative_reference_reuse_marker_by_step_id

   Modified:
   _append_narrative_for_step()

Expected pi_6^2 proof-body effect
--------------------------------
Keep:
[R2]を用いる。
[R3]を用いる。
final pi_6^2 conclusion.

Suppress the re-derivation through:
pi_{i-1}^1 = 0
[R4]
gamma -> eta_2 gamma
Toda (5.2) derivation sentence.

Out of scope
------------
- removing title-only [R1];
- Reference numbering;
- generic-route argument assembly;
- Phase 154 semantic-classification defects.

Full pytest remains deferred until Phase 153 closes.
