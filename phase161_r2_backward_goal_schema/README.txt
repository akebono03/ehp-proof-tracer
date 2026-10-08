Phase 161 R2 — single-step backward goal schema

Scope: E: pi_4^2 -> pi_5^3 isomorphism ONLY.
No full backward chaining, no injected ProofSteps, no forward execution.
Existing production code and existing tests are unchanged.

Files copied into repository root:
- phase161_backward_goal_schema.py (new module)
- tests/test_phase161_r2_backward_goal_schema.py (new focused test)

Run from repository root:
  powershell -ExecutionPolicy Bypass -File .\phase161_r2_backward_goal_schema\run_phase161_r2_backward_goal_schema.ps1

Test: python -B -m pytest -q tests/test_phase161_r2_backward_goal_schema.py
Next boundary: recursive EHP subgoal expansion belongs to R3.
