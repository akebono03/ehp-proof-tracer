# Phase 169 R3F2: packaging correction for focused pytest

This is a distribution/runner correction for R3F1. The production function payloads, mathematical rules, existing APIs, and test content are unchanged. The R3F1 ZIP did contain `tests/test_phase169_r3f_ehp_terminal_subgoals.py`, but `run.ps1` incorrectly referenced the nonexistent `tests/test_phase169_r3f1_committed_ehp_baseline_fix.py`. The runner now invokes the file actually included.

Extract the ZIP into the repository root and run from PowerShell:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3f2_test_path_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3f2_test_path_fix\run.ps1"
```

The runner verifies the package payloads and all focused test paths **before touching production files**. It then performs the same two-file guarded installation, limited pytest, real citation-screened EHP frontier audit, and guarded restoration on failure as R3F1.

Production targets are `phase165_r52_r9_shared_math.py` (`shared_expansion_provider`) and `phase165_r14_r5_ehp_connection.py` (new `expand_registered_ehp_terminal_goal` inserted before `audit_ehp_connection`). Both functions are included in full under `full_functions/`; module-level imports remain unchanged. Full modified source files are emitted in `output/*.full.py` on installation.

R3F2 only proposes typed prerequisite goals. It does not create GIVEN proof steps, infer proof completion, or alter citation eligibility. The `pi_5^3` proof stays partial until independent premises are reconstructed. Full pytest is intentionally deferred to the end of Phase 169.
