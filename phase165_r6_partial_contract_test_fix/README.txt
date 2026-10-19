Phase 165 R6 limited test-contract repair.
Modifies only:
- test_phase165_r52_partial_proof.py: 2 whole test functions' assertions
- test_phase165_r52_r3_web_adapter.py: 1 whole test function's assertions
No production changes. Backs up originals and runs four targeted pytest cases.
Does not address the partial-narrative omission of observed ProofSteps, which remains open.
Run from an extracted package inside project root: powershell -ExecutionPolicy Bypass -File .\phase165_r6_partial_contract_test_fix\run.ps1
