# Phase 165 R12-R25 — Web Proof Order Diagnostic

This package inspects the ordinary Web proof path without modifying it. It reports concrete typed goals, registered proof order, exact matching, backward expansion candidates, and observed search results. It never injects a completed proof or a group-specific adapter.

Extract the ZIP into the project root, then run `powershell -ExecutionPolicy Bypass -File .\phase165_r12_r25_web_order_diagnostic\run.ps1`.

Review `audit_result.json` before considering any order registration or shared-search code change. Only focused pytest is run; the full test suite is reserved for the end of Phase 165.
