Phase 146-3 Semantic Capability Diagnosis

Purpose
-------
Test semantic readiness properties already required by the generic
multi-argument renderer, without using target coordinates, theorem names,
or raw argument counts.

Checks
------
- every NarrativeArgument has a resolvable purpose subject
- every NarrativeArgument has a resolvable conclusion step
- every NarrativeArgument has a renderable purpose sentence
- exactly one establish_group_structure argument exists
- child-argument reachability from that root

Production changes
------------------
None.

Existing test changes
---------------------
None.

Boundary
--------
This diagnosis does not change routing. Its result determines whether these
existing semantic properties are sufficient for the Phase 146 capability
predicate or whether one more renderer-readiness property must be identified.
