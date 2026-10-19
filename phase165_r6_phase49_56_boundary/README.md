# Phase 165 R6 — Phase 49/56 Boundary Audit

This package preserves legacy tests and production files. It checks that the current registered-goal and Web routes do not import historical Phase 49/56 probes. It also inventories six historical test files for subsequent mathematical-coverage review.

Run `run.ps1` from the extracted project folder. The audit report is written under `phase165_r6_audit_results/phase49_56_boundary/report.json`.

**Limit:** Three new boundary tests do not establish that the mathematical inferences formerly tested by Phase 49/56 are equivalently covered. No legacy tests are retired by this package. Full pytest is not run.
