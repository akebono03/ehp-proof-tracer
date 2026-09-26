Phase 143-73A

Changes:
- toda_group_proof_narrative_renderer.py
- tests/test_phase143_73a_internal_statement_narrative.py

Run from repository root:

Expand-Archive `
  -Path "$HOME\Downloads\phase143_73a.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase143_73a\apply_phase143_73a.ps1"

$env:PYTHONPATH = (Get-Location).Path

pytest -q `
  ".\tests\test_phase143_73a_internal_statement_narrative.py"

Remove-Item Env:PYTHONPATH

Do not run the full suite yet.
