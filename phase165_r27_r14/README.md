# Phase 165 R27-R14 — Production Consumer Triage

This package conservatively classifies root-level legacy dependencies identified by R27-R13-R1. It does not edit production code or certify that a Python import is executed in production.

Run from the repository root with `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r14\run.ps1`.

Outputs: `audit_report.json`, `live_consumer_candidates.csv`, `public_entry_imports.json`.

The report separates Generator, Operation, public entry, legacy builders, phase bridges, backup false-positives, and other consumers. All deletion decisions are deferred. Only targeted pytest is run.
