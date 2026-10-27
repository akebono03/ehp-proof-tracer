# Phase 169 R4 — Read-only audit for π₆⁴

This package audits the current registered goal, actual backward proof search, screened citation context, Toda (4.5) range conditions, and suspension evidence for `n=4, k=2`. A baseline check for `n=3, k=2` is included. It creates **no** production-code patches or mathematical assertions. It writes only `output/audit.json` and `output/audit.md` inside its own directory.

The ZIP was based on GitHub `akebono03/ehp-proof-tracer` branch `develop`, HEAD `ff08b601badf339457ff524ca21847b5d6a67ef5`. The script warns about a changed local HEAD instead of silently assuming the same revision. Check local changes before interpreting results.

From the local repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r4_pi64_baseline_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r4_pi64_baseline_audit\run.ps1"
```

The runner executes **only** four new focused tests and the existing Phase 169 R3O tests. It does not execute the complete pytest suite. The audit then runs the current production search for both targets, without changing code, tests or tracked documentation.

Prerequisites: repository dependencies, Python, pytest and git. The audit is fail-closed on imports, malformed goals, source-screening errors and search exceptions: results are recorded, not converted into completed proofs.
