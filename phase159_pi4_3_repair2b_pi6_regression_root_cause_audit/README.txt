Phase 159 — pi_4^3 repair 2b
pi_6^3 regression root-cause audit
===================================

Context
-------
The broad repair2 was rolled back, but pi_6^3 still fails existing Narrative
contracts:
- the "(4) と (5) より" transition is missing;
- Proposition 4.4 is missing from structured References.

Therefore the regression predates repair2 and is likely related to repair1b/1c
changing the Proposition 5.1 provenance used by the Prop56 bootstrap.

This package changes no production code and no existing tests.

Audit
-----
A. Current _build_prop51_step() premises and literature references.
B. pi_6^3 structured Reference entries.
C. pi_6^3 Narrative transition graph and rendered connectors.
D. pi_6^3 block inventory with literature references.

Boundary
--------
No repair is applied here.
Repository-wide pytest is not run.
