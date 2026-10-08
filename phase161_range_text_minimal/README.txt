Phase 161 minimal range_text change

Place this directory directly under the EHP Proof Tracer repository root.
Run from PowerShell:

  powershell -ExecutionPolicy Bypass -File ".\phase161_range_text_minimal\run_phase161_range_text.ps1"

Only the two exact fixed-statement component definitions in
`toda_literature_statement_boundary.py` are modified.
The patch refuses to run if their source blocks differ from those
verified in the public GitHub main branch on 2026-10-08.
An existing applied patch is accepted without further changes.
The focused tests use the public component-lookup API.
No full test suite is run.
