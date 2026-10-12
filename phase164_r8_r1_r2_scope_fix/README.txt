Phase 164 R8-R1-R2: scoped ProofStep inventory correction.

Run PowerShell from the project root:
  powershell -ExecutionPolicy Bypass -File .\phase164_r8_r1_r2_scope_fix\run.ps1

Only root-level current Python files are counted, excluding root-level
utilities, tests and backup file names. All nested directories, including
archive, historical phase bundles and downloaded patch folders, are excluded.

Outputs replace the previously noisy inventory in phase164_r8_r1_output.
Production source is not changed. Full pytest is not run.

Boundary: counts are candidate call sites, not proven unique ProofStep producers.
'dataclasses.replace' includes operations on unrelated dataclasses.
