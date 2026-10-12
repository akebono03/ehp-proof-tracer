Repository Cleanup R2: conservative read-only audit.
Run from EHP Proof Tracer project root:
  Expand-Archive -Path "$HOME\Downloads\repository_cleanup_r2.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\repository_cleanup_r2\run.ps1"
Requires R1 CSV at repository_cleanup_r1_output/inventory.csv.
Writes only repository_cleanup_r2_output reports. Does not delete files or execute pytest.
Optional focused script self-test: python -m unittest repository_cleanup_r2/test_r2_audit.py
