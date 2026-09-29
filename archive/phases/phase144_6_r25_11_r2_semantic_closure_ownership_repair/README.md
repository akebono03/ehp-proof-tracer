# Phase 144-6 R25-11-R2 Semantic Closure Ownership Repair

## Target

Production file:
- `toda_group_proof_narrative_argument_multi_renderer.py`

Production function:
- `_toda_group_proof_narrative_argument_frontier_hidden_step_ids`

## Root cause addressed

R24 removed the general rule that protects the premises of an argument's
direct premises from becoming hidden explanatory contributions.

A later repair restored that protection only for `ESTABLISH_DEFINITION`.
That asymmetry allows semantic-closure/reachability changes to reactivate
contribution ownership in other argument roles.

## Minimal repair

Restore the pre-R24 general frontier rule: for every argument role, the
premises of direct premise steps are added to `protected_step_ids`.

No statement type is hard-coded. No pi_6^3 or pi_8^5 branch is added.
Semantic closure construction, argument construction, contribution
grouping, and connector assembly are unchanged.

## Expected invariants

- Phase37: 353
- Phase38: 291
- Phase39: 194
- Phase40 / selected: 190
- pi_6^3 selected contributions: 5
- narrative participating: 33
- detached selected: 157
- detached insertable: 0

R25-9B depth=2 semantic closure is re-run as a regression check.
R25-10 is run with `PYTHONUTF8=1` to avoid Windows CP932 audit-output
failure. No full test suite is run.
