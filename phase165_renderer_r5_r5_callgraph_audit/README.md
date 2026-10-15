# Phase 165 R5-R5: renderer helper ownership audit

This is a **read-only, evidence-producing audit**, not a migration. It reviews the candidate helper files previously discovered by R5-R2 and records source-level import and call sites. A potential standalone entry is flagged for human review. The script does not certify a fully unified execution path, mathematical validity, or search completeness.

## Prerequisites

Run the previously installed Phase 165 R5-R4 package first. The project must retain `phase165_renderer_r5_r2_archive_classification/audit.py`, used as the baseline scope and discovery logic.

## Execution

From the project root, extract the ZIP and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r5_r5_callgraph_audit\run.ps1"
```

Read `phase165_renderer_r5_r5_callgraph_audit/audit_output/review.md` and `audit.json`. No production file is modified. Five self-tests run; the project-wide pytest suite is not run.

## Scope

Only project-root production Python files and official `tests/` are inspected. Backups and previously extracted installers are excluded under the same rule as R5-R2. Tests with the historical Phase 162 `prop51_steps` fixture issue are not reclassified as passing. Not every renderer in the repository necessarily belongs to the Toda group Narrative path.
