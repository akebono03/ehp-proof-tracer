Repository Cleanup R4 - Final check (read-only, targeted pytest only)

From the EHP Proof Tracer project root:
  powershell -ExecutionPolicy Bypass -File .\repository_cleanup_r4\run.ps1

Requires R3 outputs and Phase 163 R95/R94/R91/R92 artifacts.
Runs only the four R95 test files plus three verifier tests.
Does not run full pytest. Does not delete or modify project source.
Outputs: repository_cleanup_r4_output/r4_report.md, r4_summary.json, r4_targeted_pytest.log
A pre-existing Git tracked modification is not treated as cleanup damage unless the status changes during this run.
