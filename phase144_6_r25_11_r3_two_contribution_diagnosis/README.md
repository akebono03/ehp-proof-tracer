# Phase 144-6 R25-11-R3 Two-Contribution Diagnosis

## Purpose

R25-11-R2 proved that restoring prerequisite protection for every argument
role is too broad: the selected population dropped to 145 instead of 190.

This package therefore does not attempt another production repair.

## Files and functions touched

Production file restored to the current `develop` form:

- `toda_group_proof_narrative_argument_multi_renderer.py`
- `_toda_group_proof_narrative_argument_frontier_hidden_step_ids`

The rollback restores the definition-only prerequisite protection that is
currently present on GitHub `develop`.

Diagnostic-only files:

- `rollback_r25_11_r2.py`
- `audit_r25_11_r3.py`
- `run_phase144_6_r25_11_r3.ps1`

## Audit

The diagnostic prints:

1. selected contribution counts for all six representative groups;
2. total selected count and delta from 190;
3. raw visibility-occurrence classes;
4. every selected owner's statement type, rule, argument role, discourse
   role, provider-anchor state, placement, distance, provider-key count and
   rendered semantic text;
5. a focused pi_6^3 order-argument trace showing hidden/chain/anchor and
   necessity data.

This is intentionally lighter than rerunning Phase37-40 and the completion
audit.

## Completion condition

R25-11-R3 is complete when:

- R25-11-R2 is rolled back;
- the selected population is back at 192;
- the extra ownership is localized by group and argument;
- enough provenance/necessity data is available to formulate R25-11-R4
  without a statement-type or pi_6^3-specific hard-code.

No full pytest is run.
