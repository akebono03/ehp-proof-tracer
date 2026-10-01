Phase 153-R11
=============

Theme
-----
Generic-route Reference attribution / filtering
(一般経路の参照対応付け・絞り込み)

General rule
------------
For generic routes:

1. Follow the same NarrativeArgument ordering as the generic renderer.
2. Ignore DETACHED arguments.
3. Collect ProofStep identities from each remaining argument's local body.
4. Add ProofStep identities from ordered contributions selected for insertion.
5. Keep only Reference entries containing one of those used ProofSteps.
6. Exclude the LiteratureReference of the current root theorem itself.
7. Renumber retained Reference entries contiguously.

The Proof graph is not changed.

Expected pi_6^3 effect
----------------------
Toda Proposition 5.6 is the theorem currently being proved and must not appear
as an external Reference in the "使用する結果" section.

External References structurally used by the proof remain.

Boundary
--------
Punctuation normalization is not part of R11.
The requested rule is retained for a later prose-formatting step:
use "," and "." consistently instead of "、" and "。".

Full pytest remains deferred until the end of Phase 153.
