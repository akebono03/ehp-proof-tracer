# Phase 173 R15R17 — Unified Certified Narrative Model

This package changes the model construction of incomplete proof narratives so that an existing, independently certified abstract structure tree is included in the same sequence of verified proof steps as the named-generator search progress. It never converts an abstract certificate into a completed named-generator proof.

Extract the ZIP in the root of the local `akebono03/ehp-proof-tracer` checkout on branch `develop`. The guarded PowerShell runner supports `-DryRun`, normal installation with focused tests, and `-Restore`. DryRun generates `FULL_CHANGED_UNITS.md`, which contains the complete post-patch source for every changed function and the complete updated import section.

The package checks the reviewed Git blobs, the current remote `develop` head, and working-tree/index status of each production file before changing it. It does not stage, commit, reset, stash, clean, or pull local files. It preserves original file line endings, backs up all five modified files, checks the Git index tree, and restores original files if focused tests fail. It uses no repository-wide pytest run.

The unmodified explicit legacy/outline compatibility renderer is preserved. The normal model-backed narrative now uses one citation table, one proof-step stream, one common renderer invocation, and named-generator open goals at the end. Historical tests that asserted the old separate abstract-proof headings require revised contracts before Phase 173 closeout.
