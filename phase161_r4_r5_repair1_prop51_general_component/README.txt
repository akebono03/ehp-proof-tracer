Phase 161-R4-R5 repair1

Purpose
=======
Fix two failures from the first R4-R5 attempt.

1. The test incorrectly used `replay.provenance_steps`.
   The current replay API is `replay.steps`, whose entries expose `.proof_step`.

2. The linkage inference rule name started with `Toda Proposition 5.1`.
   The generic literature-reference inference therefore treated the linkage
   step itself as a Proposition 5.1 statement and rendered the concrete
   `pi_4^3 = Z/2{eta_3}` relation in the Reference section.

Repair
======
Use the already-defined Proposition 5.1 fixed component:

  higher_eta_group_relation

as an explicit fixed literature statement.

The fixed component is:

  pi_{n+1}^n = Z/2{eta_n}, n >= 3.

Then connect the independently derived concrete `pi_4^3` step to that general
component with a non-literature linkage rule.

Expected public form
====================
Reference:
- Toda (5.2), general map statement
- Proposition 5.1, general higher-eta group statement

Proof body:
- concrete pi_4^3 = Z/2{eta_3}, linked by [Rk]
- concrete i=4 specialization of (5.2)
- eta_3 -> eta_2 eta_3
- pi_4^2 conclusion

Files changed
=============
- toda_prop56_zero_bootstrap.py
- toda_literature_statement_boundary.py
- tests/test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py

Imports
=======
`toda_prop56_zero_bootstrap.py` adds `LiteratureReference` to the existing
`from proof import (...)` block.

No full test suite is run.
