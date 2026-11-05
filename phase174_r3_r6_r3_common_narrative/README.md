# EHP Proof Tracer — Phase 174 R3-R6-R3 Common Narrative Projection

This is a source-guarded, presentation-only patch for the completed public
proof of a finite cyclic group obtained from a verified index-two suspension.
It adds no theorem, search rule, `GIVEN` statement, repository database record,
or special `n,k`/generator-name branch.

## Reviewed baseline

- GitHub `develop`: `ecbb2fea225c5b88000629d9c025934fcc2d7075`.
- Previous user-local HEAD also accepted: `e4a5b73962bb98acb62b5335ffecae4728d98378`.
- The two modified production files must match their pinned, normalized Git blob
  SHA values exactly. Any unreviewed edits cause refusal, not an overwrite.
- `git fetch origin` checks the current upstream ref but does not merge,
  reset, clean, or commit the user's local worktree.

## Files

- `projection.py`: complete new source-only presentation helpers.
- `patch.py`: checks both baselines and performs two minimal, exact-anchor
  function modifications. No top-level import sections change.
- `run.ps1`: DryRun, source-guarded Apply, and focused tests.
- `tests/test_projection.py`: full focused regression tests.
- `output/`: created at DryRun with the **full** replacement versions of
  `typed_sentence()` and `render_model_backed_narrative_markdown()`, plus a
  Japanese code listing. The new `projection.py` itself is complete.

## Scope

1. A proved and sourced Toda (4.8) index-two step now renders both injection
   and quotient, including its proved Delta-zero hypothesis.
2. A typed cyclic-extension inference renders the order calculation and why
   the doubled generator generates; it does not repeat the final relation.
3. A source-linked ν-family citation is displayed as `Chapter V, iii)` without
   altering its internal locator or source provenance.
4. Existing search results, other group proofs, and final `GIVEN` counts remain
   unchanged. The existing canonical renderer continues to own the narrative.

## Running

Extract the ZIP into the repository root, then run `run.ps1 -DryRun` before
`run.ps1`. Only the latter changes production source files. Both require the
reviewed upstream `develop` HEAD; if GitHub advances, re-audit the patch.

Full-suite pytest is intentionally not run during Phase 174. The pass/fail
results are to be collected on the user's checkout after application.
