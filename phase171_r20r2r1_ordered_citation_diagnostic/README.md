# Phase 171 R20R2R1 — Ordered Citation Diagnostic

This read-only package investigates two failures from the Phase 171 R20R2 focused test suite. It is **not a proof patch** and does not alter production Python files, Git state, citation permissions, or mathematical assertions.

## Files

- `audit.py` loads the existing test fixture from the repository, inspects the actual registered source, the citation decision, linked `GIVEN` evidence and search result, and writes `output/<timestamp>/diagnostic.json`.
- `run.ps1` runs the audit and only the two failing tests with the pytest cache provider disabled.
- `IMPLEMENTATION_NOTES_JA.md` explains what the evidence does and does not establish.
- `CHANGED_CODE.md` contains complete source for every new script and function.

## Run

Extract the ZIP at the EHP Proof Tracer repository root, then run in PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r20r2r1_ordered_citation_diagnostic\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r20r2r1_ordered_citation_diagnostic\run.ps1'
```

The runner may deliberately return a nonzero exit code when the pre-existing two-test failure reproduces. This is an observed outcome, not a failed installation.

The installer from R20R2 has already been applied; do **not** rerun it or reset your working tree to perform this audit. The present package requires no production changes. The full test suite is not run.
