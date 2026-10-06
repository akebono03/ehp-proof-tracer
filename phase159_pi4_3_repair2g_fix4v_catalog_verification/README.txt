Phase 159 pi_4^3 repair2g fix4v

Purpose
-------
Verify the active Toda (5.1) fixed-component catalog after fix4.

Why this package exists
-----------------------
fix4 stopped because its self-check incorrectly assumed that Toda (5.1)
must have exactly one fixed component.

The cumulative local state reports six (5.1) components. That is not
itself an error. The relevant contract is that the required component

  basic_sphere_group_relations

exists exactly once and can be resolved by:

  get_toda_fixed_statement_component(
    "(5.1)",
    "basic_sphere_group_relations",
  )

Scope
-----
Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.

The runner:
1. prints all active (5.1) component keys,
2. verifies basic_sphere_group_relations is unique and resolvable,
3. runs repair2g focused tests,
4. runs repair1 health checks,
5. runs low-dimensional contract checks,
6. prints the public Narrative if the earlier audit script is available.
