Phase 164 R7-R3: Generator standard-entry registry-backed internal proof link resolution.

Scope: only the STANDARD Generator lookup, not generic user supplied repository lookup.
No citation becomes usable merely because a proof repository contains a ProofStep.
No ProofStep creation or graph transformation; not a Phase R8/R9 implementation.

Changed production module:
 repository_generator_known_group_identity_lookup.py
 - import phase164_r7_r3_generator_registry.validate_generator_repository_registry_links
 - function find_standard_repository_generator_known_group_identity_nodes (full function in CHANGED_CODE.md)
Added production module:
 phase164_r7_r3_generator_registry.py
 - validate_generator_repository_registry_links (new function at module scope)
Added test module:
 tests/test_phase164_r7_r3_generator_registry.py

Commands: Expand-Archive then powershell -ExecutionPolicy Bypass -File .\phase164_r7_r3_generator_registry\run.ps1
Tests: R7-R3 local 5 tests, R7 resolver, Phase109 Generator identity, Phase120 Web Generator.
Phase boundary: R7-R4 Operation and R7-R5 Group not migrated; overall R7 remains open.
Full suite intentionally NOT executed.
