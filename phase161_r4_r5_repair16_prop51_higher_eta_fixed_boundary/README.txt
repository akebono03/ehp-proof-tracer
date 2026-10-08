Phase 161-R4-R5 repair16
Proposition 5.1 higher-eta fixed boundary

Root cause
==========
The repair15 runtime audit proved that:

  Toda Proposition 5.1 higher eta group relation

has:

  boundary = PROOF_INTERNAL

even though it is the fixed general literature statement:

  pi_{n+1}^n = Z/2{eta_n}.

Therefore:

1. initial Reference construction sees the higher-eta general statement;
2. fixed-statement-boundary filtering removes it;
3. only the Proposition 5.1 aggregate remains;
4. aggregate specialization renders the concrete pi_4^3 statement in the
   Reference section.

Repair
======
Register the missing fixed component in the existing literature boundary
catalog:

_FIXED_RULE_COMPONENT_KEYS:
  "Toda Proposition 5.1 higher eta group relation"
  -> "higher_eta_group_relation"

_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME:
  "Toda Proposition 5.1 higher eta group relation"
  -> "Proposition 5.1"

No renderer rule is added.
No pi_4^2-specific condition is added.
No import, class, or function is changed.

Files
=====
Modified:
- toda_literature_statement_boundary.py
  - _FIXED_RULE_COMPONENT_KEYS
  - _REFERENCE_LOCATOR_BY_FIXED_RULE_NAME

New:
- tests/test_phase161_r4_r5_repair16_prop51_higher_eta_fixed_boundary.py

Stale test note
===============
The old Phase144 assertion that pi_6^3 must not show Proposition 5.1 is stale.
Current Phase157-R20 contracts require Proposition 5.1 as public R4 for pi_6^3.
Repair16 therefore validates the current Phase157 tests instead of that stale
assertion.

Full pytest is not run until Phase161 ends.
