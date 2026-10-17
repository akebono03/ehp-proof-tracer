# Unified Rule Registry R3-3

This package registers the four fixed generic expansion providers and caller-provided expansion providers under stable provider IDs, preserving their original order and behavior. R1 continues supplying exactly one immutable rule tuple to R26, Witness, and Seeded paths. No proof certification or mathematical equivalence is inferred.

From the repository root, extract the ZIP and run `powershell -ExecutionPolicy Bypass -File .\phase165_r6_2_unified_registry_r3_r3\run.ps1`.

The installer refuses to run if R1 is missing or the pi4^3-specific adapter is still referenced. It backs up the shared module. Only targeted tests run. Other providers invoked directly are not yet moved into the registry; R3-4 will inventory and connect them after confirming signatures.
