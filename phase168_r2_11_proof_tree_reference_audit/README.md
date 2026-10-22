# Phase 168 R2-11 — Proof Tree / Reference audit

This is a read-only, same-invocation runtime audit for the $\pi_4^2$ narrative route. No production code is patched on disk. All temporary Python monkeypatches are reverted after the web-view call.

## Run

From the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase168_r2_11_proof_tree_reference_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r2_11_proof_tree_reference_audit\run.ps1"
```

## Scope

- Captures `presentation.nodes`, root-reachable proof steps, their rule kinds, premise IDs, and extractable literature locators.
- Captures Reference entry states before and after each selected function in the contribution renderer during **the same Web call**.
- Captures the public Web reference lines.
- Does not assert that the expected two references exist; it measures what is present.
- Does not edit or remove existing filters, change proof behavior, or run the complete test suite.

## Outputs

- `output/proof_reference_trace.json`
- `output/proof_reference_trace.md`

Send both output files for the next analysis. A `NO_PRESENTATION_CAPTURED` signal means this instrumented renderer was not visited and must not be reported as a valid reference count.

## Limitations

The audit wraps the shared contribution renderer. Other active routes are not instrumented. Reference extraction from an INFERENCE rule depends on the current `extract_toda_group_proof_step_literature_reference` implementation. Node IDs are local to the single Python process and are not stable across runs.
