# EHP Proof Tracer

EHP Proof Tracer is an experimental Python project for representing, checking, querying, and explaining Toda-style calculations of homotopy groups of spheres.

The current emphasis is theorem-backed calculations, EHP exactness, low stable stems, bounded proof search, and machine-readable proof provenance.

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

Zero-group semantics:

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

The implemented layers are:

```text
TodaEHPExactnessWindowResult
TodaEHPSequenceResult
extract_toda_ehp_sequence_result()

TodaEHPGroupTermResult
TodaEHPGroupEnrichmentResult
connect_known_toda_group_results()

TodaEHPExactnessUseResult
TodaEHPExactnessUseProvenanceResult
extract_toda_ehp_exactness_use_provenance()
```

For the actual `pi_9^5` proof, the extracted EHP chain is:

```text
pi_10^9 --Delta--> pi_8^4 --E--> pi_9^5 --H--> pi_9^9 --Delta--> pi_7^4
```

The extraction follows reachable `ProofStep.premises`; it does not enumerate unrelated repository facts.

Each extracted exactness window can also be connected to the actual `TodaProp42ExactnessStatement` proof step and its direct reachable consumers.

## Phase 93: proof dependency extraction and explanation integration

Phase 93 is complete.

Phase 93 introduced:

```text
TodaProofDependency
TodaProofDependencyResult
TodaProofDependencyRole
extract_toda_proof_dependencies()
classify_toda_proof_step_role()
TodaRepresentativeExplanationResult
build_toda_representative_explanation()
```

The flat dependency view records:

```text
proof_step
shortest depth
direct/transitive status
semantic role
```

Traversal is breadth-first, identity-based, stable with respect to `ProofStep.premises`, and cycle-safe.

Current dependency roles are:

```text
EHP_EXACTNESS
EHP_WINDOW
GROUP_STRUCTURE
RELATION
ORDER
MAP_PROPERTY
DEFINITION
LITERATURE
OTHER
```

The truth source remains the actual reachable `ProofStep` ancestry, not repository metadata.

## Phase 94: recursive proof provenance

Phase 94 is complete.

### Phase 94-1: DAG representation audit

The audit established these semantics:

```text
node identity
= ProofStep object identity

edge order
= original ProofStep.premises order

premise_index
= index in the unfiltered original premises tuple

shortest_depth
= breadth-first shortest path from the root

recursive structure
= first-class proof edges
```

Equal-but-distinct `ProofStep` objects remain distinct nodes.

Non-`ProofStep` premises are not represented as proof nodes or proof edges.

No derived/imported/assumed status taxonomy was added because there is no current theorem-backed need for it.

### Phase 94-2: minimal proof graph representation

Added:

```text
TodaProofNode
TodaProofEdge
TodaRecursiveProofProvenanceResult
```

`TodaProofNode` keeps:

```text
proof_step
shortest_depth
role
```

`TodaProofEdge` keeps:

```text
parent_step
premise_step
premise_index
```

`TodaRecursiveProofProvenanceResult` keeps:

```text
root_step
nodes
edges
```

Shared dependencies are represented by one node with multiple incoming edges.

### Phase 94-3: actual theorem-backed recursive extraction

Added:

```text
extract_toda_recursive_proof_provenance()
```

The extractor starts at `TodaGroupResult.proof_step` and performs breadth-first traversal.

For the actual `pi_9^5` theorem-backed result, the recursive graph preserves:

```text
the Phase 68 final ProofStep as the root
all reachable ProofStep nodes
all ProofStep parent -> premise edges
original premise_index values
Phase 93 shortest-depth semantics
existing dependency-role classification
```

### Phase 94-4: shared-node, cycle, and stable-order regression

Regression now fixes these semantics:

```text
shared node
-> one node identity
-> multiple incoming edges preserved

node order
-> breadth-first
-> premises-order stable

edge order
-> parent traversal order
-> original premise_index order

cycle
-> traversal terminates
-> back-edge is preserved

self-cycle
-> traversal terminates
-> self-edge is preserved
```

Cycle fixtures are synthetic regression fixtures. The implementation does not claim that the representative Toda proof graph itself contains cycles.

### Phase 94-5: representative explanation integration

`TodaRepresentativeExplanationResult` now combines:

```text
TodaGroupResult
TodaEHPSequenceResult
TodaEHPExactnessUseProvenanceResult
TodaProofDependencyResult
TodaRecursiveProofProvenanceResult
```

with the identity invariant:

```text
dependency_result.root_step
is recursive_provenance.root_step
is group_result.proof_step
```

The existing Phase 93 role-filter API remains available.

## Current end-to-end picture

The current theorem-backed calculation/explanation flow is:

```text
(n,k)
-> TodaGroupQuery
-> ProofRepositoryEntry
-> TodaGroupResult
-> actual ProofStep provenance
-> TodaEHPSequenceResult
-> EHP term group enrichment
-> TodaEHPExactnessUseProvenanceResult
-> TodaProofDependencyResult
-> dependency roles
-> TodaRecursiveProofProvenanceResult
-> TodaRepresentativeExplanationResult
```

Representative target:

```text
pi_9^5 = Z/2{nu_5 eta_8}
```

Representative EHP context:

```text
pi_10^9 --Delta--> pi_8^4 --E--> pi_9^5 --H--> pi_9^9 --Delta--> pi_7^4
```

The representative explanation can now answer both:

```text
what facts were used?
```

and:

```text
how are those facts connected through proof premises?
```

as structured machine-readable data.

## Search and architecture boundaries

The current implementation intentionally does not provide:

```text
unbounded search
general backtracking
producer ranking
proof-cost models
best-proof selection
persistent search cache
automatic natural-language proof narration
top-level calculation orchestration
generic theorem proving
```

Recursive proof provenance is a read-only view over the actual proof ancestry. It does not rewrite or mutate the proof graph.

## Verification

Latest confirmed Phase 94-5 related regression:

```text
48 passed in 2.98s
```

Latest confirmed repository-wide regression:

```text
7313 passed in 36.98s
```

`git diff --check`:

```text
clean
```

Wall-clock time is machine-dependent. Test count, semantic coverage, provenance coverage, focused regression, and repository-wide regression are the primary cross-machine signals.

## Next phase

The next planned phase is:

```text
Phase 95
calculation orchestration
```

The first step is an audit:

```text
Phase 95-1
current calculation entry points / orchestration boundary audit
```

The audit should examine:

```text
TodaGroupQuery
known-result lookup
TodaGroupResult
build_toda_representative_explanation()
ProofRepository
bounded proof search
```

before fixing a top-level calculation result or proof-search fallback policy.

Full human-readable proof narration remains a later presentation layer.

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
