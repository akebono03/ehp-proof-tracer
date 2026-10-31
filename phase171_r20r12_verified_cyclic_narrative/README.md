# Phase 171 R20R12 — Verified cyclic narrative projection

This focused phase changes only the narrative renderer. It displays the already
certified short exact sequence, finite cardinality, nonzero double, and order-four
generator conclusion. It does not add new proof rules, GIVEN statements,
completed proof trees, or search shortcuts.

The patch is guarded by the reviewed Git blob of the current renderer, permits
unrelated uncommitted changes, and preserves the renderer's line-ending style.
Use `run.ps1 -DryRun` first and then `run.ps1`. The focused pytest selection
runs during the phase; the full suite is reserved for phase closeout.

`output/audit.json` and `output/web_narrative.md` are stored in the phase
folder, never in a hidden application data folder. The audit re-runs the
canonical public search and checks the existing proof-tree trust boundary.
