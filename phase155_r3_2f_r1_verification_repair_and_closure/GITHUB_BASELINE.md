# GitHub baseline — Phase 155-R3-2F-r1

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before R3-2F-r1:

- `tests/test_phase143_1_generic_proof_order.py`
- `tests/test_phase143_1b_semantic_proof_order.py`
- `toda_group_proof_generic_narrative_renderer.py`

GitHub search confirms that the current generic renderer legitimately
contains `statement.nu_prime`.

The same renderer also legitimately accesses finite-dimensional statement
fields such as `statement.pi6_4_group_relation`.

Therefore whole-module substring bans for `"pi6"` or `"nu_prime"` are not a
valid test for group-specific rendering branches.

R3-2F-r1 changes the test contract from source-wide name absence to
control-flow-condition absence.
