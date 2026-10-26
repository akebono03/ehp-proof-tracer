# Phase 169 R3G2 — Production citation resolver audit correction

This is an **AUDIT_ONLY** package. It requires the already installed Phase 169 R3F3 terminal providers but does not patch any production source, existing tests, or project documentation.

The earlier R3G1 audit assumed that the target `pi_5^3` Relation appears *exactly once* in the registry. This is not the way the live search chooses its publication target: its database-derived typed goal may differ from the registry presentation. R3G2 calls the same `resolve_specialized_goal_citing_id` as `search_group_from_registered_goal`, and records literal registry matches solely as diagnostic evidence. The approved Proposition 5.3 component and publication checks remain required.

Extract the ZIP at the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase169_r3g2_actual_citing_resolution\run.ps1`.

The package includes the **complete audit.py**, four focused audit tests, and runs two existing EHP test files. The actual search and its report are generated locally in `output/source_and_composite.json`. Missing citations, mismatching rules, or failed tests cause nonzero termination. The completed group proof is **not** claimed, and the full suite is **not** run.
