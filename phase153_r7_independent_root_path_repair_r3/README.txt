Phase 153-R7 Independent Root Path Repair R3
============================================

Observed R7 failure
-------------------
The first structurally applied R7 patch left pi_5^2 and n >= 6 in the pi_6^2
proof body.

Cause
-----
The first R7 rule preserved a sibling premise whenever it had any consumer
outside the aggregate. Semantic closure can create such consumers even when
they do not provide an independent route to the final proof target.

Repair rule
-----------
For each unselected aggregate sibling premise:

1. temporarily exclude the aggregate step;
2. follow proof edges toward presentation.root_step;
3. preserve the sibling only if root remains reachable;
4. otherwise suppress its displayed proof-body occurrence.

This is a general Proof-graph relevance rule.

Changed production file
-----------------------
toda_group_proof_narrative_contribution_renderer.py

Added helper
------------
_phase153_r7_reaches_root_without_step()

Modified function
-----------------
suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry()

No n=2-specific or Proposition 5.6-specific branch is added.
No full pytest is run.

Run
---
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r7_independent_root_path_repair_r3" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r7_independent_root_path_repair_r3.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r7_independent_root_path_repair_r3\run_phase153_r7_independent_root_path_repair_r3.ps1"
