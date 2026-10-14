# Phase 165 R27-R38 — Operation query proof migration

This package changes the CLI operation query, CLI operation proof, and Web operation proof entry points to use the registered typed search. It does not replay any legacy repository proof. It removes now-unused repository imports from the changed files and performs a conservative dependency-graph sweep of unreachable `repository_*.py` files. Existing implementations still in use are retained.

## Installation

Extract the ZIP into the project root and run `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r38\run.ps1`.

The installer writes `phase165_r27_r38_audit.json` and backups to `phase165_r27_r38_backup`. Only targeted package tests run; the full project test suite is not executed.

The Web proof view requires an actual proven statement. When the canonical search has not proved a requested fact, the entry raises a descriptive `ValueError` rather than fabricating a proof. This phase does not implement the separate partial-proof Web UI contract, rule applicability, or rule execution.
