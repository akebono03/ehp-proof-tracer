Phase 161: Single final-rule Goal Pattern -> Premise Pattern compatibility audit

Read-only experiment. Uses current production catalog and the existing proof.py
match_statement_pattern(), substitute_statement_pattern(), and
match_premise_pattern() functions. Selects one specific production rule for this
focused Phase 161 experiment. Generates matching injective/surjective statements
for E: pi_4^2 -> pi_5^3. It does NOT establish a complete proof.

PowerShell from repository root:
Expand-Archive -Path "$HOME\Downloads\phase161_final_goal_pattern_probe.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase161_final_goal_pattern_probe\run_phase161_final_goal_pattern.ps1"

Output: phase161_final_goal_pattern_probe.json

Optional focused existing tests only:
python -m pytest -q tests/test_phase59_n3_ehp_chain.py tests/test_phase103_premise_pattern_compatibility_search.py

No repository source files or tests are modified; the full test suite is not run.
