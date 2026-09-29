# Phase 144-6 R25-21-R2 Import Repair

Audit-harness repair only. No production source files are modified.

Change:
- Correct the NarrativeArgument builder import from the nonexistent singular module
  `toda_group_proof_narrative_argument` to the current production module
  `toda_group_proof_narrative_arguments`.

The R25-21 audit scope and presentation-rule classification are unchanged.

Repository-wide pytest is intentionally not run.
