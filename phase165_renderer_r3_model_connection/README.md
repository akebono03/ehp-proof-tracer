# Phase 165 Renderer R3 — Shared Narrative Model Connection

This package connects the existing public complete/partial proof entry to the R2 `NarrativeProofModel` and one dispatcher in the established Narrative module.

It does not alter proof search, math, source references, the established rendering functions, or legacy compatibility imports. It does not remove historical duplicate functions; that is outside the narrow R3 connector scope.

## Install

Extract the ZIP into the project root. Run `phase165_renderer_r3_model_connection/run.ps1` from PowerShell. The runner saves three Markdown baselines, installs the guarded patch, runs seven targeted tests, then requires byte-for-byte equivalent Unicode text. On regression, it restores both patched files.

The runner never executes the full project test suite.
