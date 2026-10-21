# Phase 166 R3-AU-6 coordinate mapping audit

Read-only comparison of each group-local component's sorted position and the nonzero coefficient position in the R3-AU-5 audit dataset. The comparison does not certify mathematical basis order or typed expressions. The `generator` column is optional reference text.

Run `powershell -ExecutionPolicy Bypass -File ".\phase166_r3au6_coordinate_mapping\run.ps1"` from the repository root after extracting the ZIP.

Input: `phase166_r3au5_db_convention_audit/results/all_rows.csv`.

Outputs: `results/summary.json`, `results/all_mapping_rows.csv`, `results/exceptions_and_special_rows.csv`.
