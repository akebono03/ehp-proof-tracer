# Phase 178 R8 — Equal finite cardinalities and surjective homomorphisms

This isolated rule derives injectivity from three independently proved inference premises: positive finite cardinalities of the domain and codomain, both equal, and surjectivity of the same typed homomorphism. It uses the existing statement classes and checks the coordinates of E, H and Delta. No generator images or cyclic presentations are required by R8. Order one is mathematically supported, although R6 does not produce it from a zero-group statement. No source, GIVEN, production provider or renderer is changed.

Run from the repository root after R7 has passed. The guard accepts the exact reviewed R7 hook whether committed or not, requires matching local/remote develop and unchanged reviewed dependencies, and verifies the R7 provider hash. The test runner disables pytest caching and bytecode writes. It runs only the R8 and R6 isolated test modules. No complete proof search and no full suite run.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase178_r8_finite_group_surjective_injective_isolated\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase178_r8_finite_group_surjective_injective_isolated\run.ps1
```

Expected gates: `PASS_R8_READ_ONLY_DRYRUN` and `PASS_R8_FINITE_SURJECTIVE_INJECTIVE_ISOLATED`. R9 will discover supported equal cardinalities and connect this existing rule to public search. This package does not claim that any actual homotopy-group proof is complete.
