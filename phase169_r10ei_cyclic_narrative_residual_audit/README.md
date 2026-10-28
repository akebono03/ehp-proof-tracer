# Phase 169 R10EI — Cyclic Narrative Residual Audit

This is a **read-only, focused audit** for the proof-complete 6-stem and 10-stem examples. It never edits the proof engine, production renderer, existing tests, literature sources, or database.

Targets are `pi_28^22` and `pi_32^22`. The audit re-runs canonical proof search, replays the Trust Boundary, and identifies the remaining displayed one-step suspension equations after R10A presentation compression. It records duplicate displayed formulas and the actual typed ProofStep candidates associated with each formula, including consumers and citation ancestry.

**A text match is diagnostic only.** It is not a proof of equality between ProofSteps or permission to remove either proof or a separately cited statement.

## Run (PowerShell, repository root)

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10ei_cyclic_narrative_residual_audit.zip" -DestinationPath . -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10ei_cyclic_narrative_residual_audit\run.ps1"
```

The runner checks the reviewed Git ancestry and exact committed source blobs, runs only the new focused tests, and stores its JSON, Markdown and original proof prose in a newly named `output/run_*` directory. It does not overwrite existing tracked reports. A difference in existing tracked-file status is reported without performing a reset or checkout.

## Scope

In scope: evidence inventory and residual narrative diagnosis for two already-complete cyclic targets. Out of scope: changing compression behavior, resolving incomplete 11-stem or 14-stem proof goals, modifying source or inference rules, and repository-wide pytest.
