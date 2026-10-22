# Phase 168 R2-8(5): Proof Search Connection Audit

This is a read-only audit of nine citation-resolved group goals. It checks the citing assertion, its publication position, screened proof links, self-citation exclusion, and the actual backward proof-search result. `RESOLVED` citation status alone is never interpreted as proof completion.

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase168_r2_8_5_search_connection_audit\run.ps1
```

The report is written to `phase168_r2_8_5_search_connection_audit/output/search_connection.json`. The script runs only focused tests. No production code is modified. Full pytest is reserved for the end of Phase 168.
