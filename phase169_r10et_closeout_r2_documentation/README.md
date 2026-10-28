# Phase 169 R10ET Closeout R2: Five Complete Documents

This package updates **only** the five canonical Markdown documents: `README.md`, `docs/design.md`, `docs/development_log.md`, `docs/roadmap.md`, `docs/proof_records.md`. The README addition is in English; additions to the other four are in Japanese. All earlier development/proof-record bytes remain in place and the new record is appended.

## Prerequisites and operation

- Windows PowerShell with Python and pytest available in the repository.
- The `develop` branch and live GitHub `origin/develop` must match the reviewed commit `a759c12fbcc0a7fc64c578fcd8a4dd86ac94b3c5`.
- No staged or unstaged **tracked** files, including documents and code, may be modified at start. Untracked audit packages are allowed.
- All eight reviewed implementation/verification files and all five original documents must match exact inspected Git blob IDs.

Extract into the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase169_r10et_closeout_r2_documentation\run.ps1
git -c core.longpaths=true status -sb
```

Before editing anything, the runner executes the package's focused tests, probes the live remote with `git ls-remote` without fetching, validates the worktree using `git hash-object` (no `-w`), and reconstructs each entire new document from the complete local original. It writes full **BEFORE_FULL** and **AFTER_FULL** documents, a review diff, and `updated_five_documents_FULL.zip` outside Dropbox under `%LOCALAPPDATA%\EHPProofTracerRecovery\r10et_closeout_r2_<timestamp>`.

The complete Markdown documents are the deliverables, not partial snippets. The runner replaces each working document atomically, validates all five complete bytes, and restores the original changed documents on failure. It never runs Git reset/checkout/pull/fetch/add/commit, never touches the index, and does not run the full pytest suite.

This is a workstream documentation checkpoint, **not** closure of Phase 169.

## Windows newline compatibility update (R2A)

The archive test now writes binary LF and CRLF fixtures to prevent platform-dependent text-mode newline conversion. GitHub develop moved by one documentation-audit package commit; the live remote and local HEAD must both match `a759c12fbcc0a7fc64c578fcd8a4dd86ac94b3c5` before any of the five documents are updated. No guard is disabled.
