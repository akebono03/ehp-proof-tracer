# Phase 169 R10ET-R3B — Reviewed-HEAD Re-run

This is an audit-only re-run of the R10ET-R3 cyclic-definition projection experiment. R10ET-R3 initially refused to execute because the repository HEAD had advanced from `a5892721` to `085b58cf`. A GitHub commit comparison confirmed that the new `10et1` commit only adds R10ET-R2 audit files and outputs; no application code or relevant existing tests changed. The subsequent `c63ca5d` commit only adds the R10ET-R3 audit package. The shared provider Git blob SHA remains `61cbadb06f770c51a9c1f5a3c8026acf9e14aa` on all three reviewed commits.

The **only functional difference** from R10ET-R3 is the strictly enumerated `REVIEWED_HEADS` guard. The actual proof-search and projection experiment is unchanged. The package is in its own directory, so neither committed code nor the previous R3 audit package is overwritten. It retains the `develop` branch, exact shared-provider blob, and clean tracked worktree/index requirements. It does **not** execute `git reset`, `git checkout`, or any production patch. In-memory overrides are restored in `finally` blocks.

Unpack into the repository root and run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase169_r10et_r3b_reviewed_head_guard\run.ps1`. The R10ET-R1, R10ET-R2, and R10ET-R3 packages must already be present. `-Cases focus` limits the sample to four groups; the default is `all`. `-SkipTests` skips focused tests but not the audit.

Outputs are stored under `output/<timestamp>/audit.md`, `audit.json`, and group narratives. A zero audit exit means trustworthy completion and unchanged tracked files; it does not imply all presentation invariants passed. Review `CYCLIC_RECOVERED`, `DIRECT_SUM_PRESERVED`, and `ORPHAN_PREFIX` separately. The full pytest suite is not run.
