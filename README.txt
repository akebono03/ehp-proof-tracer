Phase 162 R7 - focused test runner path repair.
Only phase162_r7_connector_repair/run.ps1 is replaced.
R7 production implementation already applied by previous zip is not modified.
This script adds phase162_pi5_3_renderer_audit directory to PYTHONPATH and runs focused pytest without reapplying code.
Unzip in repository root and run:
powershell -ExecutionPolicy Bypass -File ".\phase162_r7_connector_repair\run.ps1"
