# Phase 173 R4-R12 — Verified Toda Proposition 4.4 narrative

This package adds one source-and-proof-tree-verified narrative projector, shared by the proven n=4 targets. The reviewed pi_7^4 wording is preserved through the original projector. The projected pi_8^4 through pi_11^4 proofs display the general source theorem, concrete specialization, map, actual source groups, generator correspondence, and authentic model-backed references. Nothing here proves a group or generates an uncited source.

The installer changes only `phase165_r52_r3_web_adapter.py`, replacing the entire `build_partial_web_group_proof_view` function with the reviewed function in `web_adapter_FULL.py.txt`. The existing module imports are unchanged. The R4-R11 proof-search patch is preserved exactly. The narrow test suite runs before the installer writes the production file. A final Web regression runs after installation.

Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r12_common_narrative\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r12_common_narrative\run.ps1"
```

No global test suite is run. Do not mark Phase 173 complete based on this package.
