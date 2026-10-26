# Phase 169 R3F3 — Focused-test collection repair

This package retains exactly the R3F2 production function payloads, typed inference contracts, provenance checks, and runtime audit. It corrects the focused-test list. The formerly selected `phase161_r4_literature_premise_matching/tests/test_phase161_r4_literature_premise_matching.py` imports `tests.test_phase59_n3_ehp_chain`, which is no longer in the current repository, causing pytest collection to fail before tests run.

R3F3 runs the new R3F eight-test module, the existing Phase 165 R14-R5 adapter tests, and the existing Phase 161 R3 EHP backward-expansion tests. The previous Phase 169 R3E test module is also excluded because its test `test_historical_endpoints_are_not_given_by_connection` explicitly expects zero terminal proposals, which is the behavior R3F is changing. The R3F runtime audit verifies both terminal proposals in the real citation-screened context and preserves the `INFERENCE` premise requirement. No full test suite is run.

## Windows PowerShell

Extract `phase169_r3f3_focused_collection_repair.zip` to the repository root, then run:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3f3_focused_collection_repair.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3f3_focused_collection_repair\run.ps1"
```

The runner checks all payload and selected test paths before patching, guards the committed R3E1 Git blob baseline, writes backups and full resulting modules to `output/`, runs focused pytest, and runs the actual screened EHP frontier audit. On failures after patching, it restores the two modules only if their bytes still match the package's generated versions. The baseline must still match Git HEAD; unknown local edits are refused.

## Production targets and boundaries

- `phase165_r52_r9_shared_math.py`: the complete `shared_expansion_provider()` function is in `full_functions/shared_expansion_provider.py`.
- `phase165_r14_r5_ehp_connection.py`: the new `expand_registered_ehp_terminal_goal()` function is in `full_functions/expand_registered_ehp_terminal_goal.py`, inserted immediately before `audit_ehp_connection()`.
- Module-level import sections are unchanged; local imports are in the complete function payloads.
- New and existing tests are not modified. All eight added test functions are in `tests/test_phase169_r3f_ehp_terminal_subgoals.py`.

The source claim `Proposition 5.1` is required as an independently reconstructed `INFERENCE`, not accepted as a plain `GIVEN`. The relation $H(\nu')=\eta_5$ is a pending goal, not a newly asserted fact. The $\pi_5^3$ proof remains partial until every premise is actually derived. This package does not implement Phase 169 R3G or change any project-level documentation. Run the full pytest suite only at the end of Phase 169.
