# Phase 176 R3R15: Shared Extra-Provider Probe

This package verifies two existing, independently audited inference proposals
through the public `shared_expansion_provider(extra_providers=...)` API, without
changing or registering any production provider.

The cited Toda Lemma 5.7 clause is first screened for source provenance. The
source-bearing rule proposes the base zero-suspension goal. A separately
validated generic right-composition transport proposes the base goal from the
longer composition-zero goal. No proved step or source GIVEN is injected by the
provider itself; ordinary recursive proof search remains responsible for
resolving every premise.

Run from the repository root in PowerShell after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase176_r3r15_shared_extra_provider_probe\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase176_r3r15_shared_extra_provider_probe\run.ps1"
```

The report is stored under `%LOCALAPPDATA%\EHPProofTracerAudit`.
No full test suite is run. A PASS does **not** certify completion of the
homotopy-group presentation or make these providers globally available.
