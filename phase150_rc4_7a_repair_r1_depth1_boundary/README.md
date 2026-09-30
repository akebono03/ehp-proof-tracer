# Phase 150 RC4-7A Repair R1

This repair restores the pre-existing depth=1 Narrative boundary.

RC4-7A Reference normalization is enabled only for presentations with
`max_depth >= 2`. A depth=1 presentation keeps the legacy Reference-free
fallback as required by the Phase 134 regression contract.

No Reference extraction rule, mathematical inference, dedicated renderer,
equation numbering, EHP semantic naming, or argument-flow behavior is changed.

Repository-wide pytest is intentionally deferred until the end of Phase 150.
