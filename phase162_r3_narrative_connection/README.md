# Phase 162 R3 — Group-Root Narrative Connection

This bundle adds a narrative renderer driven by the verified Phase 162 R2 group-structure proof graph. It leaves the existing public narrative renderer unchanged.

The new entrypoints are:

- `render_phase162_r3_narrative(connection, existing_public_markdown=None)`: render the mathematical proof from the group-structure root, optionally preserving the existing Reference section verbatim.
- `render_phase162_r3_with_public_references(connection, presentation)`: call the existing public renderer for its Reference section and compose the graph-derived proof body.

This is an explicit adapter; it does not automatically replace the web endpoint. Callers must pass the R2 `ExistingProofConnectionResult` and the matching existing presentation.

## Install and test

Extract the ZIP at the EHP Proof Tracer repository root, then execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase162_r3_narrative_connection\run_phase162_r3_narrative_connection.ps1
```

Focused tests only. No full-suite test is invoked.

## Scope

The implementation validates the final group root, its three transport premises and required EHP ancestry. It does not fabricate any proof step, add mathematical results or update the existing UI routing. Existing references remain owned by the public renderer. Broader map types, reference linkage and web selection remain for a subsequent integration audit.
