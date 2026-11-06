# Phase 174 R3-R7-R11: Canonical Family Diagnostic Audit

This package rechecks audit-only `nu_6` / `eta_9` / `eta_10` expressions against the **registered, source-screened** stable-family metadata. It **does not** identify different generator symbols as equal or produce a mathematical proof.

## Usage

Extract `R11.zip` in the `ehp_proof` repository root. On the `develop` branch, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r11_canonical_fixture_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r11_canonical_fixture_audit\run.ps1"
```

The source guard accepts the reviewed `23979feec6685446a48d392fce3f2f1a55e85fe8` HEAD, or **one** descendant commit changing files only inside the preceding R10 audit package, provided all 14 pinned source blobs still match. No other unrelated successor is accepted. Local and remote `develop` heads must match. Staged and tracked changes are rejected.

The certified R10 full-audit report is required at `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r10\cited_family_gap.json`.

The live audit report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r11\canonical_fixture_audit.json`. DryRun records only preflight status. Full pytest is not run.

## Trust boundary

The Toda source transcription is not independently checked against its printed edition. Database rows are only goal/typing metadata. A candidate is not a certified inference. Source-first screening, First Successful Proof Search and the common proof renderer remain unchanged. No `GIVEN`, production inference rule, Web route or proof claim is installed.
