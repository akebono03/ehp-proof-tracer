# EHP Proof Tracer

EHP Proof Tracer is a Python project for representing, checking, searching, and explaining theorem-backed calculations in Toda-style homotopy groups.

The project currently focuses on the 2-primary Toda groups \(\pi_i^n\), EHP exactness, explicit proof provenance, and the calculation spine leading through stable stems \(G_0\) to \(G_7\).

## Current mathematical coverage

The implemented mathematical spine includes Toda-style calculations and relations through the material used for the first seven stable stems.

Representative finite-dimensional results include:

\[
\pi_5^2=\mathbb Z/2\{\eta_2^3\},
\]

\[
\pi_6^3=\mathbb Z/4\{\nu'\},
\]

\[
\pi_7^4=\mathbb Z\{\nu_4\}\oplus \mathbb Z/4\{E\nu'\},
\]

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\]

\[
\pi_{10}^4=\mathbb Z/8\{\nu_4^2\},
\]

\[
\pi_{11}^5=\mathbb Z/2\{\nu_5^2\},
\]

\[
\pi_9^2=0,
\]

\[
\pi_{12}^5=\mathbb Z/2\{\sigma'''\}.
\]

The stable 2-primary stem data currently consolidated in the project is:

\[
G_0=\mathbb Z\{\iota\},
\]

\[
(G_1;2)=\mathbb Z/2\{\eta\},
\]

\[
(G_2;2)=\mathbb Z/2\{\eta^2\},
\]

\[
(G_3;2)=\mathbb Z/8\{\nu\},
\]

\[
(G_4;2)=0,\qquad (G_5;2)=0,
\]

\[
(G_6;2)=\mathbb Z/2\{\nu^2\},
\]

\[
(G_7;2)=\mathbb Z/16\{\sigma\}.
\]

This is not an all-primary calculator for ordinary homotopy groups of spheres.

## Proof infrastructure

The current proof-search infrastructure supports:

- an in-memory `ProofRepository`,
- inference-rule catalogs,
- fixed-point-safe producer selection,
- concrete theorem-instance compatibility,
- bounded dependency search,
- explicit `max_depth`,
- finite producer retry,
- cycle detection,
- selected-path execution,
- search and execution diagnostics,
- proof-step provenance,
- repository-nonmutating execution.

General unbounded proof search, proof ranking, proof-cost optimization, and best-proof selection are intentionally not implemented.

## Toda group calculation API

The main calculation entry point is:

```python
build_toda_calculation_result(
  repository,
  query,
)
```

where `query` is a `TodaGroupQuery(n, k)` representing the Toda target

\[
\pi_{n+k}^n.
\]

The current orchestration flow is:

```text
TodaGroupQuery
↓
direct theorem-backed group lookup
├─ result found
│  ↓
│  normalized TodaGroupResult
│
└─ direct lookup miss
   ↓
   concrete aggregate-theorem branch discovery
   ↓
   original branch ProofStep recovery
   ↓
   normalized TodaGroupResult
↓
representative explanation
↓
TodaCalculationResult
```

Direct results always take precedence over aggregate fallback results.

Multiple valid results are preserved. The calculation layer does not silently rank or choose one result.

## Calculation result structure

A `TodaCalculationResult` contains zero or more `TodaCalculationCandidate` objects.

Each candidate contains:

```text
group_result
explanation
goal_source
```

For direct theorem-backed results:

```text
goal_source = None
```

For aggregate-derived results, `goal_source` preserves:

```text
original aggregate ProofRepositoryEntry
branch path
```

while `group_result.proof_step` preserves the original branch `ProofStep`.

This separation keeps aggregate provenance and actual proof provenance distinct.

## Group normalization

`TodaGroupResult` provides:

```text
target
group_structure
generators
generator_orders
source_entry
proof_step
```

Order semantics are:

```text
None
= infinite order

positive integer
= finite order
```

For the zero group:

```text
group_structure = None
generators = ()
generator_orders = ()
```

## EHP and exactness provenance

For theorem-backed proofs containing actual EHP ancestry, the project can extract:

- EHP exactness windows,
- a contiguous EHP sequence,
- exactness-use provenance,
- known group information on EHP terms.

The representative \(\pi_9^5\) proof yields the EHP context

\[
\pi_{10}^9
\xrightarrow{\Delta}
\pi_8^4
\xrightarrow{E}
\pi_9^5
\xrightarrow{H}
\pi_9^9
\xrightarrow{\Delta}
\pi_7^4.
\]

Extraction is based on proof ancestry actually reachable from the final theorem-backed `ProofStep`.

## Flat and recursive proof provenance

The explanation layer exposes both:

```text
flat dependency view
recursive proof graph
```

The recursive representation preserves:

- one node per `ProofStep` identity,
- all proof edges,
- original premise indices,
- shared dependencies,
- stable traversal order,
- cycle-safe traversal,
- shortest-depth metadata.

The key identity invariant is:

```text
group_result.proof_step
is dependency_result.root_step
is recursive_provenance.root_step
```

## Current representative end-to-end coverage

Using only aggregate theorem entries in a `ProofRepository`, the top-level API is regression-tested for:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5.
\]

These cases cover:

- direct sums,
- finite cyclic groups,
- zero groups,
- outer aggregate branches,
- nested aggregate branches,
- generator orders,
- branch-proof identity,
- aggregate provenance,
- EHP provenance,
- recursive proof provenance.

## Current boundaries

The calculation layer currently handles concrete finite-dimensional theorem branches.

The following are intentionally deferred:

- automatic instantiation of symbolic higher-range branches,
- target-only generation of unknown right-hand-side proof goals,
- bounded proof-search fallback from a target-only query,
- detailed calculation-failure taxonomy,
- natural-language proof narration,
- general theorem proving,
- odd-primary full integration,
- an all-primary ordinary sphere-homotopy calculator.

These are separate capabilities rather than missing invariants in the current concrete orchestration.

## Verification

Latest confirmed repository-wide regression:

```text
7419 passed in 38.11s
```

Latest focused Phase 95 representative regression:

```text
106 passed in 4.40s
```

`git diff --check` was clean.

Wall-clock time is machine-dependent. Test count, semantic coverage, identity preservation, provenance coverage, and repository-wide regression are the primary cross-machine signals.

## Current project state

Phases 90 through 95 establish the structured calculation/explanation pipeline:

```text
query
→ theorem-backed lookup
→ normalized group result
→ EHP / exactness provenance
→ flat proof dependencies
→ recursive proof provenance
→ top-level calculation orchestration
```

Phase 95 is formally COMPLETE. The structured calculation/orchestration layer is fixed through the representative end-to-end regression and the Phase 95 documentation completion sequence.

The next development phase is Phase 96:

```text
human-readable explanation / proof report
```

Phase 96 should consume structured calculation results. It must not redefine proof truth.

## Documentation

```text
README.md
= concise current project status

docs/design.md
= current architecture, semantics, and invariants

docs/roadmap.md
= future-oriented plan and deferred capabilities

docs/development_log.md
= development-history index

docs/development_log/
= archived chronological development records

docs/proof_records.md
= proof-record index

docs/proof_records/
= archived mathematical and infrastructure proof records

docs/code_reference.md
= code navigation reference
```

## Project principle

The project follows a narrow-extension policy:

```text
actual mathematical or proof-search need
→ smallest missing representation or orchestration
→ preserve existing semantics and provenance
→ add focused regression coverage
→ do not pre-implement future phases
```
