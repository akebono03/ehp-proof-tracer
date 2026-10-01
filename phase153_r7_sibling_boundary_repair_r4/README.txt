Phase 153-R7 Sibling Boundary Repair R4
======================================

Observed after R3
-----------------
R3 removed the unrelated group-result siblings from the pi_6^2 body, but
the range premise n >= 6 remained.

Why
---
n >= 6 is also used inside the unselected higher-nu sibling branch.

R3 excluded only the aggregate step during root reachability analysis, so a
path through another unselected sibling branch could still make n >= 6 look
independently relevant.

R4 general rule
---------------
For one unselected aggregate sibling:

1. exclude the aggregate step;
2. also exclude every other unselected direct sibling step;
3. test whether the current sibling can still reach presentation.root_step;
4. preserve it only when such an independent path exists.

This prevents internal cross-links between unselected sibling branches from
making branch-only premises visible.

Production change
-----------------
toda_group_proof_narrative_contribution_renderer.py

Renamed/replaced helper:
_phase153_r7_reaches_root_without_steps()

Modified:
suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry()

No n=2-specific or Proposition 5.6-specific branch is added.

Run
---
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r7_sibling_boundary_repair_r4" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r7_sibling_boundary_repair_r4.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r7_sibling_boundary_repair_r4\run_phase153_r7_sibling_boundary_repair_r4.ps1"

Full pytest remains deferred until the end of Phase 153.
