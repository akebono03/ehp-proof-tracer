Phase 162 R8 -- PowerShell pytest path repair

Changes only the runner, not production Python source.
The preceding runner accidentally embedded a literal tab in the path
between phase162_r8_module_install_fix and test_module_install.py.

Requirements:
- phase162_pi5_3_web_replay.py must exist in the repository root.
- phase162_r8_module_install_fix/test_module_install.py must already exist.

Run in Windows PowerShell from the EHP Proof Tracer repository root:

Expand-Archive -Path "$HOME\Downloads\phase162_r8_runner_path_repair.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r8_runner_path_repair\run.ps1"

Expected: 4 focused pytest cases; no repository-wide suite.
