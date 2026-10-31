# Phase 172 R5: Provenance-preserving prior-result Reference headings

This package changes **presentation only**. It substitutes a reader-friendly Japanese heading for a verified `DB prior` entry in the completed Web proof, while preserving the original `LiteratureReference` locator, all ProofSteps, the original database adoption markers, and citation numbers. The literature proposition is displayed only as a **reference annotation**, never as independent proof authorization.

## Files

- `projection.py`: validates a cited, adopted database GIVEN leaf and projects its heading.
- `tests/test_projection.py`: real canonical proof and fail-closed checks.
- `install.py`: compares the current Renderer against the reviewed R2→R3→R4 transformation, generates complete replacement source and function outputs, patches only the Renderer, runs focused tests and rolls back on failure.
- `run.ps1`: PowerShell runner.
- `AUDIT_PLAN_JA.md`: Japanese scope, gates, and phase boundaries.
- `CODE_FULL_JA.md`: complete new source and test files, with a reproducible full-function output path.

## Windows PowerShell

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase172_R5_PRIOR_REFERENCE_DISPLAY.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r5_prior_reference_display\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r5_prior_reference_display\run.ps1" -RunFocusedTests
git status -sb
git diff --stat
```

The full test suite is intentionally excluded until the Phase 172 closeout. Do not copy presentation labels into the internal database locator: the original locator is a trust-boundary identity.
