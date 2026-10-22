# Phase 167 R4 Read-only Narrative Audit

Run from the repository root in PowerShell after extracting the ZIP into that root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase167_r4_readonly_audit.zip" -DestinationPath '.' -Force
powershell -ExecutionPolicy Bypass -File '.\phase167_r4_readonly_audit\run.ps1'
```

The tool instruments existing render functions temporarily in memory and captures public Web narratives for pi3^2 and pi4^3, including call-path observations. It **does not modify production Python files, ProofSteps, search rules or references**. It does not run pytest.

Results are written to `phase167_r4_readonly_results/` for examination before any implementation patch. The output must be checked against the rolled-back local baseline. A GitHub branch may differ from the local working tree.

## R4 audit launcher correction

`run.ps1` temporarily prepends the repository root to `PYTHONPATH`, restores the previous value with `finally`, and does not change production files. This fixes `ModuleNotFoundError: No module named 'web_group_proof'` when invoking the audit file in its subdirectory.
