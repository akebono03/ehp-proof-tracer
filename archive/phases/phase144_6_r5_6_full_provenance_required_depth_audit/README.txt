Phase 144-6-R5-6
==================

Audit only. No production code, tests, or project documents are modified.

Question
--------
Can full recursive proof provenance determine the Narrative-required replay depth
before rendering a truncated replay?

Method
------
For each of the six representative groups:

1. Extract the full recursive proof provenance.
2. Use its maximum shortest_depth only to construct a complete audit presentation.
3. Build Narrative blocks and Arguments.
4. Apply the R5-5 Argument-boundary compression rule.
5. Find the root-reachable Argument set in the complete graph.
6. Predict required depth as the maximum shortest_depth of those Argument conclusions.
7. Rebuild truncated presentations from depth 0 through full depth.
8. Find the first depth whose compressed root-required Argument signature equals
   the full-graph signature.
9. Compare the predicted depth with the observed first matching depth.

Representative groups
---------------------
pi_6^3
pi_8^5
pi_10^4
pi_12^5
pi_15^8
pi_16^9

Interpretation
--------------
If all predictions match, full provenance can precompute a candidate Narrative
depth from root-required Argument conclusions.

If a prediction fails, supporting blocks or another semantic completeness condition
must be included; do not implement the depth policy yet.

No pytest is run because this package changes no production or test files.
