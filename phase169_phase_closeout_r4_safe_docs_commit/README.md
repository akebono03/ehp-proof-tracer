# Phase 169 R4 — Safe final documentation commit

The Phase 169 R3B documentation closeout has already succeeded. This package does not edit those documents. It validates the exact five changed files, the reviewed Git HEAD, the R1 full-test report (67 focused and 3,546 active test passes), the R3 full-text backup/manifest, and the remote branch before preparing an optional local commit.

**Audit-only is the default.** Running `run.ps1` does not stage or commit anything. Run `run.ps1 -Commit` only after inspecting the documentation diff and choosing to create the commit. The package never pushes, pulls, cleans, resets, restores, or deletes audit files. It does not rerun the full pytest suite.

Expected existing inputs outside the repository:

- `%LOCALAPPDATA%\EHPProofTracerRecovery\phase169_closeout_r1_20261028_193510_755227\report.json`
- `%LOCALAPPDATA%\EHPProofTracerRecovery\phase169_closeout_r3_20261028_195816_728887\manifest.json`
- The matching `before_full/` and `after_full/` directories.

The reviewed Git HEAD is `1e881f45b2f3f3ecbb1052750c9d7a7b5bf95712`. This script deliberately stops if GitHub, local HEAD, or origin/develop changes. Its commit operation stages exactly `README.md` and the four named `docs/*.md` files, then checks the commit's file list. Existing untracked audit directories are preserved. The precommit patch and JSON commit record, when applicable, are written only under `%LOCALAPPDATA%\EHPProofTracerRecovery`.

## Commands

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_PHASE169_CLOSEOUT_R4.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_phase_closeout_r4_safe_docs_commit\run.ps1"
git -c core.longpaths=true diff -- README.md docs/design.md docs/development_log.md docs/roadmap.md docs/proof_records.md
# Explicit opt-in, only when satisfied with the audit and diff:
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_phase_closeout_r4_safe_docs_commit\run.ps1" -Commit
git -c core.longpaths=true status -sb
```

After a successful local commit, `develop` should be ahead of `origin/develop` by one commit. Pushing is a separate, deliberate operation; this package does not push.
