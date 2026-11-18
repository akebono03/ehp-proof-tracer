# Phase 175 R4R12R1R1 — Tracked pytest Cache Guard Fix

This is a replacement for the previous R4R12R1 correction overlay. It retains
the reviewed-HEAD and historical-prior-report corrections and corrects a
preflight allowlist mismatch: the existing R4R12 audit permits the tracked
`.pytest_cache/v/cache/nodeids` test cache, while the earlier correction did not.

Only that exact cache path and `phase165_r52_r9_shared_math.py` are accepted
as tracked modifications. All other tracked modifications remain rejected,
with the rejected paths included in the error. The Git HEAD and ancestry
checks remain mandatory. No tracked source is modified by this overlay
except the previously planned R4R12 installer/audit correction (untracked
package files) and the original R4R12 installation if explicitly run.

Extract the ZIP in the repository root, then execute:
`powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r1r1_tracked_cache_guard_fix\run.ps1 -DryRun`
Follow with the same command without `-DryRun`.

The runner executes only focused tests; project-wide pytest is not run.
