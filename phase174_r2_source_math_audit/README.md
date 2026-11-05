# EHP Proof Tracer — Phase 174 R2 Source-first Mathematical Audit

This audit compares Toda's source text for (4.8), Lemma 5.4,
(5.5), (5.6) and Proposition 5.6 with the existing type-safe
backward-search root proposals for the public query `pi_8^5`.

The (4.8) quotient formula is **conditional** on Delta(iota_7)=0.
Its source appearance does not establish that premise automatically.
The relation `2 nu_5 = E^2 nu_prime` is stated in (5.5), but must be
reconstructed with an independently verified typed inference path.

The audit reads the confirmed Phase 174 R1 report from LOCALAPPDATA,
preserves every open goal and abstract certificate classification,
records source text and source-screened root proposals, and explicitly
grants no new proofs.

It does not edit production sources, tests, registries, citations,
or the five project documents. It does not run the full pytest suite.
Its only persistent output outside the extracted package is
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r2\audit.json`.

From the repository root, extract the ZIP and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r2_source_math_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r2_source_math_audit\run.ps1"
```

Both local and remote `develop` must match the reviewed commit. The
reviewed replacement test from R1R1 must already be installed. This audit
never pulls, checks out, resets, cleans, commits, or pushes Git state.

The next phase (R3) may add rules only after the required sources,
premises, types, and public search boundaries have been reviewed.
