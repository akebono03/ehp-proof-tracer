# Phase 173 R4-R1: Toda (5.6) Read-Only Dependency Audit

This package checks the reviewed Git source identity and inspects the existing mathematical rules for the direct-sum target `pi_7^4`. It does not install rules, create GIVEN statements, infer a completed proof, run a full test suite, or change tracked files.

Unzip the archive in the root of `ehp_proof` on Windows. Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_audit_only\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_audit_only\run.ps1'
```

The report is saved at `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r4_r1_audit_only\audit.json`. The script accepts the reviewed R3 baseline and the current reviewed `develop` when no production sources changed. It does not automatically fetch, merge, reset, checkout, or remove untracked audit directories. A dry run verifies source identity and the static rule inventory; the full audit additionally probes the public root proposals without promoting them to a proof.
