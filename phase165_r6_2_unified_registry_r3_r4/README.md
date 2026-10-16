# Phase 165 R6-2: Unified Provider Registry R3-4

This package connects four citation-context-dependent backward expansion providers to the pre-existing provider registry. It preserves their execution order and arguments. It does not certify proofs, create witnesses, or reintroduce group-specific adapters.

From the repository root, extract the ZIP and execute `powershell -ExecutionPolicy Bypass -File .\phase165_r6_2_unified_registry_r3_r4\run.ps1`.

The installer requires completed R1, R3-3, and removal of the dedicated pi4^3 adapter. Only targeted pytest is run.
