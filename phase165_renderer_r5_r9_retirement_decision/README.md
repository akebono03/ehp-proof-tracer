# Phase 165 R5-R9: Legacy Narrative Retirement Decision

This is a read-only dependency audit for historical Narrative rendering modules. It does not remove modules, modify imports, change any math, or execute the full test suite.

## How to run

From the repository root, unzip `phase165_renderer_r5_r9_retirement_decision.zip` and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r5_r9_retirement_decision\run.ps1"
```

The script executes seven isolated tests, then writes `audit_output/audit.json` and `audit_output/review.md`.

## Scope

It scans active project-root Python modules and tests under `tests/`. Root files with `.phase` in their names are excluded as historical copies. It records static import dependencies, direct function calls, suspected dynamic string references, and paths from known UI and CLI entry modules.

## Safety and limitations

A missing static reference is not permission to delete public APIs. This does not prove absence of dynamic imports, reflection, or third-party API use. Previous Phase 162 fixture failures remain unresolved. No full pytest is run.
