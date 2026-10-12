Phase 164 R8-R2: additive ProofStep factory contract.
Unzip in the repository root and run .\phase164_r8_r2_factory_contract\run.ps1.
Changes: add phase164_r8_proofstep_factory.py and tests/test_phase164_r8_r2_factory_contract.py.
No existing production files or callers are modified.
Three narrowly-scoped entry points: checked relation, inference via existing rules, and identity-preserving reuse.
Not yet migrated: GIVEN, EXACTNESS, computation, Hopf, map facts, and other direct constructors.
Full pytest is intentionally NOT run.
