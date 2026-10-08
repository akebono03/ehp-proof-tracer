Phase 161 R5: concrete backward-driven proof reconstruction.
Unzip at repository root and run run_phase161_r5_backward_driven_proof_reconstruction.ps1.
Adds only phase161_r5_backward_proof_reconstruction.py and a focused test file.
Input leaves are supplied independently; this module never fetches completed Phase59 result.steps.
The regression fixture uses Phase59's original premise_steps, not the finished proof.
EHP exactness is accepted only as a supplied GIVEN leaf, not created by R5.
This is specific to E:pi_4^2 -> pi_5^3. It is not general goal-only theorem proving.
Full pytest is reserved for Phase completion.
