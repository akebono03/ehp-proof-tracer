# Phase 177 R6 — General Suspension Equality Public Connection

This package connects the verified R5 rules to `shared_expansion_provider`. It adds no mathematical inference rule, GIVEN, source, or Delta-composition connection. Existing proposals retain their order; R6 adds candidates at the end of the ordinary merged search. All premises must be independently proved by the existing recursive search. Family metadata proposes a middle term only. Other middle terms can be proposed from available image or equality statements, and matching composite structure. This is a bounded candidate-discovery strategy, not a complete search of arbitrary intermediate elements.

Reviewed develop HEAD: `166068e75b171bf66f08437f9329c2191c36e83a`.

Run `run.ps1 -DryRun` first, then `run.ps1`. DryRun writes the full changed shared function and imports and the full shared file to the external audit directory printed by the installer, without changing tracked source. The installation preserves the current file's UTF-8 BOM and line endings, rejects unrelated tracked edits, and is repeatable at the reviewed HEAD. On focused-test failure the installed hook remains for inspection; the original bytes are saved as `shared_math.before` in the external audit directory.

Focused tests exercise named double-suspension equality (eta, nu, sigma, epsilon), formal stable and unstable iteration, the actual captured public provider, and candidate/type guards. Full pytest is not run. The group target and the R3 Delta rule are not changed.
