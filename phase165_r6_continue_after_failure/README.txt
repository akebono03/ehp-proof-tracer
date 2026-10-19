Phase 165 R6 - Continue full-suite diagnosis after failed batches

Purpose:
- Preserve all existing success/failure logs and state.json.
- Defer failed batch 28, continuing from batch 29 in the SAME audited 4223-node snapshot.
- Record other failures without treating them as PASS.
- Do not archive or modify any test or production code.

Install from repository root:
powershell -ExecutionPolicy Bypass -File .\phase165_r6_continue_after_failure\install.ps1

Continue remaining batches:
powershell -ExecutionPolicy Bypass -File .\phase165_r6_continue_after_failure\run.ps1

This launcher intentionally exits nonzero when ANY failure remains. This is not Phase closure. The original closure audit run.ps1 remains unchanged and can retry the failures later.

Ctrl+C safely interrupts; resume with the same command.
