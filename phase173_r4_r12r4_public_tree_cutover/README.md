# Phase 173 R4-R12R4 — Public Proof-Model Narrative Cutover

This patch removes the post-render, dimension-specific narrative override from the public Web adapter. It does not modify proof search, any ProofStep, the source registry, group structures, the central model renderer, or the historical projector APIs.

The package updates exactly three tracked files: `phase165_r52_r3_web_adapter.py` (full file), `phase173_r4_r13_narrative_audit/audit.py` (the full `inspect_dimension` function), and `phase173_r4_r13_narrative_audit/tests/test_audit.py` (full file). It adds focused structural and live public-contract tests under its own directory.

## Requirements

Run from the root of a local checkout of `akebono03/ehp-proof-tracer`, on branch `develop`. Local and `origin/develop` must match. The baseline commit is `188f707e1fcd8fde7b22af02a6b4005986fb3c1e`; a descendant is accepted only if commits since the baseline touch `phase173_r4_r12r3_architecture_audit/` or `.pytest_cache/v/cache/nodeids`. The observed `382cef8b866351b14fe1e717a283e50dc6f24555` is such a descendant. Any other intervening change is refused. All three reviewed target files must match their pinned Git blobs. An already modified pytest cache is allowed. Other unrelated tracked modifications and staged changes are rejected.

## Execution

First run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r12r4_public_tree_cutover\run.ps1 -DryRun`, then run the same command without `-DryRun`.

The normal execution performs a guarded, complete-function patch followed by focused pytest. If focused pytest fails after applying the patch, the runner attempts to restore the three reviewed tracked files from the pinned HEAD. It never creates commits or modifies the user's proof data.

## Limits

This is one bounded migration step, not the final architecture gate. The central model renderer still has an n=4-specialized prose branch to be audited separately. The dormant historical projectors and source-first proof rules remain unchanged. The five previously verified groups must continue to have completed certified roots; `pi_12^4` is not promoted. The full pytest suite is reserved for the end of the Phase.

## R4-R12R4R1 head lineage correction

The original R4-R12R4 DryRun was blocked because the preceding read-only audit had been committed after package review. This update modifies only the installer guard and its own focused tests, not any production fixture or target. In addition to the original three fixture tests, two new tests verify that audit-only descendants are accepted and renderer changes are rejected. An already applied worktree is checked by the same guarded loader.
