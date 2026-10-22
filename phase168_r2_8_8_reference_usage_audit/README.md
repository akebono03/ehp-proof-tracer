# Phase 168 R2-8(8): Reference Usage Audit

This is a read-only audit. It does not patch production files. Run `run.ps1` from the extracted folder using PowerShell. It executes three focused tests and writes `output/reference_usage.json`.

The report distinguishes raw reference extraction, fixed-boundary filtering, root exclusion, synthetic premise-used filtering, and synthetic empty-used filtering. It captures the final rendered narrative. The internal `generic_used_step_ids` are **not** captured by this probe, so the exact deletion point cannot be definitively attributed to that stage.
