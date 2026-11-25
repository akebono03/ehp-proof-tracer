# Phase 177 R3 — Isolated unsigned Delta composition

This package adds an isolated, source-backed inference rule for Toda Proposition 2.5. It uses the existing cited Proposition 2.5 GIVEN and a proved unsigned Delta equality. The literal composition needs no reflexive premise; a substituted argument requires a separate inferred equality. The existing signed rule is not changed.

The reviewed HEAD is `2d09ecbe10b60a38179022da561931a8e4bb39ba`. DryRun verifies pinned dependencies and source order. The normal run executes only the new rule tests and the existing signed-rule tests. No public provider registration, new GIVEN, database change, or group-completion claim is made. The eta double-suspension identity, notation transport, and Delta injectivity remain separate future tasks.

The source transcriptions already adopted by the repository are used; original-edition verification is not newly performed. The package was syntax-checked but repository-integrated pytest and Windows execution must be performed locally.
