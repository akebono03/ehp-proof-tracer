# Phase 176 R3R22 — Composite-left Hopf frontier audit

This is a read-only audit of the existing Toda Proposition 2.2 right-composition specializer. It checks whether a composite left factor can be recognized in the existing typed implementation. It does not complete the proof of the cyclic structure of pi_8^3.

## Scope

Only `phase176_r3r22_composite_hopf_frontier/` is added. No production modules are modified, and no new GIVEN statements, inference rules, or narrative renderers are registered.

## Run

From the repository root, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r22_composite_hopf_frontier\run.ps1 -DryRun`, followed by the same command without `-DryRun`. The second command runs the focused audit tests and `tests/test_hopf_rules.py`. Full pytest is deliberately excluded.

## Completion criteria

Source checks, a typed negative/positive frontier probe, and focused pytest must all succeed. A passing audit gate means only that the current implementation boundary was recorded; it is not a successful proof of the homotopy group.
