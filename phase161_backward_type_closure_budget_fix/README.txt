Phase 161: Backward Type Closure / Eligible-rule Budget Repair

This is a read-only diagnostic. It modifies only the standalone audit script.
The original script stopped before attempting inference because more than 1000 catalog rules
were reachable by statement type alone. This revision keeps the goal-derived type closure,
but tests whether every premise has an available ProofStep of compatible statement type
and proof-rule origin before applying the 1000-rule execution budget.

It does not establish full backward chaining: four exactness goals, Proposition 5.1,
and a provenance-name-filtered relation still form a preselected six-premise seed profile.
It does not enable production fixed_point_safe flags or mutate the repository.

Run from the repo root:
  powershell -ExecutionPolicy Bypass -File .\phase161_backward_type_closure_budget_fix\run_phase161_backward_type_closure.ps1

Output JSON: phase161_backward_type_closure_budget_fix.json
A nonzero exit means no proof was established within the stated limits;
inspect status and first_attempts diagnostics. Entire pytest suite not executed.
