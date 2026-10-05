Phase157-R20 repair3

Purpose
-------
Fix the Prop58 Equation (5.7) step selector after Proposition 2.2 became an
explicit proof dependency.

Cause
-----
`_build_equation57_steps()` selected Equation (5.7) only by the shape of its
conclusion:

- Relation
- lhs is H(...)
- lhs argument is a Composition

The new Proposition 2.2 intermediate relation has the same broad shape, so the
selector found two steps.

Repair
------
Select Equation (5.7) by its inference-rule identity:

  "Toda Equation 5.7 nu-prime eta_6 Hopf value"

This is a proof-step identity refinement, not a pi_6^3 Narrative
specialization.

Changed file
------------
- toda_prop58_zero_bootstrap.py
  - _build_equation57_steps()

Import changes: none.
Test changes: none.
Documentation changes: none.
Repository-wide pytest: intentionally not run.
