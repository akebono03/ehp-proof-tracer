Phase 161 - semantic rule selection + real proof execution (read-only probe)

Run from repository root with run_phase161_semantic_selection_execution.ps1.
No existing repository files are edited. The script writes JSON to the repository root.

Rule selection does NOT use inference-rule names. It selects a rule by matching
real available ProofSteps to the rule's premise patterns, applying its guard
and conclusion builder, and comparing the generated conclusion with an exact
mathematical Statement goal. It computes seven known intermediate Statement
goals for the n=3 EHP chain; this is NOT yet automatic backward discovery of
all subgoals from the final goal alone. A provenance filter for the existing
Hopf relation still uses 'equality transitivity' rule name: removing that is
a future follow-up, not falsely claimed here.

Only genuine ProofSteps from the Production scope or derived in this run are
used. No synthetic GIVEN or INFERENCE statements are inserted. The complete
Production catalog is never marked fixed_point_safe.

Focused existing test (optional):
python -m pytest -q tests/test_phase59_n3_ehp_chain.py
The whole test suite is deliberately not run.
