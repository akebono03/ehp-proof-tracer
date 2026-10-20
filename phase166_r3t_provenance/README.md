# Phase 166 R3-T: Specialized Goal Provenance Audit

This read-only package identifies the fixed typed assertions that contain or specialize into the group goal for pi_5^4, and checks whether the previously registered pi_4^3 statement is admitted under each candidate source's publication ordering.

No production code is patched. No proof tree is reused as a reference. No full test suite is run.

From the repository root run `powershell -ExecutionPolicy Bypass -File .\phase166_r3t_provenance\run.ps1`.

See `audit_result.json` for the actual assertion IDs and publication positions. Do not create an artificial assertion ID as a workaround.
