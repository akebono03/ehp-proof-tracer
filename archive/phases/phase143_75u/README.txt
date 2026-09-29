Phase 143-75U
=============

Purpose
-------
Re-audit the remaining rule-name fallback inventory after Phase 143-75T.

Production changes
------------------
None.

Test changes
------------
None.

Audit scope
-----------
n = 2..15
k = 0..7
proof replay max_depth = 7

The audit uses the production narrative fallback condition:

_render_group_proof_narrative_fact(step) == step.inference_rule.name

Expected baseline
-----------------
112 groups
11033 presentation nodes
365 rule-name fallback occurrences
31 statement types
0 render errors

No implementation
-----------------
This subphase does not modify a renderer. The next implementation target
must be selected from this measured inventory.

No full pytest
--------------
No tests are changed and the full suite remains deferred until the end
of Phase 143.
