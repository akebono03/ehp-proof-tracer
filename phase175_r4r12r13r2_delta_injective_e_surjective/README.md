# Phase 175 R4R12R13R2 — Isolated Delta Injectivity and EHP Surjectivity

This package adds **two isolated, conditional, generic inference rules**. It does not modify production files, connect the public proof provider, add a literature GIVEN, or assert that the target group has a complete proof.

The first rule infers injectivity of a Delta map from a proved free-cyclic source presentation, a proved direct-sum target presentation with one free summand and one finite cyclic summand, and a proved signed image of the source generator with nonzero free coefficient.

The second rule infers surjectivity of a suspension map from independently proved injectivity of the matching Delta map and both consecutive EHP exactness windows.

The target example is the map from pi_8^4 to pi_9^5. The cited Toda (5.8) formula remains a separate ordinary proof goal.

Run `run.ps1 -DryRun` and `run.ps1` from the extracted repository root. Both invocations run only focused tests. No full pytest suite is run.
