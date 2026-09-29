Phase 147 RC1-5 Final Regression

Purpose
-------
Close Phase 147 / RC1 (Argument-method ownership) without adding new
production behavior.

Production changes: none.
Test changes: none.
Documentation changes: none in this package.

Order
-----
A. Syntax preflight
B. RC1 ownership focused regression
C. Generic Narrative regression
D. Web group-proof Narrative regression
E. RC1/RC2 boundary verification
F. Repository-wide pytest

The repository-wide suite is intentionally run only at the end of Phase 147.

Phase boundary
--------------
Phase 147 / RC1 owns only the semantic relationship between a Narrative
argument and its selected primary exactness method.

Phase 148 / RC2 will address recursive exactness evidence exposure.
Phase 149 / RC3 will address contribution ownership / insertion ordering.

Known Narrative symptoms such as excessive auxiliary exactness display and
short-exact-sequence placement are intentionally not repaired in RC1-5.
