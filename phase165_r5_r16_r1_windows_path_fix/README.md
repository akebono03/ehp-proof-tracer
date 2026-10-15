# Phase 165 R5-R16-R1 — Windows Path Correction

This package reruns the read-only R5-R16 retirement gate. It fixes the Windows-only relative path formatting in direct-import reports by using `Path.as_posix()`. No production or proof code is modified.

Run from the project root after extraction:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r5_r16_r1_windows_path_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r5_r16_r1_windows_path_fix\run.ps1"
```

Reports are written to this package's `audit_output` directory. Full pytest is not run.
