Phase 161-R4-R5 repair15
Proposition 5.1 Reference-selection audit

Current status
==============
Repair14 fixed the disappearing-Reference problem far enough that:
- Proposition 5.1 survives in the public Reference section.
- The body linkage to concrete pi_4^3 passes.
- The remaining pi_4^2 defect is that the Reference statement is concrete
  pi_4^3 instead of the general Proposition 5.1 higher-eta statement.

One Phase144 pi6_3 test is stale:
Phase157-R20 explicitly requires Proposition 5.1 in the public pi6_3
Reference section, so the old "Proposition 5.1 not in reference" assertion
must not be treated as a current regression.

Audit purpose
=============
Print the exact Proposition 5.1 Reference-selection state at three stages:

1. Before fixed-statement-boundary filtering
2. After fixed-statement-boundary filtering
3. After statement selection and aggregate specialization

For every relevant step it prints:
- rule name
- extracted literature reference label/locator
- literature boundary classification
- component_key
- raw rendered statement
- selected step
- specialized rendered statement

This determines exactly why the higher_eta_group_relation general statement
is not the final Reference line.

No production files are modified.
No tests are modified.
No full pytest is run.
