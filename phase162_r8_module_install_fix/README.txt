Phase 162 R8 missing module installation fix

The previous R8 ZIP updated web_group_proof.py but left phase162_pi5_3_web_replay.py inside its own package folder. Its tests accidentally imported the file from there, hiding the missing root module that the Flask server needs.

This repair installs ONLY phase162_pi5_3_web_replay.py into the repository root, preserving the current R8 web_group_proof.py and all other existing files. It validates the import from the repository root, and runs 4 focused regression tests. Full pytest suite is NOT run.

On Windows PowerShell in repository root:
Expand-Archive -Path "$HOME\Downloads\phase162_r8_module_install_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r8_module_install_fix\run.ps1"

Restart the Flask development server after a successful repair.
