# Phase 165 R7 Rule Identity Review

Read-only review of five potential rule-signature collisions in the active R8 discovery path.

Extract this directory into the repository root and run `run.ps1`.

Outputs `audit_result.json` with the premise and conclusion patterns, descriptions, and callable implementation evidence for each pair. The report does not claim mathematical equivalence. A matching displayed pattern is not sufficient grounds for deleting or merging rules.

The retired standard production applicability catalog is not called. No production files are changed; only two targeted tests run. Full pytest is intentionally omitted.
