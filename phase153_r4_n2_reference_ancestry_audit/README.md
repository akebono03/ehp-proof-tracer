# Phase 153-R4 — 6-group n=2 Reference ancestry audit

## Purpose

This package audits Reference selection for the six low-dimensional `n=2` targets:

- `pi_4^2`
- `pi_5^2`
- `pi_6^2`
- `pi_7^2`
- `pi_8^2`
- `pi_9^2`

R4 is intentionally audit-only. It does not change production code and does not implement the later Reference-granularity work.

## Evidence collected

For every literature Reference entry in each target proof presentation, the audit reports:

- whether the target/root proof step belongs to the Reference entry,
- whether the current Reference statement-selection rule selects the root step,
- whether each Reference-bearing step is actually used as a proof-edge premise,
- its direct proof-edge parents,
- the shortest proof-edge distance from the step to the target/root,
- the rendered statement currently associated with the step.

This separates three notions that must not be conflated:

1. a target/root statement carrying a literature locator,
2. a theorem aggregate carrying the same locator,
3. an external premise/ancestry statement actually used by the target proof.

## Files

- `audit_phase153_r4_n2_reference_ancestry.py`
- `test_phase153_r4_n2_reference_ancestry_audit.py`
- `run_phase153_r4_n2_reference_ancestry_audit.ps1`

The generated report is written to:

`output/phase153_r4_n2_reference_ancestry_audit.md`

## Scope boundary

R4 does not:

- change `toda_group_proof_narrative_references.py`,
- change the Narrative renderer,
- split one literature Reference into statement-level References,
- remove or renumber existing References,
- perform the 112-group audit,
- run the full test suite.

The next implementation step should be based on the evidence from this audit and should introduce only the smallest generic rule needed to exclude target/root ownership from external Reference selection while preserving genuinely used proof ancestry.
