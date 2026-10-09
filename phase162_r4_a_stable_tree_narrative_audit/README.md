# Phase 162 R4-A: stable proof-tree / narrative comparison audit

This package is read-only. It compares the public narrative path with the existing Phase 158 baseline using the same `TodaGroupProofPresentation` for `pi_5^4`. The baseline performs semantic closure; therefore its output is **not** represented as a raw `ProofStep` rendering.

From the repository root, expand the ZIP and run:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase162_r4_a_stable_tree_narrative_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r4_a_stable_tree_narrative_audit\run_phase162_r4_a.ps1"
```

Artifacts are saved in `phase162_r4_a_stable_tree_narrative_audit/audit_output/`: `comparison.md`, `audit.json`, `public.md`, and `baseline.md`.

The classification is diagnostic, not a formal proof of semantic ancestry. Examine exact conclusions and edges before deciding which component requires a change in R4-B. No production file is modified. The runner executes focused tests only.
