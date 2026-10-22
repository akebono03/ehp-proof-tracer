# Phase 168 R2-8(7) — Typed provenance for screened proof steps

This package attaches registered literature locators to source-screened GIVEN steps, and identifies the verified Toda (5.2) transport inference with its registered equation locator. It does not change citation admissibility, theorem content, proof rules, or publication ordering.

Run from the repository root after extracting the ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase168_r2_8_7_reference_binding\run.ps1
```

`patch.py` checks the expected AST and source markers before writing; backups are retained. Existing trace results are regenerated in `phase168_r2_8_6_reference_trace/output/reference_trace.json`. Full replaced functions and the complete altered import section are emitted as text files by the patch.

This patch does **not** claim that the shared Narrative renderer will display the reference section: its later fixed-boundary and body-usage filters must be audited against the new trace. It also does not change generic "supporting result" prose yet.
