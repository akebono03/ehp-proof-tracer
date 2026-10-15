# Phase 165 R5-R15: Deduplicate legacy EHP inputs

This guarded installer removes duplicate EHP leaf/window construction from the historical Phase 162 Web Narrative builder. It reuses the R5-R11 shared leaf function. It **does not delete the historical Renderer** or alter the public API. The bundled runner executes only focused tests and restores the old source if they fail.

Extract this package into the EHP Proof Tracer project root, then execute `run.ps1` from PowerShell. The original file is backed up under the package directory. Do not run twice without inspection.
