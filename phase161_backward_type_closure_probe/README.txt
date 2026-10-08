Phase 161 — backward statement-type closure + bounded real proof execution (read-only)

The only proof goal is E: pi_4^2 -> pi_5^3 is an isomorphism.
No list of seven intermediate statements or seven inference rule family names is used.
The script discovers statement TYPES backward from the Production rule catalog and attempts bounded forward application of rules in that closure to actual Production ProofSteps.

LIMITATIONS: This is NOT full goal-only concrete backward chaining. The initial six-fact profile is still supplied structurally (Proposition 5.1, Hopf relation, four EHP exactness windows), and an equality-transitivity provenance name filter remains. Type-level compatibility overapproximates applicability. No Production data is mutated, no fake proof steps are registered, no fixed_point_safe flags are changed. The attempted work is capped at five seed pairs, seven rounds, 80 generated steps, and 1000 candidate rule entries. Failure within these budgets is not a mathematical impossibility result.

In repository root, extract ZIP into repository root and run:
powershell -ExecutionPolicy Bypass -File .\phase161_backward_type_closure_probe\run_phase161_backward_type_closure.ps1

Focused tests if needed:
python -m pytest -q tests/test_phase59_n3_ehp_chain.py tests/test_phase86_depth_three_bounded_search.py
Whole suite reserved for Phase closure.
