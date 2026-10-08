Phase 161-R4-R5 repair7 source-step audit

Purpose
=======
Repair6 still leaves the Proposition 5.1 marker on the general statement.

The previous pipeline audit proved that the reference-body consumer helper is
called, but it does not relocate the Proposition 5.1 marker.

This audit inspects the exact source-step set used by:

  _phase154_r5_reference_source_steps_by_number()

and the exact result returned by:

  _phase154_r5_unique_visible_non_root_consumer_line()

for every Proposition 5.1 reference entry.

It prints:
- every reference entry
- every proof_step owned by Proposition 5.1
- every source step used by the consumer search
- each step's rule name
- each step's extracted literature locator
- each rendered statement
- the consumer_line result
- the relevant proof graph nodes and premises

No production or test files are changed.

Full pytest is not run.
