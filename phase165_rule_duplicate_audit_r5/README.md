# Phase 165 R5 — Rule Inventory Duplicate Audit

Run `run.ps1` from PowerShell after extracting the archive at the repository root. The audit is read-only and does not run the full pytest suite. The JSON report distinguishes duplicate catalog keys, names, Python object identity, and textual premise/conclusion signature candidates. Signature candidates require manual mathematical review; they are not automatically merged. It compares the production catalog with the R8 discovery path and guards against the six dedicated pi4_3 rules being re-registered.
