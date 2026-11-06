# Phase 174 R3-R7-R4 — Source-first Delta-surjectivity gap audit

This is a **read-only** audit of the still-unproved EHP Delta-surjectivity
premise, `Delta : pi_13^13 -> pi_11^6`, in Toda Proposition 5.9.

The R3-R7-R3 isolated generic zero-group root passed its focused tests,
but its Delta-surjectivity premise had zero candidate expansions. This audit
compares the different EHP chain

`pi_10^5 --E--> pi_11^6 --H--> pi_11^11 --Delta--> pi_9^5`

with the adopted Toda source transcription and the existing common typed
proof-search provider. It carefully distinguishes the **nonzero** group
`pi_10^5 = Z/2` from the assertion that its suspension map has **zero
image**. A generic rule requiring `pi_10^5 = 0` is not a valid shortcut.

## Installation and execution

Extract the ZIP under the repository root. The package creates the directory
`phase174_r3_r7_r4_delta_surjectivity_audit/`; no production files are
replaced. Run from the repository root using Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r4_delta_surjectivity_audit\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r4_delta_surjectivity_audit\run.ps1'
```

The runner uses only focused pytest and `--import-mode=prepend` to preserve
the validated project import behavior. It does not run the complete suite.

The read-only audit requires the R3-R7-R2 and R3-R7-R3 JSON reports in
`%LOCALAPPDATA%\EHPProofTracerAudit`. It checks pinned source blobs and one
of two reviewed develop HEADs (`ae537ca...` or `1f3a61d...`). A local HEAD
behind the reviewed remote is reported as requiring reconciliation before a
future implementation, not automatically changed.

The report is written to:

`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r4\delta_surjectivity_audit.json`

## Scope and status

The source's mathematical conclusions are **not** new GIVEN leaves or
proof steps. Registered database rows provide only goals, not evidence.
No production provider, proof tree, renderer, Web route, or common project
document is modified. The adopted transcription is checked, but the original
printed edition has not been independently verified by this audit.

Completion means that source guards, focused tests, and diagnostics pass. It
does **not** imply that Delta-surjectivity or the target zero group has been
proved. Future work must find non-circular typed proofs for the actual map
properties before introducing any new generic inference rule.
