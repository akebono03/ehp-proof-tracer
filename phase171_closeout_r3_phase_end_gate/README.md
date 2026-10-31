# Phase 171 R3 — Final Active-Suite Closeout Gate

This archive closes Phase 171 only after verifying the reviewed Phase 171 R2 five-document worktree, unchanged source/test Git blobs, and the single active-suite `tests/` pytest run at the end of the phase.

The reviewed baseline is `3e74849bf90bc115c16503ddd46d49996baa0856` on `develop`. Descendant commits are accepted only if their changes consist of the five reviewed documents and the listed Phase 171 closeout audit directories. Unknown source changes, staged changes, unreviewed document content, a missing or modified R2 document writer, or a previously installed final marker fail closed. Git is never reset or pulled automatically.

Run from the repository root on Windows:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_Closeout_R3_Final_Gate.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_closeout_r3_phase_end_gate\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_closeout_r3_phase_end_gate\run.ps1"
git status -sb
git diff --check
git diff --stat
```

Dry-run does not execute the active suite or modify tracked files. Normal execution invokes exactly one active full suite, using `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests`. If it passes, a final dated Phase 171 closeout section is inserted into `README.md` and appended to `docs/design.md`, `docs/development_log.md`, `docs/roadmap.md`, and `docs/proof_records.md`. The five complete revised documents, originals, pytest log, and `closeout.json` are preserved outside the repository in `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_closeout_r3_*`.

If pytest fails, no documents are modified. If pytest passes but document application fails, the originals are restored and the audit report preserves the successful test evidence; using `-ResumeReport <path-to-closeout.json>` is supported to finish the documents without rerunning the full suite, but only when the recorded HEAD and all five document SHA-256 digests match exactly. R3 does not add or modify mathematical source code, search, Proof Tree, or production rendering.

Isolated auditor tests can be run separately from the phase-end suite:

```powershell
python -B -m pytest -q --disable-warnings -p no:cacheprovider phase171_closeout_r3_phase_end_gate/tests/test_closeout.py
```
