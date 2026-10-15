# Phase 165 R56-R2 — Restore the Public Narrative Renderer

This patch reconnects completed, typed backward-search proofs to the **existing** `render_toda_group_proof_narrative_markdown()` entry point. R56 mistakenly called `render_toda_group_proof_generic_proof_markdown()` and inserted ad-hoc public headings and a placeholder Reference section. R56-R2 removes that alternate formatting path.

## Scope

The only production file replaced is `phase165_r56_presentation_adapter.py`. Its `render_completed_shared_narrative()` function retains R56's proof-root validation and Toda replay/presentation construction, but delegates its complete presentation to the existing public narrative renderer without adding text of its own. Its complete import section and full function are supplied in the installed Python module and `CHANGED_CODE.md`. No old proof replay or special group-number branch is introduced. The existing fail-closed partial-result path stays untouched.

New files under this package: `install.py`, `run.ps1`, `test_phase165_r56_r2_public_renderer.py`, and `CHANGED_CODE.md`. No current repository README or other documentation is modified.

## Install and run (PowerShell)

Expand `phase165_r56_r2_public_renderer.zip` into the repository root, and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_r56_r2_public_renderer\run.ps1"
```

The installer checks the expected R55/R56 baseline, backs up the existing adapter once, and is idempotent. Only the new focused tests and the R55/R56 focused regressions are run. The full test suite is reserved for the end of Phase 165.

## Completion and limitations

Success requires all targeted tests, including an actual $\pi_3^2$ Web-compatible public narrative rendering, to pass. If the established public renderer cannot yet handle a typed R53 ProofStep, the integration test must fail rather than returning the deprecated generic or a hard-coded proof. Rendering parity for other groups and the completeness of Reference provenance remain separate verification work.
