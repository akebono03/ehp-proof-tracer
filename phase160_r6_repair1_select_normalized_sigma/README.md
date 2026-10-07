# Phase 160-R6 Repair 1

Fix the production selector for the stable seven-stem sigma relation.

After Phase 160-R6, the stable inference result intentionally contains both:

1. the generic finite-cyclic transport result with generator `E^(n-9) sigma_9`, and
2. the sigma-family-normalized result with generator `sigma_n`.

The existing `higher_step` selector matched only the target group and cyclic order, so it selected the earlier generic intermediate result. Toda Proposition 5.15 integration requires the normalized `sigma_n` relation.

This repair changes only the `higher_step` selection predicate so it requires the generator to equal the already derived symbolic sigma-family element.

No inference rule, normalization rule, theorem guard, public Narrative, or test expectation is changed. No full test suite is run.
