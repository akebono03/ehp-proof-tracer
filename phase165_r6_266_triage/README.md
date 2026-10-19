# Phase 165 R6 — Remaining Collection Error Triage

Run `run.ps1` from the repository root after the Phase 165 R6 graph cleanup. Reads the most recent `phase165_r6_audit_results/graph_cleanup/*/collection.log`. Expects 266 collection errors, and refuses to write a report if the count differs. Produces `phase165_r6_audit_results/triage_266/report.json` and `summary.md`. This package never deletes or edits production files or existing tests. It does not rerun pytest collection or full-suite tests; the only pytest call runs three focused tests of the parser.
