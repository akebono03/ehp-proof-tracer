# Phase 163 R4-R75: Focused Ownership Review

This package reads the R74 report without modifying the production registry. It examines seven held boundary proposals and four unnumbered assertion candidates, and groups nearby candidates when a shared reference is plausible. These are provisional editorial ownership proposals, not verified mathematical statements or allocated IDs.

Run from the repository root with `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r75_boundary_ownership\run.ps1`. Requires Python and pytest, and the R74 output. It produces JSON, CSV and Markdown in `phase163_r4_r75_output`. Full pytest is intentionally not run.
