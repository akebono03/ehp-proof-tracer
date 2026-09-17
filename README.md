# EHP Proof Tracer

EHP Proof Tracer is an experimental Python project for representing, checking, querying, and increasingly explaining Toda-style calculations of homotopy groups of spheres. The current emphasis is theorem-backed calculations, EHP exactness, low stable stems, bounded proof search, and preservation of machine-readable proof provenance.

## Current mathematical frontier

The repository formalizes the concrete proof spine through Toda Lemma 5.16 and consolidates the stable groups through stem 7:

```text
G_0 = Z{iota}
(G_1;2) = Z/2{eta}
(G_2;2) = Z/2{eta^2}
(G_3;2) = Z/8{nu}
(G_4;2) = 0
(G_5;2) = 0
(G_6;2) = Z/2{nu^2}
(G_7;2) = Z/16{sigma}
```

Proof provenance is preserved with `ProofStep` objects rather than storing only final conclusions.

## Proof-search capability

The current high-level proof-search flow is:

```text
goal
-> goal-compatible final-rule selection
-> missing-premise analysis
-> binding preservation
-> concrete requested-statement construction when fully bound
-> concrete producer compatibility filtering
-> bounded producer search
-> finite explicit producer retry only for remaining true ambiguity
-> search diagnostics
-> execution diagnostics
-> unified search report
-> exact selected-path execution
-> concrete producer-output validation
-> goal ProofStep
```

The bounded search uses an explicit `max_depth`.

Formal regression covers:

```text
max_depth = 2
max_depth = 3
max_depth = 4
```

The default remains:

```text
max_depth = 2
retry_policy = None
```

Phase 87 added finite producer retry. Phase 88 added concrete theorem-instance compatibility filtering. Phase 89 audited the remaining pressure for general backtracking and found no current theorem-backed need for a new general search algorithm.

## Theorem-backed Toda group queries

Phase 90 introduced:

```text
TodaGroupQuery(n,k)
-> TodaPrimaryGroup(n+k,n)
-> ProofRepository
-> matching theorem-backed ProofRepositoryEntry
-> original ProofStep
```

A lookup miss returns an empty tuple and does not start proof search.

Phase 91 introduced normalized machine-readable group results:

```text
TodaGroupResult

target
group_structure
generators
generator_orders
source_entry
proof_step
```

Order semantics:

```text
positive int
= finite generator order

None
= infinite order
```

Zero group semantics:

```text
group_structure = None
generators = ()
generator_orders = ()
```

Representative theorem-backed results include:

```text
TodaGroupQuery(4,3)
-> pi_7^4
-> Z{nu_4} + Z/4{E nu'}
-> generator_orders = (None, 4)

TodaGroupQuery(4,6)
-> pi_10^4
-> Z/8{nu_4^2}
-> generator_orders = (8,)

TodaGroupQuery(2,7)
-> pi_9^2
-> 0
```

The original `ProofRepositoryEntry`, `ProofStep`, premises, and group-structure objects are preserved rather than reconstructed.

## Phase 92: theorem-backed EHP extraction and provenance

Phase 92 is complete.

### Phase 92-1: current-representation audit

The audit confirmed that the repository already had the structural building blocks:

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
TodaPrimaryGroup
ProofStep provenance
TodaGroupResult
```

The missing layer was aggregation and connection of those objects to an actual theorem-backed group result.

### Phase 92-2: minimal EHP result representation

Added:

```text
TodaEHPExactnessWindowResult
TodaEHPSequenceResult
```

The result layer preserves the identity of the existing structural EHP objects and supports a selected subset of contiguous exactness windows.

### Phase 92-3: actual theorem-backed EHP extraction

Added theorem-backed extraction from the final group-result proof ancestry.

For the actual `pi_9^5` proof, the extracted chain is:

```text
pi_10^9 --Delta--> pi_8^4 --E--> pi_9^5 --H--> pi_9^9 --Delta--> pi_7^4
```

The extraction is provenance-based: it follows reachable `ProofStep.premises` and collects the actual `TodaProp42ExactnessStatement` objects used in the proof ancestry.

It does not enumerate unrelated repository facts.

### Phase 92-4: connect known group structures to EHP terms

Added:

```text
TodaEHPGroupTermResult
TodaEHPGroupEnrichmentResult
connect_known_toda_group_results()
```

Each EHP term can now be connected to the available normalized theorem-backed `TodaGroupResult` values in a `ProofRepository`.

Unknown and known-zero remain distinct:

```text
unknown group
-> group_results == ()

known zero group
-> TodaGroupResult(group_structure=None)
```

Representative Phase 92 integration:

```text
pi_10^9 -> unresolved
pi_8^4  -> known theorem-backed group
pi_9^5  -> known theorem-backed group
pi_9^9  -> unresolved
pi_7^4  -> known theorem-backed group
```

### Phase 92-5: exactness-use provenance

Added:

```text
TodaEHPExactnessUseResult
TodaEHPExactnessUseProvenanceResult
extract_toda_ehp_exactness_use_provenance()
```

Each extracted exactness window is connected to:

```text
TodaEHPExactnessWindowResult
-> actual TodaProp42ExactnessStatement ProofStep
-> direct reachable consumer ProofSteps
```

This makes it possible to distinguish the existence of an exactness window from its actual use in the theorem-backed proof.

The Phase 92-5 layer remains intentionally EHP-specific. A generic dependency graph / mathematical explanation layer is deferred to Phase 93.

## Current Phase 92 end-to-end picture

The current theorem-backed flow is:

```text
TodaGroupQuery
-> theorem-backed ProofRepositoryEntry
-> TodaGroupResult
-> final ProofStep provenance
-> actual EHP exactness windows
-> TodaEHPSequenceResult
-> known group structures for EHP terms
-> exactness ProofSteps
-> direct exactness consumers
```

Representative target:

```text
pi_9^5 = Z/2{nu_5 eta_8}
```

Representative EHP context:

```text
pi_10^9 --Delta--> pi_8^4 --E--> pi_9^5 --H--> pi_9^9 --Delta--> pi_7^4
```

## Search and architecture boundaries

The current implementation intentionally does not provide:

```text
unbounded search
general backtracking
producer ranking
proof-cost models
best-proof selection
DFS / BFS / A*
persistent search cache
generic mathematical dependency extraction
recursive explanation of every proof dependency
automatic proof narrative generation
generic theorem proving
```

These boundaries are deliberate. New machinery is added only when an actual theorem-backed calculation requires it.

## Verification

Latest confirmed Phase 92-5 focused regression:

```text
68 passed in 8.90s
```

Latest confirmed repository-wide regression:

```text
7203 passed in 109.03s
```

`git diff --check`:

```text
clean
```

Wall-clock time is machine-dependent. Test count, semantic coverage, provenance coverage, focused regression, and repository-wide regression are the primary cross-machine signals.

## Next phase

The next planned phase is:

```text
Phase 93
proof dependency extraction / explanation layer
```

The goal is to generalize beyond EHP-specific provenance and extract the mathematical dependencies actually used by a final theorem-backed result.

The intended direction is:

```text
final result
-> actually used intermediate conclusions
-> propositions / lemmas / relations / known groups / map properties
-> dependency roles
-> machine-readable explanation structure
```

Phase 93 should not pre-implement recursive full proof narration or a generic theorem prover.

## Documentation

```text
README.md
= current status and capabilities

docs/design.md
= current architecture, semantics, and design boundaries

docs/development_log.md
= chronological implementation history

docs/code_reference.md
= current code navigation

docs/proof_records.md
= representative mathematical and infrastructure records

docs/roadmap.md
= future-oriented plan and deferred boundaries
```

## Project principle

The implementation follows a narrow-extension policy:

```text
actual mathematical or proof-search need
-> smallest missing representation or orchestration
-> preserve existing semantics and provenance
-> add focused regression coverage
-> do not pre-implement future phases
```
