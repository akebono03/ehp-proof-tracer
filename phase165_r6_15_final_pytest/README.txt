Phase 165 R6-15: Final whole current test-suite execution

Run from repository root with PowerShell:
  powershell -ExecutionPolicy Bypass -File .\phase165_r6_15_final_pytest\run.ps1

Does not change source code or test files. Executes python -m pytest tests -q --tb=short once.
Logs and JSON summary: phase165_r6_audit_results/r6_15_final_pytest
Does not claim Phase 165 is complete unless the full tests pass and any outstanding conditions are reviewed.
