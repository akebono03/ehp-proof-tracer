# Phase 169 — Final documentation closeout (R3)

This package certifies Phase 169's **reviewed implementation and active-test scope only**. It creates complete revised versions of `README.md`, `docs/design.md`, `docs/development_log.md`, `docs/roadmap.md`, and `docs/proof_records.md` at runtime using the exact previously reviewed files. All five original full documents and all five updated full documents are stored under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase169_closeout_r3_*`, outside the checkout. Prior history is preserved, with development and proof logs appended.

The script checks the 13 reviewed Git blobs, the R6 evidence blob, the final end-of-phase test-gate JSON report (67 focused and 3,546 active passes), the repository's branch, and the reviewed remote HEAD before making a change. Only the five documents may change. It does not run the full pytest suite again, change source code or tests, stage, commit, reset, clean, restore, pull, or push. The 10 lightweight helper tests are scoped to this documentation script.

If the local checkout is at the earlier reviewed commit, the script can still write the documentation but explicitly warns that the remote has moved ahead. **Do not run an unconditional `git pull`** when untracked audit-package paths may collide with newly tracked paths; preserve and reconcile those directories first. Do not use `git add -A` for this closeout. Use explicit paths for staging after reviewing the diff. The document change should only be committed after reconciling Git history safely.

Run from Windows PowerShell in the checkout root:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_PHASE169_CLOSEOUT_R3.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_phase_closeout_r3_documentation\run.ps1"
git -c core.longpaths=true status -sb
git -c core.longpaths=true diff -- README.md docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md
```

To **generate the complete documents without applying** them, run `python -B .\phase169_phase_closeout_r3_documentation\run.py --repo . --prepare-only` (requires the same reviewed repository and R1 report). This gives an opportunity to inspect the full proposed files in the external recovery folder first.
