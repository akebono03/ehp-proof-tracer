# Phase 174 R3-R7-R46 — Cited Proposition 4.2 and Depth-First Search Audit

This is a read-only audit. It investigates why R45 found all four public Proposition 4.2 specialization candidates but observed no certified proof steps under a bounded root-first search. It separately runs genuine canonical recursive proof search for each exactness window and for the lower image-kernel consequence. These isolated subproofs do not certify the final group.

Requirements: the reviewed `develop` HEAD `4b06ef96628b39e591cfa0b423fa0e0dec366a3b`, the untracked R45 audit folder, and the R45R1-reviewed runner and test replacements.

Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r46_prop42_dfs_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r46_prop42_dfs_audit\run.ps1"
```

Output: `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r46\prop42_dfs_audit.json`.

No production module, registry, renderer, database, source or mathematical rule is modified. No new GIVEN is registered. The runner executes only focused pytest groups; no full-suite tests are performed.
