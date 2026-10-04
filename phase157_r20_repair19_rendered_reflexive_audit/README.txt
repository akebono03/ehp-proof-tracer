Phase157-R20 repair19 runtime audit

Purpose
-------
Identify equality proof steps whose original lhs and rhs are structurally
different but whose generic rendered expressions become identical.

Reason
------
repair16 suppressed only Relation steps satisfying:

  statement.lhs == statement.rhs

The public Narrative still contains:

  eta_3^3 = eta_3^3
  eta_5 = eta_5

The generic renderer normalizes the two relation sides independently, so a
non-reflexive source Relation can become reflexive only at presentation time.

This audit prints every equality node satisfying:

  render(lhs) == render(rhs)

together with:
- whether lhs == rhs structurally;
- lhs/rhs types and repr;
- normalized lhs/rhs;
- rendered full step;
- inference rule;
- premise types.

Production code changes: none.
Tests: none.
pytest: not run.
