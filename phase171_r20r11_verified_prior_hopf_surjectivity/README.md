# Phase 171 R20R11 — Verified Prior Group in Hopf Surjectivity

This narrowly scoped patch keeps the existing First Successful Proof Search algorithm, source-publication screening, and all pre-existing inference-only rules intact. It adds an alternative checked inference for an earlier database group result (`GIVEN`) and an independently inferred Hopf-generator image (`INFERENCE`).

The prior group leaf is accepted only when the existing `verified_db_step` validates the actual proof step against the CSV, dependency order, and optional registered annotation. It never creates or introduces a new mathematical GIVEN and never imports a completed proof tree.

## Files changed

- `phase171_r2j_r2_cyclic_hopf_surjective/source.py`: add a verified prior result inference rule and a conditional proposal. The existing two-INFERENCE rule is preserved.
- `phase165_r52_r9_shared_math.py`: pass the existing source context to the proposal provider.

The package supplies focused tests and a post-patch audit. No other production files or project documentation are changed.

## Commands

From the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R20R11_VERIFIED_PRIOR_HOPF.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r11_verified_prior_hopf_surjectivity\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r11_verified_prior_hopf_surjectivity\run.ps1"
git status -sb
git diff --stat
```

The installer verifies the `develop` branch, two specific GitHub-reviewed source blobs, and the absence of pre-existing edits to these two source files. It preserves the line endings of each original source file and backs them up inside the package output folder.

The installer writes full replacement files and the complete changed functions/imports to `output/full_replacements/` and `output/CODE_FULL_JA.md`. The audit report is visible at `output/audit.json` **within this package**.

The post-patch audit distinguishes proof search completion from web verification; it makes no claim of complete or web-verified proof unless the canonical search actually establishes it.

Do not re-run the installer after successful application. It fails closed on already patched files.
