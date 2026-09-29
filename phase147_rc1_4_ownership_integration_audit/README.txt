Phase 147 RC1-4 Ownership Integration Audit

Audit only. No production files are changed.

Checks:
- multi renderer uses the RC1 ownership API for primary-method selection;
- the old inline primary selector is absent from the multi renderer;
- method evidence extraction remains present for the RC2 boundary;
- ownership results match the pre-RC1 selection pipeline across six groups;
- pi_6^3 establish_order and establish_group_structure own distinct primary methods;
- generic purpose-to-method header prose remains intact.

No repository-wide pytest is run in RC1-4.
