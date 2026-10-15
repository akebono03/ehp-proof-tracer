# Phase 165 R57-R26 — Generic Backward Search Connection

This package connects the R23 typed conclusion matcher, R24 registered candidate selection, and R25 typed premise generation to the existing shared `GoalExpansion` provider. The canonical recursive search and proof validation engine is unchanged. The Pi(4,3)-specific expansion remains active until R27. All generated expansions are unproven proposals and must pass the existing forward inference verifier.

From the repository root, extract the ZIP and run the included `run.ps1` script. The installer creates one backup and replaces only `shared_expansion_provider()`, installing the new generic provider module. Nine focused tests run. The full suite is deferred to the end of Phase 165.
