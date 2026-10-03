Phase157 R11-R12 — remaining two defects audit

repair4 result:
- 55 passed / 3 failed.
- tagged Reference linkage for H(nu') = E^2 eta_3 now works.
- remaining defects:
  1. derived H(nu') = eta_5 appears after H-surjectivity.
  2. (5.3) double relation 2nu' = eta3 eta4 eta5 disappears from Reference.

This audit changes no production/test code.

It prints:
- all (5.3) entry candidates
- identity-based used status
- conclusion-equality matches against used premises
- used premise list
- body paragraph indices for tag(4), tag(5), tag(6), pi_6^5 and H-surjectivity
- direct premise/subpremise chain for H-surjectivity

pytest is not run.
full repository pytest remains deferred until Phase157 closure.
