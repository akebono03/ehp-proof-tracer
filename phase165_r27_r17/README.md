# Phase 165 R27-R17: Generator legacy bootstrap entry removal

This installer replaces only `explore_standard_repository_generator_input` and removes the no-longer-used import of `build_standard_production_proof_repository` from `repository_element_facade.py`.

The injected-repository API, `explore_repository_generator`, remains unchanged. Standard entry returns a typed zero-occurrence report backed by an empty `ProofRepository`, preserving aliases and the presentation contract. Zero occurrences means **no verified source evidence in this interim route**, not mathematical nonexistence.

The earlier tests that assert legacy Bootstrap occurrences for `nu_prime` intentionally conflict with the migration goal and are **not** modified or run in R27-R17. Before phase closure they must be replaced with new-source evidence tests, and the entire suite must run at the end of Phase 165. The canonical typed registry and rules are unchanged.

Run `run.ps1` from the repository root. The script creates a `.phase165_r27_r17_backup.py` copy of the original source before replacing it. Only five new targeted tests run. No full pytest.
