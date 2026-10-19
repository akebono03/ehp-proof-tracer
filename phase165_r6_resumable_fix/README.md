# Phase 165 R6 — Resumable test execution

This package replaces **only the R6 execution wrapper**. It does not modify proof search, narrative rendering, tests, or the frozen R4 baselines.

## Install and run

Unpack this ZIP at the repository root. From PowerShell:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r6_resumable_fix.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r6_resumable_fix\run.ps1"
```

The wrapper rechecks R3 and R4, collects pytest test IDs using pytest itself, and runs the collected suite in groups of 25 test items. Live output is printed and appended to `phase165_r6_audit_results/full_pytest.log`. Results for each finished group are atomically recorded in `resume_state.json`, and test IDs are saved in `collected_nodeids.json`.

Press **Ctrl+C** to stop. A group interrupted during execution remains incomplete. Run the same PowerShell command to resume the remaining groups. A finished failed group remains recorded as a failure; rerunning does not silently turn it into a pass. Each restart reruns the inexpensive R3/R4 tests before continuing the full suite.

Log files: `r3_pytest.log`, `r4_pytest.log`, `collection.log`, `full_pytest.log`, `resume_state.json`, `collected_nodeids.json`, and `audit_result.json`.

## Important limitations

- The collected test inventory is frozen for one run. If repository test files or collection settings change, do not resume from the old inventory. Archive or remove the prior `phase165_r6_audit_results` directory and start a fresh run.
- Executing groups as separate pytest processes is **not identical to one monolithic invocation**, especially for session-scoped fixtures or global test state. Treat the result as a segmented full-suite audit, not proof of a single-process full pytest pass.
- Ctrl+C best-effort stops the current child process; hard termination or a crash may leave an incomplete last log entry, but completed groups remain recorded.
- The browser and MathJax/KaTeX view must still be checked manually; this package does not certify HTML rendering.
- A failed group is not automatically re-run. Inspect its log and investigate before deciding to start a fresh audit.
