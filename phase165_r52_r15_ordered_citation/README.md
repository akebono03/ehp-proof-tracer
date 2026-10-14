# R52-R15: Ordered Reference Lookup

This package adds an opt-in `typed_reference_ordered` backward-search mode using the existing Phase 164 citation policy. It does not alter the existing `typed_reference` behavior, claim that source order is verified, or change the renderer.

## Install and test

Run `run.ps1` in PowerShell after extracting the package into the repository root. The installer checks exact code anchors and keeps a backup. Run only the targeted tests for this step.

## Scope

- `phase165_r3_recursive_search.py`: extend `reconstruct_registered_goal` with a third lookup mode, while preserving existing modes.
- `phase165_r52_r15_ordered_citation.py`: new general-purpose `ordered_typed_reference_steps`.
- `test_phase165_r52_r15_ordered_citation.py`: new targeted tests.
- `run.ps1`: installer and targeted pytest invocation.

A reviewed assertion ID and verified earlier availability are required. Existing adopted-TeX registrations with unknown availability will fail closed in the new mode. Integration of independently reviewed order metadata into the default Web proof path is a later step.
