# Phase 165 R57-R4: unreachable renderer cleanup

This narrowly scoped patch removes the **first historical, shadowed definition** of `render_toda_group_proof_narrative_markdown` in `toda_group_proof_narrative_renderer.py`. It also removes the Phase 159 stable-transport helper *only if* it is referenced solely by that dead definition and has no references in other top-level Python modules.

The two live renderer definitions (the common renderer captured in `_phase160_r7_previous_public_narrative_renderer` and the final public wrapper) remain intact. The currently active stable finite-cyclic specialization remains intact; it cannot safely be removed without an equivalent tested generic derivation.

The installer is guarded, idempotent, retains a backup, and validates syntax before writing. Its test suite covers dead-code removal, helper retention, alias capture protection, and repeat installation. Targeted regression tests are run; the full suite is deliberately deferred to the end of Phase 165.

Expand the ZIP into the repository root and run `phase165_r57_r4_shadowed_branch_cleanup/run.ps1` from PowerShell.
