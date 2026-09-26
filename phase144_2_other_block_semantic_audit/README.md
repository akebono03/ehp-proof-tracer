# Phase 144-2 OTHER Block / Semantic Renderer Audit

Audit only. No production code or tests are modified.

Targets:

- pi_10^4: n=4, k=6
- pi_12^5: n=5, k=7
- pi_15^8: n=8, k=7

For every OTHER block, this audit prints:

- concrete statement type
- inference-rule name
- current Block role
- semantic-sidecar step roles
- semantic-sidecar premise roles
- generic semantic statement renderer result
- legacy group Narrative renderer result
- complete statement repr

The goal is to distinguish three different causes:

1. the statement has useful semantics but Block recognition is missing;
2. the statement is correctly OTHER but generic rendering coverage is missing;
3. the proof graph/semantic statement itself does not expose enough mathematical structure.

Phase 144-2 should not add per-group Narrative special cases.
