# Phase 174 R3-R7-R46R1: reviewed R45 merge Source Guard fix

This ZIP applies a narrow, idempotent repair to the audit-only R46 Source Guard.
It preserves the production math and the canonical search engine, and does not
add any inference rules, source leaves, or public narrative variants.

The GitHub `develop` branch advanced one commit from
`4b06ef96628b39e591cfa0b423fa0e0dec366a3b` to
`4d37adab06b40330832c8ec1f08a1b7924ff95af`.
The 23 added files belong exclusively to the R45 and R45R1 audit packages.

Extract the ZIP at the repository root. Run
`powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r46r1_source_guard_merge_fix\run.ps1 -DryRun`
then run the same script without `-DryRun`.

The patch fixes only `phase174_r3_r7_r46_prop42_dfs_audit/source_guard.py`.
Both pre-merge local and merged local HEADs are accepted, but the upstream
HEAD and all source hashes remain strictly pinned.
