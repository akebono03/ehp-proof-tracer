# Phase 178 R20R1 — Suspension isomorphism bridge (public wiring)

This package exposes the previously tested R20 bridge without changing its rule or adding GIVEN statements. It appends the proposal after the existing candidate ordering and before the existing root gate. It also updates the single R20 test that previously required absence of the public bridge.

Run `run.ps1 -DryRun` first, then `run.ps1`. The installer requires the reviewed develop commit and exact relevant Git blobs, rejects unrelated tracked changes, exports complete proposed modules and the complete changed function to the audit directory, and restores its own changes on a failed gate. It does not commit or push.

Focused tests include the R20, R19, R19R1, R20F1 classifier, and R17R3 renderer tests. The six historical R4C tests are executed separately; only the exact already documented missing-ancestry assertion is permitted to remain open. A separate test replays the currently selected historical proof through the existing trust boundary. The failure is not counted as a pass.

The real public search is observed for n=2 through n=6, k=6. Four previously complete groups must remain verified; the n=6 search must actually reach the typed and generic isomorphism, injectivity and Delta-zero obligations. Surjectivity visits are reported, not required when the first unresolved premise stops the branch. No Delta-zero inference or display changes are introduced. Full pytest is not run.
