Phase 163 R1D - Read-only static registration audit

Existing source files are not modified. The script excludes tests, archives,
phase patch folders, and the standard excluded directories. It does not import
project modules or execute registry factories. Counts are site counts, not
unique mathematical statements.

Run: powershell -ExecutionPolicy Bypass -File .\phase163_r1d_registry_identity\run.ps1
Focused tests: python -B -m pytest -q .\phase163_r1d_registry_identity\tests\test_audit.py
Outputs: phase163_r1d_output\registration_sites.csv,
statement_type_definitions.csv, duplicate_key_candidates.csv,
repeated_expression_candidates.csv, summary.json, report.md.
