# Phase 165 R9 Rule Registry Inventory

This read-only audit inventories active rule factories, reports deterministic provisional IDs, checks duplicate candidates, and records backward-pattern eligibility and static connection sites.

Extract into the repository root, then run `run.ps1`. Results are written to `audit_result.json` in this folder.

The retired production applicability catalog is never constructed. No production code or existing tests are modified, and only two targeted tests are run. This audit does not certify the full rule registry or prove semantic rule equivalence.
