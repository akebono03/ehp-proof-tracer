# Phase 168 R3-41F — Inline Citations on Incomplete Proof Steps

This patch preserves the exact citation numbers already attached to each ProofStep by the shared `ProofNarrativeModel` when rendering incomplete narratives. It does not create a reference, infer a mathematical proposition, or alter the certified Proof Tree.

## Scope

The sole implementation change replaces the entire `render_model_backed_narrative_markdown()` function in `phase168_r3_5_model_renderer.py`. Only the incomplete-result branch changes. No imports or other production files change.

The new focused tests check registered references plus rule citations, uncited steps, inference citations, rejected malformed citation maps, and a premise-closed prefix reconstructed from a real completed proof. The prefix is an **audit-only reconstruction** and not a genuine incomplete search result.

`run.ps1` takes complete and compatibility narrative snapshots before patching, applies a guarded replacement, runs focused tests, captures after snapshots, verifies byte-identical complete narratives and compatibility routes, and creates `output/review_bundle.zip`. On failure after patching, it restores the original file.

## Run

Extract the ZIP into the repository root and execute `phase168_r3_41f_inline_step_citations/run.ps1` from PowerShell. Requires earlier Phase 168 packages R3-41B1, R3-41C1, R3-41D1, and R3-41E.

The full test suite is intentionally not run until the end of Phase 168.
