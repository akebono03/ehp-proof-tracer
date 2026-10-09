Phase 163 R1C: Static registration evidence audit (read-only)

Requirement: Run Phase 163 R1B first, leaving phase163_r1b_output/registration_priority.csv in the project root.

Run on Windows PowerShell from project root:
  powershell -ExecutionPolicy Bypass -File ".\phase163_r1c_registration_evidence\run.ps1"

Outputs: phase163_r1c_output/registration_sites.csv, file_counts.csv, summary.json, report.md

Only R1B priority files are inspected. Call sites are not distinct registered statements.
No imports from the application are executed. No existing source or test files change.
