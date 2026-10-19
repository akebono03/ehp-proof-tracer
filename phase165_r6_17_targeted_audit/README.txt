Phase 165 R6-17 read-only targeted audit

Run from repository root with PowerShell:
  powershell -ExecutionPolicy Bypass -File .\phase165_r6_17_targeted_audit\run.ps1

Scans source for 7 key functions (including 5 standalone compatibility failures), and reports exact function bodies as present on the local checkout. Explicitly detects missing goal and citing_assertion_id at the Phase 164 pi5_3 web entry. Does not change repository source or tests. Does not execute full pytest or mathematical proof generation. Results are written to phase165_r6_audit_results/r6_17_targeted_audit/report.json.
