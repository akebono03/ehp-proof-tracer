# Phase 165 R8 Zero-Relation Rule Review

This read-only audit compares the general zero-equality inference rule with its composition-restricted counterpart. Matching premise and conclusion patterns alone are insufficient to establish equivalence because the latter has a match guard. The audit performs no consolidation or deletion.

Extract into the repository root and execute `run.ps1`. Only two targeted pytest tests are run. No full pytest is run. The report is written to `audit_result.json`.
