# Phase 169 R3F — EHP Terminal Subgoals

This package extends the current typed backward-search provider without granting any new proof facts. It adds a narrowly scoped backward connection for the two existing $n=3$ EHP terminal inference rules. The corresponding requirements remain **unproved subgoals**. The original `ProofRule.INFERENCE` premise patterns are preserved, and the code never constructs a `ProofStep`, adds a `GIVEN`, or marks $\pi_5^3$ complete.

## Prerequisite

R3E1 must have been successfully applied, and its extracted directory must remain in the repository root. The installer compares the complete current `shared_expansion_provider()` function with the reviewed R3E1 version. The current HEAD versions of both production files must match their reviewed Git blobs.

## Modified production files

- `phase165_r14_r5_ehp_connection.py`: insert `expand_registered_ehp_terminal_goal()` immediately before `audit_ehp_connection()`; the existing adapter is unchanged.
- `phase165_r52_r9_shared_math.py`: replace the entire `shared_expansion_provider()` with the version in `full_functions/shared_expansion_provider.py`. No module-level imports are changed.

`full_functions` contains the complete affected functions. The installer writes the full updated module contents into the package `output` directory when applying.

## Run

Extract the ZIP at the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase169_r3f_ehp_terminal_subgoals\run.ps1`.

The run performs guarded installation, focused tests, and an actual citation-screened EHP frontier audit. If validation fails, it restores both production files only if they still exactly match the files written by the installer. It does not run the entire test suite.

The audit report is `output/ehp_terminal_frontier.json`.

## Intended boundary

A rule proposal is not a proof. In particular, the historical terminal rules require **INFERENCE** witnesses for the Proposition 5.1 composite and the Hopf relation $H(\nu')=\eta_5$. A screened source GIVEN alone cannot discharge these premises. The next step must prove the remaining subgoals using individually eligible earlier mathematical statements.
