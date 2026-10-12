Phase 164 R8-R5: guarded bulk centralization of legacy ProofStep creation

REQUIRES: locally installed Phase 164 R8-R2 factory and R8-R3 changes.
ROOT: run this bundle's run.ps1 from the EHP Proof Tracer project directory.

Preflight compares actual AST call classifications with R8-R4's audited manifest.
If any relevant file has changed, or the local R8-R2 factory differs from
its verified baseline, migration stops without modifying production files.

Centralizes 128 legacy GIVEN constructors, 18 legacy INFERENCE constructors,
and 22 caller-side apply_inference_match invocations. It does NOT claim their
mathematical correctness, a statement registry link, or provenance eligibility.
The core proof.py engine stays unchanged to avoid circular dependencies.

Before each change, original bytes are copied into an automatically named
phase164_r8_r5_backup_YYYYMMDD_HHMMSS directory. The runner executes targeted
pytest only (no full suite). If those tests fail it restores backed up sources.

Outputs phase164_r8_r5_output/audit.json and CHANGED_CODE.md including full
modified import sections/classes/functions. Outstanding reviews: 66 replace()
calls, 10 core engine sites and one dynamic rule constructor. These are NOT
assumed migrated; therefore Phase 164 R8 is NOT closed by this bundle.
