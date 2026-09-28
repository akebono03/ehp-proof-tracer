# Phase 144-6 Final Regression Repair R19

## Changed production file
- `toda_group_proof_narrative_argument_multi_renderer.py`
  - `render_toda_group_proof_narrative_multi_argument_markdown`

## Reason
R18 showed both residual duplicates are facts already completed in the order
Argument and then reintroduced by the later group-structure Argument.

R19 feeds the accumulated completed direct-premise/support step identities into
the body renderer's existing `context_hidden_step_ids` channel. It also records
both direct premises and their relocation support as completed after rendering.

No group-specific branch is added.

## Tests
First the two confirmed duplicate regressions, then Phase143-57c,
Phase143-61b, Phase143-61b-R and Phase144-5 equation-numbering tests.

No full suite.
