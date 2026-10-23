# Phase 168 R3-24: π₄³ narrative sequence and order

Prerequisite: R3-23 installed and its two targeted tests passing.

Changes only `render_model_backed_narrative_markdown` in `phase168_r3_5_model_renderer.py` by replacement of the full function. The other module imports and declarations are kept. The previous file is backed up.

Two proven, composable consecutive EHP exactness windows are rendered as one four-term exact sequence. The textual `is exact` suffix is removed from other explicit exactness windows. A first-isomorphism sentence is postponed until after the actual domain group Relation if that Relation occurs later in the Proof Tree. No source or inference is guessed and no group-specific proof text is inserted.

Run `run.ps1` from PowerShell after extracting the ZIP into the repository root. Only focused R3-24 and R3-23 tests run. Whole-suite tests remain deferred to the end of Phase 168.

The code was statically checked, but integration pytest cannot run in this delivery environment. Compare the actual Web output with the frozen baseline before declaring R3-24 complete.
