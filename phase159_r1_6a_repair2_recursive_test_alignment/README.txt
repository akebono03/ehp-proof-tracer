Phase 159-R1-6a repair2

Scope:
Test-only repair.

Reason:
R1-6a repair1 intentionally changed foundational-reference collection from
`presentation.nodes` to recursive `ProofStep.premises` ancestry. The original
focused test still inspected only `presentation.nodes`, so it could only see
the depth-2 identity-group fact and not the deeper pi_2^1=0 / E-isomorphism
premises.

Change:
Update only
`test_phase159_r1_6a_pi3_2_foundational_premises_keep_identity()`
to traverse recursively from `presentation.root_step`.

Production changes:
none

Full pytest:
not run
