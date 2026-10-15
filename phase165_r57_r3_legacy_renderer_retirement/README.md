# Phase 165 R57-R3 — Legacy renderer retirement

This package removes the unused `render_toda_group_proof_generic_proof_markdown` function from the shared math helper module while leaving helper functions used by the public Narrative renderer intact. It replaces the historical R39 proof-specific, hard-coded Web narrative with a compatibility wrapper delegating to the current standard typed group-proof Web entry. The compatibility function preserves the old import name for callers but provides no alternative proof or rendering pipeline.

The canonical public narrative function remains `render_toda_group_proof_narrative_markdown`, with incomplete searches handled by the R57-R2 adapter. No theorem, generator, proof-search rule, or mathematical assertion is altered. The installer checks top-level production Python files for static references to the removed entry, validates the expected historical module shape, and makes backups before changes. It is idempotent.

Run `run.ps1` after expanding this package into the repository root. Five targeted test modules are collected. No full pytest is run. This is **not** full legacy-route removal: compatibility API and the older partial helper remain pending dependency and test migration, and the public renderer contains legacy specialized branches. Dynamic imports and subdirectory usages are not exhaustively audited.
