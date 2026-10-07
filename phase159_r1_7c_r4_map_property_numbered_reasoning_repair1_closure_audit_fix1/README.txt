Phase 159 R1-7c R4 numbered reasoning repair1 closure audit fix1

Cause
-----
The previous closure audit missed pi_5^3.

Its public surjectivity line is:

  これより, $E: ...\tag{2}$ は全射.

The audit parser stripped Reference prefixes but did not strip the ordinary
public prose prefix "これより, ". Therefore it failed to normalize the
surjectivity line to the same map key.

Focused pi_5^3 inspection confirmed the production output is already correct:

  (1), (2) より, $E: ...$ は同型.
  $E: ...\tag{1}$ は単射.
  これより, $E: ...\tag{2}$ は全射.

Change
------
Audit only.

The corrected parser strips:
- [R#]より,
- これより,

before comparing map-property lines.

Expected closure result:
- pi_3^2
- pi_5^3
- pi_7^3
- pi_11^6

as fully numbered trios.

The Delta pairs in pi_9^3 and pi_10^3 remain pairs without isomorphism.

Production code changes: none.
Test code changes: none.
No full pytest.
