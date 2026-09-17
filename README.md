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

### Phase 93-1: dependency traversal audit

The audit established the following boundaries:

```text
direct dependency
= ProofStep appearing directly in root_step.premises

transitive dependency
= recursively reachable ProofStep

shared dependency
= one ProofStep object reachable by multiple paths

truth source
= actual ProofStep ancestry
```

Repository metadata such as `key`, `phase`, and `theorem` is provenance metadata and is not used as mathematical truth.

### Phase 93-2: minimal dependency result

Added:

```text
TodaProofDependency
TodaProofDependencyResult
```

Core semantics:

```text
proof_step
depth
is_direct
```

The root proof step is kept separately and cannot appear in `dependencies`.

Equal-but-distinct `ProofStep` objects remain distinct. Repeated references to the same `ProofStep` object are identity-deduplicated.

### Phase 93-3: actual theorem-backed dependency extraction

Added:

```text
extract_toda_proof_dependencies()
```

The traversal is breadth-first.

This gives:

```text
shortest depth for shared dependencies
stable order derived from premises tuple order
identity-based deduplication
cycle-safe traversal
```

For actual `pi_9^5`, the result includes theorem-backed EHP exactness steps, Hopf-zero, suspension-surjectivity, known-group facts, relations, and definitions reachable from the final proof.

### Phase 93-4: dependency role classification

Added:

```text
TodaProofDependencyRole
classify_toda_proof_step_role()
```

Current roles:

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

Classification is primarily based on first-class statement types and `RelationType`, not theorem-name strings.

`OTHER` is deliberate: unreviewed Toda-specific statements are not guessed into a role.

### Phase 93-5: representative explanation integration

Added:

```text
TodaRepresentativeExplanationResult
build_toda_representative_explanation()
```

The integrated result combines:

```text
TodaGroupResult
TodaEHPSequenceResult
TodaEHPExactnessUseProvenanceResult
TodaProofDependencyResult
```

while preserving the original theorem-backed proof graph.

Representative flow:

```text
TodaGroupQuery
-> theorem-backed group result
-> TodaGroupResult
-> EHP context
-> exactness-use provenance
-> classified proof dependencies
-> TodaRepresentativeExplanationResult
```

For `pi_9^5`, the integrated result can expose dependencies such as:

```text
EHP exactness
EHP windows
pi_8^4 group structure
Delta injectivity
Hopf-zero
E surjectivity
Delta eta_9 relation
generator bridge
nu_5 definition
```

The explanation result is still structured data. It does not yet recursively explain how every dependency was itself proved.

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

## Search and architecture boundaries

The current implementation intentionally does not provide:

```text
unbounded search
general backtracking
producer ranking
proof-cost models
best-proof selection
persistent search cache
recursive proof-provenance tree/DAG result
automatic proof narrative generation
generic theorem proving
```

Phase 93 dependency extraction is a read-only view over the actual proof ancestry. It does not rewrite or mutate the proof graph.

## Verification

Latest confirmed Phase 93 focused regression:

```text
66 passed in 7.61s
```

Latest confirmed Phase 92 -> Phase 93 integration regression:

```text
88 passed in 5.05s
```

Latest confirmed repository-wide regression:

```text
7269 passed in 102.15s
```

`git diff --check`:

```text
clean
```

Wall-clock time is machine-dependent. Test count, semantic coverage, provenance coverage, focused regression, and repository-wide regression are the primary cross-machine signals.

## Next phase

The next planned phase is:

```text
Phase 94
recursive proof provenance
```

The first step should be:

```text
Phase 94-1
current recursive provenance / DAG representation audit
```

The intended direction is:

```text
final result
├─ dependency A
│  ├─ premise A1
│  └─ premise A2
├─ dependency B
│  └─ shared dependency
└─ dependency C
```

Phase 94 should represent how each dependency was proved while preserving sharing and avoiding accidental tree duplication.

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
