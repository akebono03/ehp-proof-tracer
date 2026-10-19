# Phase 165 R6 Closure Audit

This package performs the final **read-only source audit** for Phase 165. It does not edit production Python files or update frozen baselines.

## Prerequisites

Run from the EHP Proof Tracer repository root. The completed R3 Architecture Guard test and R4 frozen baseline tests, including both JSON baseline files, must already exist locally.

## Execute

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r6_closure_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r6_closure_audit\run.ps1"
```

The script runs R3 tests, then R4 tests, and only if both pass runs the full `python -m pytest -q` suite once. It captures each output, checks that baseline file SHA256 values are unchanged, and emits `phase165_r6_audit_results/audit_result.json`. The script does not rerun the R4 baseline capture utility.

A passing test suite is not proof that the HTML and mathematical typography are visually correct. Complete the manual checklist in `web_checklist.md`, including checking the actual browser at both `(n=2,k=1)` and `(n=3,k=1)`. Only mark Phase 165 closed after examining the pytest logs and the browser results.

Known cosmetic issues (English internal rule names, duplicated generator relations, repetitive specialization prose) are **not** automatically fixed in this phase. Baselines should not be silently updated to hide changes.
