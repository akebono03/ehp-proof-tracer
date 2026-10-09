Phase 163 R1: read-only registration-site inventory

Unzip at the repository root and run:
  powershell -ExecutionPolicy Bypass -File .\phase163_r1_inventory\run.ps1

Outputs:
  phase163_r1_inventory_output\candidate_sites.csv
  phase163_r1_inventory_output\candidate_files.csv
  phase163_r1_inventory_output\summary.json
  phase163_r1_inventory_output\report.md

This scanner statically inventories candidates, not final distinct theorem counts.
It does not import project modules or execute registered proof builders.
It excludes historical phase patch folders and archive from the canonical scan.
Review any alternate active code locations manually.
