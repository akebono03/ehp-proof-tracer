# Phase 174 R3-R7-R44: canonical zero-image frontier

This read-only audit separates the mathematically different goals `E pi_10^5 = 0` (zero image of suspension) and `pi_10^5 = 0` (zero group). It attempts a bounded reconstruction of the public R43-to-R41 source-backed inference chain through the established recursive proof-search API, without adding a rule, a GIVEN leaf, or a renderer exception.

## Requirements

Run from the `develop` repository, with the reviewed R43 completion present. The source guard accepts exactly the merged R43 commit or its exact unmerged production patch. Other tracked or staged edits are rejected.

## Running

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r44_public_zero_image_tree_frontier\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r44_public_zero_image_tree_frontier\run.ps1
```

The JSON reports are written under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r44`. A successful audit does not claim a verified final root, does not make an HTTP request, and does not replace a complete Web proof search. Full pytest is explicitly excluded.
