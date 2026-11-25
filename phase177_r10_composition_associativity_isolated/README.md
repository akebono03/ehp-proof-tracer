# Phase 177 R10 — General Composition Associativity Isolated

This package adds a general, typed element-equality rule for composition associativity. It uses the existing `typed_endpoints` check and preserves the exact ordered factors. It never changes symbol encodings, suspension wrappers, or factor order. The existing suspension GeneratorImage associativity rule is left unchanged.

The isolated test proves the left-associated Delta equality using the actual R8 source-screened provider, proves reassociation using the new rule, and replays existing equality transitivity to obtain the exact database route equality. This is not a public proof-search connection or a complete group proof.

Run `run.ps1 -DryRun` followed by `run.ps1` from the extracted package. The preflight accepts the reviewed R8 HEAD or a descendant with only new R9 audit files and verifies pinned sources. No existing tracked files, citations, GIVENs, or source registries are modified. Only focused tests run.
