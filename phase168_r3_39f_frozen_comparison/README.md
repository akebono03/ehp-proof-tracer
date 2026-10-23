# Phase 168 R3-39F — frozen narrative comparison

This is an audit-only package. It reuses the existing `phase168_r3_38_frozen_fulltext_audit.audit` capture and comparison implementation; it does not change production code, the renderer, or frozen benchmark files.

Extract the ZIP into the repository root and run `phase168_r3_39f_frozen_comparison/run.ps1` with PowerShell. The script captures the current Web narrative for `pi3_2`, `pi4_3`, and `pi5_4`, generates full Reference/proof unified diffs and a report in `output/`, then runs two focused pytest checks. It never runs the full test suite.

The benchmark source is `phase168_narrative_baseline_frozen/` and the rules in `phase168_frozen_v1/BASELINE_POLICY.md`. Numbering differences are deliberately not considered failures. Presence-of-explanation checks do not certify mathematical correctness and must be interpreted alongside the complete text diffs.
