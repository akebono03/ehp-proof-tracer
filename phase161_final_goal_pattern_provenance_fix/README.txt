Phase 161 final Goal Pattern provenance-corrected audit

Read-only audit. Production code and tests are not modified.
The prior audit used synthetic GIVEN ProofSteps. The actual final inference rule may require INFERENCE proof steps. This corrected audit separately reports semantic statement compatibility, GIVEN compatibility, and simulated required-proof-rule compatibility. A simulated INFERENCE step is NOT proof evidence.

Run from repository root:
  powershell -ExecutionPolicy Bypass -File .\phase161_final_goal_pattern_provenance_fix\run_phase161_final_goal_pattern_provenance_fix.ps1

Output: phase161_final_goal_pattern_provenance_fix.json
Focused existing pytest (optional):
  python -m pytest -q tests/test_phase59_n3_ehp_chain.py tests/test_phase103_premise_pattern_compatibility_search.py
