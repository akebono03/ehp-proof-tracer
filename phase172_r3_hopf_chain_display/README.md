# Phase 172 R3 — Verified Hopf-Chain Presentation

This package shortens the rendered proof of a previously verified right-Hopf composition relation. It does not change proof search, mathematical rules, proof steps, the trust boundary, or references. It does not construct new facts or synthetic GIVEN steps.

## Reviewed baseline

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed Renderer Git blob: `bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95` (committed Phase 172 R2).
- Reviewed R2 projection Git blob: `bba6280a36ca1c094be1b2a65d94ba0d2582c7a1`.
- Phase 172 R3R1R1 audit: `PASS_CORRECTED_R3R1_AUDIT`, canonical proof complete, 50 ProofSteps, 8 references, and zero open goals.

## Installation

Extract the ZIP in the **repository root**. From Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase172_R3_VERIFIED_HOPF_DISPLAY.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r3_hopf_chain_display\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r3_hopf_chain_display\run.ps1" -RunFocusedTests
```

The dry run writes the complete replacement `render_model_backed_narrative_markdown()` function and the complete modified Renderer source to a fresh external directory under `%LOCALAPPDATA%\EHPProofTracerRecovery`. It never alters the repository.

The full run modifies only `phase168_r3_5_model_renderer.py` among existing tracked production files, after exact Git blob and function-anchor checks. If any focused test fails, its original bytes are restored. The new projection module and tests are installed by extracting the archive.

## Presentation contract

For a fully verified proof tree with exactly the right-Hopf premise graph, the projector keeps the cited suspension relation, the proved Proposition 2.2 application, the cited Hopf-generator image, and the final proved Hopf image. Only five uncited intermediate inference sentences are hidden from the prose. The actual proof graph, all direct citations, and the final cyclic group proof remain unchanged. Unrecognized or untrusted cases retain the previous full narrative.

Five focused pytest groups cover the new behavior and existing Phase 172 R2, Phase 171, and Phase 169 narratives. No full-suite pytest is run; the full suite is reserved for Phase 172 closeout.
