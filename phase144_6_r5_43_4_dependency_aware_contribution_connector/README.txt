Phase 144-6-R5-43-4 dependency-aware contribution connector

Production change:
- toda_group_proof_narrative_contribution_renderer.py

Rule added:
- Add "これより、" only when two consecutive ordered contributions have
  a direct Proof graph edge from the first contribution to the second.
- Do not infer a connector from visual adjacency.
- Do not convert transitive reachability into a direct prose claim.

For pi_6^3, the R5-43-3 audit predicts exactly one connector:
C4 -> C5.

Not changed:
- R5-42 selection, ownership, ordering, and placement.
- transitive contribution prose.
- mathematical statement rendering.
- public renderer route.
- full test suite.
