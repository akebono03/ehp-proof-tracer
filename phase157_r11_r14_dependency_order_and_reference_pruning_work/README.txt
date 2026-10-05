Phase157 R11-R14 — dependency order / Reference pruning

R11-R13 audit confirmed:

1. ord(eta_3^3)=2 directly depends on:
   - pi_5^2 = Z/2{eta_2 eta_3 eta_4}
   - E: pi_5^2 -> pi_6^3 injective
   but public body currently shows the order statement before injectivity.

2. H-surjectivity directly depends on H(nu')=eta_5.
   Public body proves H-surjectivity only after already deriving the short exact sequence.

3. [R3] Proposition 5.3 has no body marker.
   Its only consumer is [R1]'s pi_5^2 statement.
   Therefore it is ancestry for another public Reference statement, not a direct public proof dependency.

R11-R14 changes:
- Generic ORDER dependency ordering.
- MAP_PROPERTY equality support + map statement precede the short-exact derivation.
- Ancestry-only fixed References are not restored.
- No pi6_3 / nu_prime / Proposition 5.3 name hard-code.

Focused pytest only.
Full repository pytest remains deferred until Phase157 closure.
