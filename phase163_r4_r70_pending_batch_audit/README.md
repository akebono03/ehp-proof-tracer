# Phase 163 R4-R70: Read-only pending-candidate batch audit

Run `run.ps1` from the extracted folder under the EHP Proof Tracer repository root.

The script requires `phase163_r4_r51_output/review.json` and `phase163_r4_r69_output/order_duplicate_audit.json`. It runs focused tests and generates `phase163_r4_r70_output/pending_batch_audit.json`, `pending_batch_audit.csv`, and `report.md`.

The lexical buckets are not mathematical classifications. No production files, IDs, or proof search are modified. The full pytest suite is reserved for the end of Phase 163.
