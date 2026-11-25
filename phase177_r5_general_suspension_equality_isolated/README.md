# Phase 177 R5 — General suspension equality (isolated)

Reviewed develop HEAD: `61911911e25b2ae379669be809001c1237051d2c`.

R4 found independently provable one-step images but missing element equality for eta, nu, sigma and epsilon, and missing iterated notation for formal stable and unstable elements.

This package adds two isolated backward proposals. The first requires the exact independently inferred typed `GeneratorImage` to derive $E(x)=y$. The second checks the identical typed base and equal total suspension exponents, with a genuine nested representation and total exponent at least two. It does not identify different named generators. Both use the existing typed endpoint checker; its sphere-dimension lower bound of two is preserved. Existing equality congruence and transitivity are replayed to establish $E^2(x)=z$ from two real one-step images in focused tests. No stable-range restriction is introduced by either new rule. No database row or new GIVEN supplies an equality.

No existing file is modified, no public provider is connected, and no whole-suite pytest is run. Historical eta/composite paths remain unchanged to preserve prior proof and renderer behavior. This is an isolated validation, not proof completion of the root group. The subsequent step is to connect the verified rules and plan the intermediate goals in public search without duplicating per-family logic.

Run `run.ps1 -DryRun`, then `run.ps1` from the repository. The package checks the reviewed local and origin/develop HEAD, existing source blobs and a clean tracked worktree. All source and test functions are in the package, and the runner executes only scoped tests. The package was syntax-checked before distribution; repository-dependent tests must run locally.
