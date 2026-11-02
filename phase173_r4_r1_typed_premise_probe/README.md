# Phase 173 R4-R1 — Typed Premise Probe

This package inspects the missing proof prerequisites for the Toda (5.6) direct-sum decomposition of `pi_7^4`. It does not modify production code, infer an unproved theorem, or add a `GIVEN`.

The audit checks the six historical Toda rule factories against the modern backward-rule registry; compares the public root both with and without a *hypothetical, never-verified* prior-structure input; and independently runs the existing `pi_7^7` group query to determine whether a proof is already available. The latter is a focused query, not the full test suite.

All reviewed mathematical sources are pinned to Git object hashes. The reviewed `f9fdaf35`, `6f5adde0`, and `c352f7d2` develop commits are accepted; unknown commits are rejected. Comparing `6f5adde0` to `c352f7d2` on GitHub verified that the only new files are the seven `phase173_r4_r1_frontier_readout/` audit artifacts. All pinned mathematical source blobs must remain identical, and staged/unstaged edits to them are rejected. Existing tracked and untracked changes are never reset or overwritten. Only the JSON report under `%LOCALAPPDATA%` is generated.

Run from the repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_typed_premise_probe\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_typed_premise_probe\run.ps1'
```

To skip the independent `pi_7^7` query, add `-SkipPi77Search`. The default runs that query.

The JSON report contains complete source text for six existing historical rule factories. `COMPLETE_PROOF_CERTIFIED=False` means this inspection has not proved the target decomposition.
