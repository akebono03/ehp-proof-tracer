Phase157-R20 repair53-r2 — pi15 Proposition 4.4 reference loss audit

Purpose
-------
Locate the stage at which the public pi_15^8 Narrative loses the explicit
Toda Proposition 4.4 decomposition-isomorphism Reference.

Why this is not treated as a stale test
---------------------------------------
Unlike the earlier pi_8^5 historical label assertion, Proposition 4.4 is:
- explicitly emitted by the dedicated pi_15^8 renderer;
- explicitly preserved by Phase150 cross-group Reference tests;
- mathematically consumed by the generator-transport argument.

Therefore its disappearance is a production-regression candidate.

Audit stages
------------
1. Dedicated Phase134-24 raw renderer.
2. Graph-derived Reference entries.
3. Fixed-statement boundary filter.
4. Reference statement-line generation.
5. Body-usage filter.
6. Specialized public Reference connection.
7. Final public Narrative.

Production code changes
-----------------------
None.

pytest
------
Not run.

Next step
---------
Use the first stage where Proposition 4.4 disappears to decide the minimal
repair:
- boundary eligibility repair, or
- body-usage detection repair, or
- specialized public connection repair.

repair53 display-fragment normalization remains in place and is not changed by
this audit.
