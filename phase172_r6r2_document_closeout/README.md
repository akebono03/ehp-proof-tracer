# Phase 172 R6R2 — Five-document closeout

This is the final **documentation-only** step after the successful Phase 172 R6 closeout. It never runs the active full pytest suite or alters mathematical proof code.

The installer checks the reviewed `develop` HEAD (`6ac7fd8a`), the five original document Git blobs, the committed R5 renderer blob, local/remote synchronization, and the existing R6 `closeout.json`, its test log, and the verified public proof. It rejects unreviewed source changes and reapplying an already documented closure.

Run from the repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r6r2_document_closeout\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r6r2_document_closeout\run.ps1" -Apply

git status -sb
git diff --stat
git diff --check
```

Both modes write **complete revised Markdown files**, with all historical content retained, to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r6r2_document_closeout_<timestamp>\full_documents\`, and preserve original full files under `backup_original`. DryRun changes no tracked files; Apply changes only `README.md`, `docs/design.md`, `docs/development_log.md`, `docs/roadmap.md`, and `docs/proof_records.md`. Application performs six focused tests, never reruns the full suite, and restores all five documents if the installation check fails.

The default R6 evidence directory is `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r6_20261031_144642_024616Z`. Use `-ReportDir <path>` if the verified output was saved elsewhere. No commits, fetches, resets, or Git index mutations are performed by the installer.
