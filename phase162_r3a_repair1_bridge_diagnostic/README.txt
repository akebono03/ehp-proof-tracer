Phase 162 R3-A bridge mismatch diagnostic (no mathematical modification).

Run from repository root:
Expand-Archive -Path "$HOME\Downloads\phase162_r3a_repair1_bridge_diagnostic.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r3a_repair1_bridge_diagnostic\run_phase162_r3a_bridge_diagnostic.ps1"

The script writes phase162_r3a_bridge_diagnostic.json even if focused pytest fails. Compare actual_bridge with planned_bridge. R2 production files are not overwritten.
