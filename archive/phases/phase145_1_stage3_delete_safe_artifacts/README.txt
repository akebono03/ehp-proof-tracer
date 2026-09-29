Phase 145-1 Stage 3 - Delete Audited A_SAFE_DELETE Artifacts

Scope
-----
Delete exactly the 28 artifacts classified A_SAFE_DELETE and reviewed in
Phase 145-1 Stage 2.

Safety
------
- Exact target allow-list; no wildcard deletion.
- Requires HEAD:
  3bcb84fe687ace64f15859df1f9dcb5da7113266
- Requires all 28 targets to exist and contain tracked files.
- Allows the already staged working-tree deletions from Stage 1 only when
  their paths have backup markers.
- Allows only the Phase 145-1 helper directories as untracked content.
- Does not touch B_REVIEW or C_SAVE artifacts.
- Does not modify production code, canonical tests, or formal docs.
- First run is dry-run; deletion requires typing YES.

Run
---
From the repository root:

powershell -ExecutionPolicy Bypass `
  -File ".\phase145_1_stage3_delete_safe_artifacts\run_phase145_1_stage3.ps1"

Testing
-------
No pytest is run in this stage because only audited obsolete artifacts are
removed. Repository-wide pytest remains reserved for the end of Phase 145.
