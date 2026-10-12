Repository Cleanup R3 (cache-only deletion)
Run from EHP Proof Tracer root:
  powershell -ExecutionPolicy Bypass -File .\repository_cleanup_r3\run.ps1
Uses R2 generated CSV from repository_cleanup_r2_output.
Only untracked, unchanged regenerable cache files from that allowlist are eligible.
No Python code, source archives, evidence, backups, or tests are deleted.
To preview without deleting:
  python .\repository_cleanup_r3\r3_cleanup.py --project .
Output: repository_cleanup_r3_output/r3_report.md, r3_summary.json, r3_deleted.csv, r3_skipped.csv
