Phase 148 RC2-4 Repair R4.1 — Numbered-equation dependency audit

Purpose
-------
Audit why pi_6^3 numbered calculation equations disappear after the R4
Web Narrative depth-parity repair.

Production changes
------------------
None.

Existing production tests changed
---------------------------------
None.

Audit targets
-------------
EQ1:
2 nu' = eta_3 E eta_3 eta_5

EQ2:
eta_3 E eta_3 eta_5 = eta_3^3

EQ3:
2 nu' = eta_3^3

The audit compares:
- depth=2 replay;
- depth=2 + current semantic closure;
- depth=3 replay;
- depth=3 + current semantic closure;
- complete replay.

For each numbered-equation ProofStep it reports:
- shortest depth;
- proof role;
- inference rule;
- presence before and after semantic closure;
- block location;
- Argument ownership;
- incoming/outgoing proof dependency edges;
- final Narrative visibility.

Why this audit is needed
------------------------
R3 proved that complete replay causes the Web depth=2 Narrative to process
177 nodes / max depth 10 and expose 15 raw exactness statements.

R4 correctly removed that hidden complete-replay substitution, but focused
tests showed that numbered equations (1)-(3) were also lost.

The current semantic closure implementation was inspected on GitHub develop.
It adds only explicitly registered semantic prerequisites, currently centered
on the definition-introduction path. It is not a general calculation-
dependency closure.

R4.1 determines the exact missing dependency frontier before any R4.2
production repair is designed.

Phase boundary
--------------
No production repair.
No exactness policy change.
No contribution-layer cleanup.
No Narrative ordering change.
No repository-wide pytest.
