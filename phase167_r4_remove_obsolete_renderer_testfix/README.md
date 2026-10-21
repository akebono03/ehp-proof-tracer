# Phase 167 R4 — obsolete Renderer removal (test correction)

The previous archive correctly captured identical before/after results for pi3^2, pi4^3, pi5^4, pi6^5 and pi7^6, but pytest collected a historical package-local module with the same name as a root module. The previous run therefore rolled back.

This archive retains the same production changes. The test command uses `--import-mode=importlib` and a new focused R4 test module. It additionally runs only the historical tests still compatible with the current completed pi5^4 implementation; it does not rewrite historical tests or assert obsolete expectations.

Modified production files: `phase165_r56_presentation_adapter.py` (`render_completed_shared_narrative` complete replacement), `phase165_r57_r10_step_narrative.py` (`render_completed_from_proofsteps`, `_math_statement`, `_reference_label` deleted and imports updated). The installer retains the existing `ordered_proof_ancestry` and `has_transport_proof_ancestry`.

Baseline comparison: five groups at k=1, n=2..6, including stable 1-stem n=4..6. Compares status, conclusions, open goals, ProofSteps, Web lines and complete Markdown. Does not touch 2-stem. Full pytest is not run. On any failure production files are restored.

Run at repository root from PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase167_r4_remove_obsolete_renderer_testfix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase167_r4_remove_obsolete_renderer_testfix\run.ps1"
```
