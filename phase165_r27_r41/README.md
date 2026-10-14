# Phase 165 R27-R41

This targeted change moves the operation query parser into a neutral module and migrates the legacy `cli.py element` command to the typed generator search. It preserves the CLI signature and retains the old parser for external compatibility. No full test suite is run.

## Install

Unzip at the repository root, then run `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r41\run.ps1`.

## Scope

This package does not remove the remaining legacy group calculation, proof-scope catalog or generator execution engine. Those require semantic migrations rather than deleting imports. Backups are saved in `phase165_r27_r41_backup`.
