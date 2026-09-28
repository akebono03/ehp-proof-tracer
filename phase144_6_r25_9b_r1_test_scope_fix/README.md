# Phase 144-6 R25-9B-R1 — Focused Test Scope Fix

This package changes no production code.

The original R25-9B focused test additionally required the final Hopf relation
`H(nu-prime) = eta_5` to be emitted by the depth-2 generic Narrative.

That assertion is outside the R25-9B repair boundary. R25-9B repairs only the
selection of a missing endpoint already classified by semantic metadata as a
`DEFINITION_INTRODUCTION`.

The corrected test retains the actual completion conditions:

- source replay remains depth 2;
- ordinary presentation remains depth 2;
- semantic closure adds exactly one required bracket-membership endpoint;
- an `ESTABLISH_DEFINITION` argument is built;
- depth-2 Narrative contains the nu-prime definition introduction;
- pi_5^3 remains suppressed;
- the order relation used by the current Narrative remains present;
- the final pi_6^3 group statement remains present;
- CLI depth-2 Narrative has the definition;
- existing R25-9A and Web-mode regressions remain green.

The full suite is intentionally not run here.
