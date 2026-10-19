# Phase 166 R3: Direct typed-reference citation gate

Extract into the repository root and run `phase166_r3_lookup_gate_fix/run.ps1` in PowerShell. The installer backs up the existing production file and modifies only `_typed_reference_steps()` and its call site in `reconstruct_registered_goal()`. It fails closed on unexpected source changes and is idempotent. The ordered citation gate is reused; no proof facts, permissions, or new database types are introduced. Only focused pytest is executed.
