# Phase 174 R3-R7-R22 — Typed Hopf–Delta Boundary Audit

This package performs a read-only, source-first audit of the proof obligations needed to derive Delta surjectivity for the EHP proof of `pi_12(S^7) = 0`.

The audit checks the reviewed GitHub `develop` lineage, the adopted Toda Proposition 5.9 evidence, typed Delta source/target groups, the existing independently required codomain and Delta-image premises, and the unchanged public incomplete proof frontier.

No production modules, registered inference rules, database entries, proof leaves, or narrative renderers are modified. A result printed in a reference and a database generator notation are not treated as certified proof steps. This is not a root-completion release.

## Run

Extract the ZIP at the repository root and execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r22_typed_hopf_delta_boundary_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r22_typed_hopf_delta_boundary_audit\run.ps1"
```

This script runs only focused pytest groups, not the full test suite. It stops on unreviewed Git lineage or modified tracked source files and does not check out, reset, or change production code.
