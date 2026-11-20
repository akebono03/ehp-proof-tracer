# Phase 176 R3R13 Two-Boundary Audit

This is a read-only inspection of two independent boundaries: the cited Toda Lemma 5.7 expansion and the right-composition zero-image transport expansion. It does not modify production code, add GIVEN statements, or assert a completed proof of the group structure.

From the repository root after extraction:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r13_two_boundary_audit\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r13_two_boundary_audit\run.ps1
```

The R3R10 audit report must exist under `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r10_right_zero_transport_isolated\report.json`. The script checks source anchors and the ancestor commit, compares ordinary shared proposals against an isolated citation wrapper, and tests the isolated right-composition proposal. A dynamically observed absence of a provider is not in itself a statement about all potential mathematical proofs.

Reports are written outside the repository to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r13_two_boundary_audit\report.json`. Pytest runs in a focused scope with its cache provider disabled; full pytest is not run.
