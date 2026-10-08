Phase 161-R4-R5 repair10 final relink audit

Purpose
=======
Repair9a successfully added the final public Reference-body relink call, but the
final output is unchanged.

Earlier audits proved:
- the internal R3 Proposition 5.1 component has pi_4^3 as its unique consumer;
- the linkage helper works correctly in isolation.

This audit traces every call to:

  link_toda_group_proof_narrative_reference_body_consumers()

during the final public render after repair9a.

For each call it prints:
- final/current Reference number and locator
- every proof step owned by each Reference entry
- source steps selected by the linkage helper
- the unique visible consumer returned for each Reference
- interesting body lines before and after the call

This directly determines whether the final public R2 uses:
- the Proposition 5.1 higher-eta component, whose consumer should be pi_4^3; or
- the Proposition 5.1 aggregate, whose consumer may be the general component.

No production or test files are modified.
No full pytest is run.
