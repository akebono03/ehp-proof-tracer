# Phase 176 R3R19 — Cyclic Structure Frontier Audit

This read-only package inspects the unresolved cyclic-structure child of the group goal for pi_8(S^3). It compares the ordinary shared backward provider with two existing, independently sourced routes: finite cardinality plus full generator order, and an injective Hopf generator lift.

No production code, mathematical rules, group GIVEN statements, or established proofs are changed. No claim of a completed group proof is made. The root target is never admitted as a proof premise.

Run from the repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r19_cyclic_structure_frontier\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r19_cyclic_structure_frontier\run.ps1
```

The audit report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r19_cyclic_structure_frontier\report.json`. The focused tests use pytest importlib mode with cache disabled. Full pytest is not run.
