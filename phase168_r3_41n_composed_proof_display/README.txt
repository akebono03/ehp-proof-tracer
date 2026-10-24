Phase 168 R3-41N. Minimize redundant proof-step prose after R3-41M2.

Use Windows PowerShell at the repository root:
  Expand-Archive -Path "$HOME\Downloads\phase168_r3_41n_composed_proof_display.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41n_composed_proof_display\run.ps1"

The renderer and one existing R3-41L test file are modified. This update checks its
SHA-256, keeps a backup and restores both original files on failed validation.
The full pytest suite is NOT run. Upload output/review_bundle.zip afterward.
