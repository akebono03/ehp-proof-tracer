# Phase 166 R3-Q Reference Audit Runner Fix

This package corrects only the audit startup path. It includes the unchanged `audit.py` from the preceding read-only reference audit. Run `run.ps1` after extracting the ZIP into the repository root. The script changes to the repository root and invokes the audit with Python module mode so project imports can be resolved.

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase166_r3q_reference_audit_runner_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3q_reference_audit_runner_fix\run.ps1"
```

This is a read-only audit of production code. Its only intended output is `phase166_r3q_reference_audit_results/audit.json`; the full pytest suite is not run.
