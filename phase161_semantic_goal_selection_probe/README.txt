Phase 161 — Semantic Goal Selection Candidate Discovery (read-only)

Scope:
- Build the real Production repository and applicability rule catalog.
- Start with the goal E: pi_4^2 -> pi_5^3 is isomorphism.
- Expand candidate rule conclusion types to a depth of three prerequisite layers.
- Match final candidate premise patterns against production proof-scope steps.
- Do not select the target proof's ancestry, do not import Phase59, and do not enumerate known rule families.
- Do not change Production flags or files.

This is a diagnostic discovery experiment, NOT a completed goal-only prover.
It does not certify fixed-point safety, prove that rules with identical conclusion
statement types target the same maps, or execute a derived proof.

Run in PowerShell from the repository root:
  powershell -ExecutionPolicy Bypass -File .\phase161_semantic_goal_selection_probe\run_phase161_semantic_goal_selection.ps1

Full JSON output:
  phase161_semantic_goal_selection_probe.json

Relevant targeted existing pytest tests (optional, no full suite):
  python -m pytest -q tests/test_phase86_depth_three_bounded_search.py tests/test_phase103_premise_pattern_compatibility_search.py
