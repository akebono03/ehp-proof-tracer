# Phase 176 Closeout R2 — repaired active suite

This package keeps the initial failed gate and the R1 repair unchanged. It requires the reviewed `develop` commit `7b4e071b735d8c309c2155c04c96869e7e774bdb`, a clean tracked checkout, and the original local failure and R1 collection evidence. R1 restored the Phase 175 active Python inventory by preserving four misplaced historical files as `.py.txt` archives. It collected 3546 tests without executing them.

Run `run.ps1 -DryRun`, then `run.ps1` from the repository root. The focused suites run before the single repaired active `tests/` execution. The gate refuses repeat attempts and retains stdout/stderr, report, and the earlier evidence hashes. No test exclusions, mathematical rules, proof providers, GIVEN registrations, or production renderers are changed. The final count must match the 3546 collected tests exactly. The four previously known historical Phase 174 source-guard failures remain outside this active scope and are not claimed as passing.

Only a successful final gate writes all five complete Markdown documents and the verified ZIP under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_closeout_r2/`. Original files are backed up and the initial failure and R1 repair are recorded in the updated documents. Do not remove previous attempt files or repeat a failed R2 run automatically.
