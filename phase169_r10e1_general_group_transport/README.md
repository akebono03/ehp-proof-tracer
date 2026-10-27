# Phase 169 R10E1 — Structure-Neutral Stable Transport

This package adds a typed Toda (4.5) stable-transport inference supporting zero groups, finite cyclic groups, free cyclic groups, and finite direct sums of finite/free cyclic groups. It does **not** add a theorem, treat a database entry as a proof, or automatically certify generators.

The new generic rule requires an earlier, publication-eligible source-group assertion, a proved Toda (4.5) isomorphism, and independently proved one-step image witnesses for **every** generator in a nonzero group. The zero-group variant requires no generator image witnesses. Direct-sum components must correspond in order and type; unsupported summand types, reordered components, mismatched orders, and unchecked generator names fail closed.

## Installation and focused verification

From the Windows repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10e1_general_group_transport.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e1_general_group_transport\run.ps1"
```

The runner requires the `develop` branch and the existing R7, R10B and R10D2 installation. It patches only the `shared_expansion_provider()` function in `phase165_r52_r9_shared_math.py`. The complete modified function and complete modified production file are written to `output`; an independent backup is kept there, and failures during focused checks trigger restoration. Other application files and existing tests are not patched.

The finite-cyclic provider continues to use the proven R7 public API for backward compatibility. The new general rule itself also supports finite cyclic groups; the common provider dispatches all supported shapes through one entry point. No stem-specific branch is added.

## Boundaries

* Group-shape support is not proof-source availability. The R10E0 audit reported unresolved **target citation IDs** for all five sample goals, so `ELIGIBLE_PRIOR=0` must not be interpreted as a reliable count of mathematically unavailable predecessors.
* Zero-group transport requires a previously cited zero statement, not just a zero-valued CSV row.
* The earliest stable group (`n=k+2`) has no lower stable-domain predecessor.
* A nontrivial generator identity must still be derivable from a cited family definition. `HyoujiGen.csv` provides identity/type metadata only.
* The copied Toda transcription's order is not an independently verified publication order of the original edition.
* The full pytest suite is intentionally deferred until the end of Phase 169.
