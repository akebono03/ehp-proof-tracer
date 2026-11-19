# Phase 175 R13R8R8 — Read-only Closeout Audit

This package checks the existing R13R8 proof-citation implementation without installing code, registering GIVEN statements, or changing proof rules.

## Requirements

Run on the `develop` branch at commit `b5a0b13884f6f0af527034d8c8bcd47b90c7cc97`. The audit compares the working tree, index, and committed blobs of the two production modules with their reviewed GitHub versions.

From the repository root, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r13r8r8_closeout\run.ps1 -DryRun`, followed by the same command without `-DryRun`.

The full command runs the existing R13R8R6 source-binding audit and checks the actual public narrative route for groups (5,4), (6,5), and (7,5). It then runs 13 focused pytest tests (R13R8R3, R13R8R4, and R13R8R6) with pytest caching disabled. No full test suite is run. The JSON report is written to the system temporary directory.

This gate is scoped to the three audited groups; it does not establish a universal guarantee for every possible future statement type.
