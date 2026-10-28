# Phase 169 — End-of-phase active-suite verification

This package runs only at the **end of Phase 169**. It does not implement new mathematical facts, change existing source/tests/documents, stage files, or certify mathematical truth for arbitrary homotopy groups.

Prerequisites: clean tracked Git checkout on `develop`, local HEAD = `origin/develop` = remote HEAD; 13 production/doc reviewed Git blobs unchanged; the stored 19-case R6D audit evidence unchanged and PASS. Audit-generated untracked folders are permitted.

Steps: (1) eight focused helper tests, (2) preflight and 19-case R6 audit evidence validation, (3) ten focused Phase 169/168 regression files, (4) the full active `tests/` pytest at the Phase boundary, (5) tracked Git/index preservation verification.

All pytest invocations use `-p no:cacheprovider`, `-B`, and `PYTHONDONTWRITEBYTECODE=1` to avoid tracked `.pytest_cache` and bytecode changes. The full suite uses `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests` with the repository's existing Phase 155 historical audit deselection policy. No additional tests are silently excluded. A failing focused regression prevents the full run; a failure does not confer a completion status.

Logs and JSON report are written under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase169_closeout_r1_*`, outside the repository.

Successful `TEST_GATE_PASS=True` is **not** a completed Phase 169 closeout: review the report and update final Phase 169 documentation in a separate step. Only then record Phase 169 completion and the remaining scope/limitations.

## Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_PHASE169_CLOSEOUT_R1.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_phase_closeout_r1_final_test_gate\run.ps1"
git -c core.longpaths=true status -sb
```
