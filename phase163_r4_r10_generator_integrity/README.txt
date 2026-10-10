Phase 163 R4-R10: Proposition 5.6 generator integrity

Extract the ZIP into the existing ehp_proof project folder, then run:

powershell -ExecutionPolicy Bypass -File .\phase163_r4_r10_generator_integrity\run.ps1

Scope: focused typed registry generator audit only. No production logic or
renderer changes. No full test suite. Failure is fail-closed and will not
mutate the registered mathematical statement.
