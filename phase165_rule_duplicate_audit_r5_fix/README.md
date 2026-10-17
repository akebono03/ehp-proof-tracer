# Phase 165 R5 Active Rule Duplicate Audit Fix

Read-only inspection of the active R8 rule discovery path.
The retired `standard_production_applicability_catalog` is never imported or called.

Run `run.ps1` from the extracted folder in the repository root.
The report `audit_result.json` checks name collisions, identical pattern signatures,
and object-identity collisions. It does **not** certify the entire unified registry.
No production files change. Only two targeted pytest tests run.
