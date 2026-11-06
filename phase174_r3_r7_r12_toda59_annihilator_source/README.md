# Phase 174 R3-R7-R12 — Source-qualified general annihilator

This package isolates the **general family relation** in Toda equation (5.9):
`nu_n ∘ eta_{n+3} = 0` for `n >= 6`. It does not install the statement in the
public source registry or add any new group result as a `GIVEN` assertion.

The generic inference candidate requires an **independently certified cited
source leaf**. It cannot derive a zero relation from a database generator name,
a symmetric equality, a hand-written symbol alias, or a mere TeX quotation.

## Run in Windows PowerShell

Extract `R12.zip` directly into the root of `akebono03/ehp-proof-tracer` at a
reviewed `develop` HEAD. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r12_toda59_annihilator_source\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R12 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r12_toda59_annihilator_source\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R12 audit failed" }
```

The script runs only focused pytest groups, then checks current remote/local
HEAD lineage and source blobs, the certified R11 JSON report, the adopted Toda
text, and the unproved typed inference proposal. The final report is placed in
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r12\toda59_annihilator.json`.

A successful isolation audit is **not** a completed proof of `pi_12^7 = 0`.
Only the final Phase 174 closeout may run the entire pytest suite.
