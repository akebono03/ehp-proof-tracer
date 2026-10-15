# Phase 165 Renderer R4-R3 Heading Regression Repair

Correct one remaining outdated compatibility-test assertion: the current partial Narrative heading is `## 証明`, not the historic `証明（Proof`. No proof semantics or presentation output changes are made. This package reuses the scoped R4 import migration and updates the same reviewed test within the guarded install.

Run `run.ps1` from an extracted directory under the project root. The installer uses a separate `.phase165_renderer_r4_fast_r3_backup` and restores on targeted test or exact Narrative mismatch. Full pytest is not run.
