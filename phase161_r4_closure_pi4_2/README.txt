Phase 161-R4 closure
pi_4^2 proof body specialization / Reference frontier

Status
======
The Phase161 R4 focused test set passes 14/14 after R4-R4 repair2.

The remaining Phase156 public-header failures are not used as R4 gates because
their expectations were superseded by later Phase157 Reference contracts.

Current pi_6^3 contract
=======================
Later Phase157 work requires:

- R1 Proposition 5.6
- R2 (5.3)
- R3 Proposition 5.3
- R4 Proposition 5.1
- R5 Proposition 2.2

Equation (5.7) is proof-internal and uses Proposition 2.2 as an actual premise.

The current local/public Narrative still showing `(5.7)` instead of
Proposition 2.2 is a known pre-existing Phase157 regression. It predates
Phase161-R4 and is not repaired here.

R4 completion criteria
======================
For pi_4^2:

- `(5.2)` remains a general-form public Reference.
- Proposition 4.4 is not public.
- Proposition 4.4 decomposition prose is not in the body.
- second-summand restriction prose is not in the body.
- `(5.2)` is specialized at i=4 in the body.
- pi_4^3 = Z/2{eta_3} is shown.
- eta_3 -> eta_2 eta_3 is shown.
- pi_4^2 = Z/2{eta_2^2} is shown.
- QED is shown.

This closure package changes no production code and no tests.

Next Phase161 step
==================
Audit pi_5^3.

The full test suite remains reserved for the end of Phase161.
