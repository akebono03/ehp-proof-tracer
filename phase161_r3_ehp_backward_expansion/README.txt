Phase 161 R3 — Concrete EHP Backward Goal Expansion

Adds four concrete EHP implication schemas with exactness as a separate
subgoal, composing with the previously installed Phase 161 R2 entry point.
It does not perform proof search, assert goal satisfaction or construct
ProofStep objects. Two literature/fact goals remain unresolved at R3.

Run from the repository root after R2:
  powershell -ExecutionPolicy Bypass -File .\phase161_r3_ehp_backward_expansion\run_phase161_r3_ehp_backward_expansion.ps1

Changes:
  NEW phase161_r3_backward_goal_schema.py
  NEW tests/test_phase161_r3_backward_goal_schema.py
Focused tests:
  python -B -m pytest -q tests/test_phase161_r2_backward_goal_schema.py tests/test_phase161_r3_backward_goal_schema.py
