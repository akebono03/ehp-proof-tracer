# Phase 163 R4-R67 Context Expansion

Read-only verification packet that checks SHA-256 hashes of 10 previously flagged source spans against the local Toda TeX files, then exports neighboring lines for editorial inspection. It preserves one Reference with possibly multiple Assertions. It does not approve mathematical boundaries, allocate production IDs, or alter the registry.

From the project root, expand the archive and run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r67_context_expansion\run.ps1`.

Inputs: `phase163_r4_r66_output/boundary_decisions.json`, `phase163_r4_r42_tex_extract/inputs/*.tex` (or project-root copies, as in R63). Outputs: `phase163_r4_r67_output/context_review.json` and `context_review.md`.

Only the five focused tests are run. The complete suite is reserved for the end of Phase 163.
