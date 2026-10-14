# Phase 165 R27-R58 — CLI Group Cutover

This package migrates the `cli.py` group command from legacy `build_toda_report` to the canonical partial-proof search via `toda_typed_group_facade.build_standard_toda_partial_result`. It renders the actual `PartialProofResult`, including unresolved cases, without claiming a known group structure.

Run `run.ps1` from an extracted package under the project root. The installer requires the current function signature and fails closed on unknown implementations. A backup and JSON audit are produced. The old calculation implementation and four `repository_*` specialization modules are **not** deleted in this step; existing legacy tests still use them.

Targeted tests only; no full pytest is run.
