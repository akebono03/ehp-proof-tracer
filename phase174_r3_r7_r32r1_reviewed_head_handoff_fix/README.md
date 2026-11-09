# Phase 174 R3-R7-R32R1 — Reviewed R31 merge handoff fix

This is a minimal repair for the R32 checkout guard. The earlier R32 package
accepted only `25118e281445ca17b30c60c8fd02d00acaa25ea5`; GitHub `develop` now points to
`02f694b27a4239052bfa9d27a116fca6bbbff6b5`, which added only the R31 audit directory.

The reviewed local checkout may be at either commit while the remote must be
at the reviewed R31 merge commit. R31's `audit.py` must match its original
SHA256, and all R32 audited source file pins remain unchanged. The repair
never checks out, resets, pulls, fetches, or modifies the R31 directory.

Only two existing R32 files are replaced after exact SHA256 verification:
`phase174_r3_r7_r32_lower_delta_kernel_audit/audit.py` and
`phase174_r3_r7_r32_lower_delta_kernel_audit/run.ps1`. Full replacement
files are included in `replacement/` and the complete changed function and
imports are available in `CHANGED_FUNCTIONS_FULL.py` and `IMPORTS_FULL.txt`.

The original R31 HEAD-dependent regression checks cannot be run unchanged
after its merge. The R32 runner selects the eight reusable R31 regression
checks and preserves all R31 files unmodified. R32 and R5/R18 focused checks
are still run separately. No full test suite is run.

Extract under the repository root. From PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r32r1_reviewed_head_handoff_fix\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r32r1_reviewed_head_handoff_fix\run.ps1'
```

DryRun does not modify any file. The normal run installs the guarded patch,
runs the R32 source audit and focused tests. No mathematical inference,
GIVEN, proof provider, or certified conclusion is added. Root completion
remains unproved.
