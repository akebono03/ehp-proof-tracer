# Phase 167 R4-2: typed display origin trace

This is a read-only instrumentation of the current shared Narrative path. It captures the existing typed eta-family and generator-suspension statement render calls, preserving their order and their caller location. It does not modify any repository files or ProofSteps.

Run from the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase167_r4_2_render_origin_trace.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File .\phase167_r4_2_render_origin_trace\run.ps1
```

Attach `phase167_r4_2_render_origin_trace/trace.json` for the Phase 167 R4-2 targeted implementation. No pytest or 2-stem work is done here.
