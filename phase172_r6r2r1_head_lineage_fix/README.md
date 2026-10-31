# Phase 172 R6R2R1 — reviewed descendant HEAD correction

This correction repairs only the Git HEAD preflight of the previously supplied Phase 172 R6R2 document closeout installer. The Phase 172 R6 proof gate was completed at commit `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`. The subsequent `develop` commit adds only seven reviewed files under `phase172_r6_phase_closeout/`.

The replacement installer checks R6 commit ancestry, the exact seven changed paths and each reviewed Git blob. All five original document Git blob checks, the completed Renderer blob check, the prior R6 closeout JSON/full-test log, and the exact local/remote HEAD match remain mandatory. It does not rerun the full test suite or alter production code.

Run `run.ps1 -DryRun` before `run.ps1 -Apply`. On successful `-Apply`, the original document installer writes full revised contents of `README.md` and the four Japanese files under `docs/` into the local recovery folder, verifies document-only tests, and replaces only those documents. The correction script restores the original installer if any step fails; the document installer separately restores document originals on an apply failure. All operations are bounded to the reviewed source and previously completed phase gate.

The complete corrected installer and other added code are bundled as source files and printed in `CODE_FULL_JA.md`.
