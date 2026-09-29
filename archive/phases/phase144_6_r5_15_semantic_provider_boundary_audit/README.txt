Phase 144-6-R5-15
===================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-14 showed that unrestricted premise closure reaches full proof depth for
five of six representative groups and depth 15/16 for the sixth.

R5-15 tests whether existing generic Narrative semantics already provide a
usable stopping boundary.

Boundary actions
----------------
EXPAND
  Continue through a provider seed or ordinary Narrative proof material.

REFERENCE
  Stop below an existing REFERENCE block or another Narrative Argument
  conclusion. The result may be cited/used without recursively proving it in
  the current Argument.

STRUCTURAL
  Stop below EXACTNESS or MAP_PROPERTY blocks. The structural fact remains
  visible/usable, but its own proof is not recursively expanded.

INTERNAL
  Stop at OTHER material that has no current Narrative semantic role.

Inputs
------
Only existing generic structures are used:
- Narrative block roles
- Narrative Argument conclusions
- R5-13 provider seeds
- actual provenance edges

No target-specific n/k boundary rule is used.
No inference-rule-name parsing is used.

Benchmark
---------
The primary benchmark is pi_6^3.

The desired result is:

  full depth = 10
  semantic Narrative boundary depth = 3

without checking n=3, k=3 inside the boundary classifier.

Caution
-------
A shallow result is not automatically correct. INTERNAL boundaries may be too
aggressive. The audit prints deepest retained nodes and stop boundaries so
that every representative group can be inspected before any production depth
policy is implemented.
