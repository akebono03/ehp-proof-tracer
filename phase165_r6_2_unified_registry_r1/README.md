# Phase 165 R6-2: Unified Backward Rule Registry R1

This first integration replaces three independent R8 discovery calls in the shared provider with one registry snapshot. Rule source identifiers are `module.factory`. No missing witness arguments are synthesized, no group-specific adapters are restored, and the existing public entry points are preserved.

From the repository root, run `powershell -ExecutionPolicy Bypass -File .\phase165_r6_2_unified_registry_r1\run.ps1`. The installer creates a source backup before changing `phase165_r52_r9_shared_math.py` and refuses unfamiliar source layouts.

Scope: R8's nine modules, plus explicitly registered `InferenceRule` objects through the registry API. Full-project rule registration, previously unregistered providers, actual proof reachability and recursive proof success remain outside R1 and must not be represented as completed.
