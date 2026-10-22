# Phase 168 R3-1 — Narrative Boundary Audit

A read-only AST audit of the current local EHP Proof Tracer checkout. It maps relevant function definitions and calls related to search, proof trees, narratives, and reference selection, and collects test candidates. No source files are changed and no full test suite is run.

From the repository root, extract the ZIP and execute:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase168_r3_1_narrative_boundary_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_1_narrative_boundary_audit\run.ps1"
```

Review `output/boundary_audit.md` and `output/boundary_audit.json`. This static audit cannot establish which calls occur at runtime or whether Proof Tree citations are complete. The next step is to use these findings alongside the R2-14 runtime route trace before replacing functions.
