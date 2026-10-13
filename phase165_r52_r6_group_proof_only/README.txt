Phase 165 R52-R6: Group proof only view

Purpose: Hide non-group tools and the extra Group proof progress form.
Visible: EHP Proof Tracer title, Group query, group calculation result, Group proof.
The existing n/k query, Phase 165 registered proof, ProofStep, Reference,
Flask routes and mathematical renderer are NOT modified.

Installation from the repository root:
  Expand-Archive -Path "$HOME\Downloads\phase165_r52_r6_group_proof_only.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r6_group_proof_only\run.ps1"

To show all tools again:
  powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r6_group_proof_only\restore.ps1"

Changed project file: templates/index.html only.
Added project file: test_phase165_r52_r6_group_proof_only.py.
No source Python methods, imports or classes are changed.
No full pytest until the end of the phase.
