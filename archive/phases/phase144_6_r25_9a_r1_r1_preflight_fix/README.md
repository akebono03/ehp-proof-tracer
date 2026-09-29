# Phase 144-6 R25-9A-R1-R1

## Purpose

R25-9A-R1 stopped before applying its production repair because its PowerShell
preflight used a formatting-sensitive raw string `Contains()` check.

R25-9A had previously applied its frontier change before its focused pytest
failed, and that runner did not roll the production file back.

R25-9A-R1-R1 replaces only the faulty preflight mechanism.

## Preflight

`check_phase144_6_r25_9a_frontier.py` parses
`toda_group_proof_narrative_argument_multi_renderer.py` with Python AST and
requires:

- an `ESTABLISH_DEFINITION` role guard;
- the second-level `direct_premise_steps -> premise_step.premises` protection
  loop to be inside that guard;
- no equivalent unguarded top-level loop in the helper.

If the R25-9A repair is genuinely absent, the runner stops. It does not
silently reapply it.

## Production repair

After the AST preflight passes, the same R25-9A-R1 repair is applied to
`toda_group_proof_narrative_argument_body_renderer.py`:

hidden steps are excluded from `relocated_direct_premises` as well as from
ordinary block display.

No nu-prime depth-selection repair is included.

## Tests

Focused tests only. The full suite remains deferred until the Phase 144-6
completion boundary.
