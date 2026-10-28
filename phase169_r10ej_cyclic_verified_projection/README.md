# Phase 169 R10EJ — Verified cyclic narrative projection

This package modifies one existing presentation function in EHP Proof Tracer:
`phase169_r10a_verified_stable_chain_projection/projection.py::project_verified_stable_image_chain()`.

It does not modify mathematical search, inference rules, proof trees, data files, trust boundaries, or the renderer. It requires a complete searched proof and retains the existing verified R10A root, suspension-map, image, citation, and external-consumer checks.

R10EJ extends the display to:

- Render the already-proven, typed composite generator with the existing public LaTeX printer when `element_tex()` does not cover it.
- Suppress only uncited nested `GeneratorImage` / `GeneratorSuspension` proof steps whose every actual consumer is already suppressed or is the compressed root.
- Leave unrelated/shared/cited evidence visible and keep all `ProofStep` objects in the model.

The focused live regression checks `pi_28^22` and `pi_32^22`, and controls for `pi_10^8`, a direct sum, and the 1-stem regression. It also checks Trust Boundary replay and citation visibility. The package never runs a full pytest suite.

## Windows PowerShell

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10ej_cyclic_verified_projection.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10ej_cyclic_verified_projection\run.ps1"
```

The runner verifies the reviewed Git ancestor and exact original file, creates a byte-exact backup under `output/run_...`, patches one function, runs focused tests and an audit, and restores the file automatically if validation fails. It does not checkout, reset, stage, commit, or push.

The separately supplied full modified function and source are in `project_verified_stable_image_chain_FULL.py` and `output/projection.py.FULL`. The runner exports the actual installed full function again under its timestamped output folder.
