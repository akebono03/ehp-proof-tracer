# Phase 165 R5-R6 — Renderer ownership review

This is a read-only, scoped audit of the 26 Renderer candidates identified by Phase 165 R5-R5. It neither rewrites application source nor removes historical backups. It produces an evidence report, not a claim of complete renderer consolidation.

## Requirements

Run from the root of `akebono03/ehp-proof-tracer` after completing R5-R5. The sibling folder `phase165_renderer_r5_r5_callgraph_audit` and its source audit dependencies must be present.

## Windows execution

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_renderer_r5_r6_ownership_review.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r5_r6_ownership_review\run.ps1"
```

## Outputs

- `audit_output/audit.json`: machine-readable candidates, upstream callers and focal import sites.
- `audit_output/review.md`: Japanese ownership report and review boundaries.

Six narrowly scoped audit tests run. No full pytest is executed. Six historical Phase 162 fixture failures are not resolved by this package.
