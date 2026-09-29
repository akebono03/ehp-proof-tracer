Phase 144-6-R5-7
==================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-6 showed that full provenance can precompute the replay depth needed to
reproduce a chosen full Argument signature. It also showed that the current
compressed root closure becomes far too large for several representative groups.

R5-7 therefore audits Narrative-required Argument selection.

Question
--------
Does a compressed Argument dependency correspond to a Narrative-required
subproof when the dependency path touches the parent's current R4 visible
Narrative frontier?

Method
------
For each of the six representative groups:

1. Build the full provenance presentation.
2. Build blocks and Arguments.
3. Apply R5-5 Argument-boundary compression.
4. Compute the full root-reachable Argument closure.
5. For every compressed edge into that closure, inspect its block path.
6. Reuse the existing R4 frontier policy to determine whether the intermediate
   non-Argument path contains steps that remain visible in the parent Narrative.
7. Print each reachable Argument with:
   - role
   - conclusion depth
   - purpose subject
   - conclusion statement types
   - incoming compressed edge count
   - frontier-contact incoming edge count
   - whether it is directly reached from the root
   - path length and block roles for each incoming edge

No selection rule is implemented in this package.

Representative groups
---------------------
pi_6^3
pi_8^5
pi_10^4
pi_12^5
pi_15^8
pi_16^9

Next decision
-------------
If frontier contact separates benchmark-required Arguments from deep internal
Arguments, it becomes a candidate generic selection signal.

If not, R5-8 should audit stronger semantic signals rather than changing
production code.
