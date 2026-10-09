# Phase 162 R10-R5: Read-only prose origin audit

This diagnostic does not modify existing project code or tests.

From the project root, extract the ZIP into the root and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase162_r10_r5_prose_origin_audit\run.ps1"
```

Reports:
- `phase162_r10_r5_prose_origin.md`: every node and each narrative line with candidate mathematical origins.
- `phase162_r10_r5_prose_origin.json`: machine-readable audit records.
- `phase162_r10_r5_web_narrative.md`: actual generated Markdown.

Exact-LaTeX matching is diagnostic, not a proof of dependency or irrelevance. A line may match several ProofSteps; a multi-line display formula may fail to match. The transport appendix is separately inspected. Tests cover helper functions only; the audit executes the production Web replay.
