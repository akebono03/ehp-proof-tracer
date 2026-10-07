# Phase 159 Semantic Numbered Map-Property Reasoning Repair 25

This package repairs the focused failures observed after repair24 without
returning to prose-based semantic inference.

## Root cause

The pi_7^3 Hopf injective / surjective / isomorphism steps used while rendering
pi_11^6 occur deeper in recursive proof ancestry than the depth-2 presentation
nodes used by the public report.

The previous final prose normalizer found those statements by parsing rendered
sentences. Repair24 correctly removed that prose inference, but it exposed the
depth-boundary mismatch.

## Repair

Repair25 reuses the existing
`_phase159_r1_6c_recursive_proof_steps()` helper and builds map-property triples
from:

- typed injective statement classes;
- typed surjective statement classes;
- typed isomorphism statement classes;
- equality of the underlying `group_map` objects.

No map identity is inferred from rendered prose.

`EXACTNESS_TO_MAP_PROPERTY` remains the typed source for deciding whether the
public numbered statement receives `完全性より,`.

## Stale tests

Two old tests are updated:

- pi_3^2 now expects the current display-math numbered contract with exactness
  provenance;
- a synthetic text-only test now verifies that the helper refuses to invent
  semantic numbering when no presentation is supplied.

The old pi_11^6 numbered reasoning test is retained and is expected to pass via
recursive semantic triples.

Repository-wide pytest is not run in this Phase step.
