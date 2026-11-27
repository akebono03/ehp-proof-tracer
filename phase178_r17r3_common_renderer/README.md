# Phase 178 R17R3 — common Renderer

Display-only candidate based on develop `720a7e8658a3f7e94f92a20ab530f763f1b421e1`.

## Scope

- `phase168_r3_27_typed_statement_projection.py`: hook in `typed_sentence` for the existing six-premise finite cyclic quotient inference.
- `phase168_r3_37c_reference_projection.py`: hook in `_verified_source_sentence` for canonical typed Toda (5.12) statements.
- `phase168_r3_5_model_renderer.py`: two post-layout hooks in `render_model_backed_narrative_markdown` for exclusive composition factor elision and safe quotient/image ordering.
- The new package contains the complete projection, installer, regression tests, and PowerShell entry point. The existing rank-two projection and its tests are not changed.

No mathematical rule, GIVEN, source registration, proof step, search order, trust boundary, or document outside this package is changed.

## Execution

Extract the package into the repository root and run `run.ps1 -DryRun`, then `run.ps1` without the switch. The installer checks the reviewed HEAD, branch, upstream reference, dependency blobs, tracked worktree, and exact function anchors. It refuses unrelated changes. Dry run does not edit tracked source and exports the full proposed source files to `%LOCALAPPDATA%/EHPProofTracerAudit/phase178_r17r3_common_renderer` (temporary directory fallback). Normal execution also keeps the original bytes as backups.

The focused test gate reuses the R17R2 public audit, checks 18 proof steps and six model citations, checks the actual rendered quotient and the canonical source body, tests rejection of ambiguous or shared branches, and reruns the existing Phase 177 rank-two and composition display tests. The full pytest suite is not run.

This package was syntax-checked in the artifact environment. The complete repository was not available locally there; actual integration pytest and the final display gate must pass in the reviewed checkout before the change is accepted. No GitHub write is performed by this package.
