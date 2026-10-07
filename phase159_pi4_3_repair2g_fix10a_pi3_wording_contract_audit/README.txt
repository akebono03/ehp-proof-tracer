
Phase 159 repair2g fix10a audit

Purpose
-------
Determine whether the two pi_3^2 test failures after fix10 are:

- a production regression, or
- a pre-existing production/test contract mismatch.

Why this is audit-only
----------------------
fix10 only removes the late unconditional clearing of public Reference
entries. It does not modify proof-body generation.

The two failures concern proof-body wording and numbering:
- injective / surjective / isomorphism prose,
- zero-map prose,
- equation-number display form.

This audit prints the complete current pi_3^2 public Narrative and counts
the exact wording/numbering forms.

Scope
-----
Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.
