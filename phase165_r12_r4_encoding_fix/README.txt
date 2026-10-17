Phase 165 R12-R4 encoding fix

This patch replaces only the existing R12-R4 audit.py and run.ps1, plus adds one targeted test module.
The worker emits UTF-8 via PYTHONIOENCODING, and binary subprocess pipes are decoded explicitly.
CP932 and malformed bytes do not crash the audit. Search errors remain reported as errors.
No mathematics, registry, or proof logic is changed. No full pytest.

Execute from project root:
Expand-Archive -Path "$HOME\Downloads\phase165_r12_r4_encoding_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r12_r4_pi43_search\run.ps1"
