# Phase 160-R6 Repair 2

Repair only the new Phase 160-R6 focused test.

The previous test walked the complete provenance of `higher_step` and counted every generic finite-cyclic transport rule appearing in downstream dependencies. After Phase 160-R5, the repository legitimately contains generic transports from other stems, so the provenance-wide count is not expected to be one.

The Phase 160-R6 contract is narrower: the sigma normalization step must have exactly one direct generic finite-cyclic transport premise for the seven-stem sigma branch.

This repair changes the test to inspect `result.higher_step.premises` directly.

No production code, inference rule, theorem semantics, public Narrative, or existing historical test is changed. No full test suite is run.
