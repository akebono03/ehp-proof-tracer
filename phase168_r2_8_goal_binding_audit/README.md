# Phase 168 R2-8 Goal Boundary Audit

Read-only audit of typed group-goal selection, unique literature citation boundaries,
publication-order-screened GIVEN steps, and self-citation. No production code is changed.

Run from the repository root with `powershell -ExecutionPolicy Bypass -File .\phase168_r2_8_goal_binding_audit\run.ps1`.

The report is written to `output/goal_binding_audit.json`. A non-OK case is a finding,
not proof of an invalid theorem. Missing citation boundaries must not be substituted
with arbitrary assertions. The next implementation should fix only verified issues.
Full-suite pytest is reserved for the end of Phase 168.
