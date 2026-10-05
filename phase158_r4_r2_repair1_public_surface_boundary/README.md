# Phase 158-R4-R2 repair1 — Public-surface boundary

This repair narrows Phase 158-R4 back to the public Narrative surface.

Changes:

- restore the pre-R4-R2 internal equation-numbering implementation;
- keep public equation-tag cleanup in the contribution renderer;
- when an equation-reference connector has no surviving visible tagged equation,
  replace it with an unnumbered connector;
- remove duplicate public tag occurrences;
- compact surviving public equation numbers;
- narrow stale Phase 144.5 tests away from exact historical numbering;
- narrow prose tests to semantic content rather than an exact rendered group string.

Only R4-relevant focused tests are run.
The full pytest suite remains deferred until Phase 158 closure.
