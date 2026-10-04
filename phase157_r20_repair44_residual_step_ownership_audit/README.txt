Phase157-R20 repair44 runtime audit

Purpose
-------
Inspect the remaining pi_6^3 body defects after repair43:

1. the late Proposition 2.2 specialization
   H(nu' eta_6) = H(nu') eta_6;
2. the repeated Delta-zero conclusion after the short exact sequence.

The audit prints:
- all presentation steps whose rendered form matches each target;
- step identity;
- rule name;
- literature reference locator;
- direct premises;
- direct consumers;
- final visible paragraph order.

This determines whether:
- the Proposition 2.2 specialization should be relocated before its Equation
  5.7 consumer;
- the late Delta-zero paragraph is a second rendering of the same semantic
  step or a distinct derivation of an already established fact.

Production code changes: none.
pytest: not run.
