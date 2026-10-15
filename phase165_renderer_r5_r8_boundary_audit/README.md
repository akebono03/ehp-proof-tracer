# Phase 165 R5-R8 Public Entry Boundary Audit

This read-only package checks import connectivity and direct imported-function calls across current Group Proof, CLI, Generator, and the historical Phase 162 narrative modules. It does not modify application source files.

## Windows execution

Extract this ZIP into the project root, preserving the `phase165_renderer_r5_r8_boundary_audit` directory, then run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r5_r8_boundary_audit\run.ps1"
```

The script executes six scoped audit tests and writes `audit_output/audit.json` and `audit_output/review.md`. It does not run the full test suite or certify that runtime or dynamically imported routes are absent.

## Scope

- `audit.py`: active top-level Python modules, direct import calls, and known public entry boundaries.
- `test_audit.py`: focused AST-audit tests with temporary fixtures.
- `run.ps1`: tests followed by read-only inspection.
- `CHANGED_CODE.md`: complete source for every new or edited function and file.
- `AUDIT.md`: Japanese scope, acceptance criteria, and outstanding issues.
