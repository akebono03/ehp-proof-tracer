# Phase 144-6 Final Regression Repair R17

## Changed production files

- `toda_group_proof_narrative_argument_multi_renderer.py`
  - `render_toda_group_proof_narrative_multi_argument_markdown`
- `toda_group_proof_narrative_argument_body_renderer.py`
  - `render_toda_group_proof_narrative_argument_body_markdown`

## Change

R16 mixed prerequisite support steps into `direct_derivation_premises`.
That changed the semantic meaning of the existing API and caused duplicate
premise rendering.

R17 restores `direct_derivation_premises` to its original meaning and passes
immediate prerequisite support through a separate
`direct_derivation_support_steps` argument. The body renderer considers these
steps only for relocation. The multi renderer records relocated support as
already displayed for later cross-argument suppression.

There is no group-specific branch.

## Tests

R17 first runs the two residual R16 failures, then the directly related
Phase143-57c, Phase143-61b, Phase143-61b-R, and Phase144-5 numbering tests.

No full test suite is run.
