Phase 153-R10
=============

Theme
-----
Used Reference filtering
(使用参照の絞り込み)

General rule
------------
After the final proof body is produced, keep only Reference entries whose
[Rk] marker actually appears in that body.

Then:
- renumber retained References contiguously from R1;
- remap statement-line metadata to the new numbers;
- remap body markers to the same new numbers;
- leave the Proof graph unchanged.

Expected pi_6^2 result
----------------------
Reference section:
[R1] Proposition 5.6.
[R2] (5.2).

Removed:
Lemma 5.7.
Proposition 4.4.

Proof body:
first use [R1], then [R2], then conclude pi_6^2.

Changed production files
------------------------
toda_group_proof_narrative_references.py
toda_group_proof_narrative_contribution_renderer.py
toda_group_proof_narrative_renderer.py

Full pytest remains deferred until the end of Phase 153.
