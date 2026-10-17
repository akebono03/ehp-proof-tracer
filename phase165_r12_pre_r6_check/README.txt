Phase 165 R12 pre-R6 read-only verification

Install by expanding the ZIP into the EHP Proof Tracer repository root.
Then run the PowerShell script from the repository root:
  powershell -ExecutionPolicy Bypass -File .\phase165_r12_pre_r6_check\run.ps1

No production files are replaced. The script inspects exact rule patterns,
checks whether the R5 goal reaches the R2 rule, and runs only focused pytest.
It DOES NOT check citation-backed source witnesses and DOES NOT certify pi_4^3.
