# Phase 173 R4-R1 — Read-Only Frontier Readout

This package reads the existing `phase173_r4_r1_committed_cache_resume/audit.json` report from `%LOCALAPPDATA%`. It makes no changes to tracked project files, proof rules, references, or Git state.

Extract the ZIP into the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_frontier_readout\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_frontier_readout\run.ps1'
```

The script runs only its focused tests, with pytest's cache provider disabled, and then prints the source, prior-result, and proposal status. Results are observations, not new proof steps. No full pytest suite is run.
