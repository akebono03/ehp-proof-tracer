# Phase 144-6 Final Regression Repair R22

## Changed production file
- `toda_group_proof_narrative_argument_body_renderer.py`

## Changed function
- `render_toda_group_proof_narrative_argument_body_markdown`

## Change
The normal non-exact display path already honors
`excluded_non_exact_step_ids`. R21 showed that the relocation path did not.

R22 applies the same exclusion to relocation candidates. A proof step already
displayed by an earlier Argument therefore cannot be reinserted as a relocated
direct premise/support step in a later Argument.

No group-specific condition is added.

## Tests
No tests are changed.

The runner first executes the two residual duplicate regressions. If they pass,
it executes the directly related Phase143-57c, Phase143-61b,
Phase143-61b-R, and Phase144-5 equation-numbering tests.

No full suite is run.
