# Phase 162 — Group-Structure-First Backward Reconstruction

This patch adds an evidence-driven finite cyclic group-structure transport inference on top of the existing seven-inference EHP suspension-isomorphism reconstruction. It does **not** alter the Phase 161 inference rules, existing APIs, or web rendering.

## Install and run (Windows PowerShell)

From the root of your EHP Proof Tracer repository:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase162_group_structure_backward.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_group_structure_backward\run_phase162_group_structure_backward.ps1"
```

## Changes

- New `phase162_group_structure_backward.py`: `GroupStructureBackwardPlan`, `GroupStructureBackwardResult`, `_transport_conclusion`, `_transport_guard`, `group_structure_transport_inference_rule`, `expand_group_structure_goal`, and `reconstruct_group_structure_goal`.
- New `tests/test_phase162_group_structure_backward.py`: six focused checks for the root conclusion, seven existing inferences, and rejection of missing/mismatched premises.
- `run_phase162_group_structure_backward.ps1`: copy the complete files to the repository and run focused tests only.

## Important boundaries

- The source cyclic group structure and generator image are **required external evidence** (`ProofStep` objects); they are not manufactured by this patch. Test fixtures use explicitly trusted premises solely to isolate the transport inference.
- The existing Phase 161 reconstruction is restricted to `E: pi_4^2 -> pi_5^3`; this patch does not claim arbitrary-stem search capability.
- Web narrative integration and independently verifying authentic source proof records are **not yet implemented**. This patch is a first implementation slice and **does not close Phase 162**.
- Only a syntax compilation was possible in the build environment. Run the included focused pytest against your repository before accepting the patch.
