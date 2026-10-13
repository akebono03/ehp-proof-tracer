Phase 165 R52: Generic Partial Proof Result Model

Run from the repository root:
Expand-Archive -Path "$HOME\Downloads\phase165_r52_generic_partial_proof.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r52_generic_partial_proof\run.ps1"

Adds a separate shared model and Markdown rendering entry point.
It does not modify the existing Web route or existing goal search function.
Callers must supply actually proven ProofStep objects; the model does not certify them.
Only targeted pytest is run. No 112-group ceiling.
