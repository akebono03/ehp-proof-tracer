# Phase 165 Renderer R4 — retire legacy narrative imports

This package completes the static import migration away from the retired Generic Narrative renderer. It retains the established Markdown behavior and the shared low-level components. No proof search or theorem rule is changed.

## Scope

- Rename the first of two same-name public functions in the canonical renderer to a private internal function; preserve the existing alias so output does not change.
- Migrate imports of low-level helpers to `toda_group_proof_narrative_shared_components`.
- Migrate the partial public import to `toda_group_proof_narrative_renderer`.
- Retire the compatibility package only after checking that no static imports remain.
- Keep copies of every modified file and the removed compatibility package in `.phase165_renderer_r4_backup`.
- Compare exact completed and incomplete Markdown baselines and run targeted tests. Roll back on failures.

## Execution (from repository root)

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_renderer_r4_legacy_retirement.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r4_legacy_retirement\run.ps1"
```

Run after Phase 165 Renderer R3. Full pytest is intentionally not run until Phase closure.

## Review files

`AUDIT.md` explains the migration boundaries. `CHANGED_CODE.md` includes the complete installer/test/runner source. The installer records every modified production file in `.phase165_renderer_r4_backup/manifest.json`, with full originals in the same backup directory.
