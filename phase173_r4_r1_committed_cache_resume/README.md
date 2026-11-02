# Phase 173 R4-R1 — committed pytest-cache audit resume

This independent, **read-only** package resumes the Toda (5.6) proof-route audit
without modifying the existing committed R4-R1 auditor, production inference
rules, proofs, citations, or database goals. It accepts only the two reviewed
`develop` commits (2a3f37cf and f9fdaf35), the exact Phase 173 audit files
added after a7763513, and the committed change to `.pytest_cache/v/cache/nodeids`.

The working-tree gate additionally tolerates the unstaged pytest cache change
and the exact SHA-256 of three previously distributed R4-R1 audit corrections.
All other staged or unstaged edits are rejected. No Git reset, checkout,
restore, stash, clean, or write operation is performed.

From the repository root, extract the ZIP and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_committed_cache_resume\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_committed_cache_resume\run.ps1'
```

The report is stored in
`%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r4_r1_committed_cache_resume\audit.json`.
The `-DryRun` validates source and metadata, without exploring the runtime roots.
Only focused pytest is run (`-p no:cacheprovider`); full pytest belongs to
Phase 173 closeout. Observations are not completed ProofSteps.
