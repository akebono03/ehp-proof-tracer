Phase 161 real proof execution - RepositoryProofScopeResult API fix

Changes from prior import-fixed audit:
- Iterate over scope.nodes, not the RepositoryProofScopeResult object.
- Compute number of nodes with len(scope.nodes).

No changes to production files, existing rules, tests, or selection behavior.
This is a read-only audit using six real candidate premises from the Production proof scope.
It does not prove autonomous goal-driven rule discovery.

Windows PowerShell:
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase161_real_proof_execution_scope_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase161_real_proof_execution_scope_fix\run_phase161_real_proof_execution.ps1"

Output: phase161_real_proof_execution.json
