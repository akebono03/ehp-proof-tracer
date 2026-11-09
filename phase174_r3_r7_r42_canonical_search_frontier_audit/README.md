# Phase 174 R3-R7-R42: Canonical Search Frontier Audit

This is a **read-only**, source-pinned audit of the bridge from the R41 public
zero-image candidate to the original EHP zero-group root. It changes no
production file, mathematical rule, or result database.

It deliberately distinguishes three things:

1. A public backward `GoalExpansion` for the suspension zero image.
2. A certified, separately adopted DB prior usable for the actual group root.
3. A canonical proof search which needs a connected upper Delta-surjectivity
   provider and correctly scoped DB-prior admission.

The `search_registered_partial_proof` calls in this audit use **explicitly
filtered public expansions** to isolate the root and zero-image boundaries.
They are *not* an HTTP probe or an exhaustive simulation of all Web proposals.
No final proof or user-facing completion is claimed.

## Running from the repository root

Unpack `R42.zip` at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r42_canonical_search_frontier_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r42_canonical_search_frontier_audit\run.ps1"
```

The script runs only focused pytest groups. The complete test suite remains
reserved for the final gate of Phase 174.
