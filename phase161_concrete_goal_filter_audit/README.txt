Phase 161: Concrete goal filter capability audit

Purpose: inspect the exact goal E:pi_4^2 -> pi_5^3 isomorphism against
Production catalog rules. Separate invertible conclusion_pattern rules from
conclusion_builder-only rules. The latter cannot be backward-unified without
additional information. No count-based beam pruning.

IMPORTANT: Full Production proof scope is used only as a diagnostic witness.
It contains target ancestry, and therefore DOES NOT establish independent
goal-only backward proof discovery. No repository code is changed.

Run the PowerShell launcher from the extracted directory. JSON is written
to the repository root.

Related tests: tests/test_phase59_n3_ehp_chain.py;
tests/test_phase86_depth_three_bounded_search.py.
Do not run the full suite before the end of Phase 161.
