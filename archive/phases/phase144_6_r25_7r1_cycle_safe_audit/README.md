# Phase 144-6 R25-7R1 — Cycle-safe Audit Repair

This package changes no production code.

R25-7 stopped because the diagnostic helper `_contains_nu_prime()` recursively
walked object `__dict__` values without cycle detection. R25-7R1 adds an
identity-based visited set to that diagnostic helper only.

The audit scope is otherwise unchanged:
- inspect the root `nu'` proof construction;
- inspect complete recursive provenance;
- verify exact Narrative block membership;
- enumerate production block dependency paths from each Argument to `pi_5^3`;
- print proof and semantic edges touching the `pi_5^3` block.

Only focused related tests are run. The full suite is intentionally not run.
No production repair is attempted.
