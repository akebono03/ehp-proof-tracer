# EHP Proof Tracer

EHP Proof Tracer is a Python project for representing, checking, searching, explaining, and presenting theorem-backed Toda-style homotopy-group calculations.

The project currently focuses on the 2-primary Toda groups \(\pi_i^n\), EHP exactness, explicit proof provenance, and the calculation spine leading through stable stems \(G_0\) to \(G_7\).

## Current mathematical coverage

Representative finite-dimensional results include:

\[
\pi_5^2=\mathbb Z/2\{\eta_2^3\},
\qquad
\pi_6^3=\mathbb Z/4\{\nu'\},
\]

\[
\pi_7^4=\mathbb Z\{\nu_4\}\oplus \mathbb Z/4\{E\nu'\},
\]

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\qquad
\pi_{10}^4=\mathbb Z/8\{\nu_4^2\},
\]

\[
\pi_{11}^5=\mathbb Z/2\{\nu_5^2\},
\qquad
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
\qquad
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
\qquad
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

The calculation entry point is:

```python
build_toda_calculation_result(
  repository,
  query,
)
```

where `query` is a `TodaGroupQuery(n, k)` representing

\[
\pi_{n+k}^n.
\]

The calculation flow is:

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

Direct results take precedence over aggregate fallback results. Multiple valid results are preserved; the calculation layer does not silently rank or choose one result.

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

For aggregate-derived results, `goal_source` preserves the original aggregate `ProofRepositoryEntry` and branch path, while `group_result.proof_step` preserves the original branch `ProofStep`.

Status semantics are:

```text
0 candidates  -> NOT_FOUND
1 candidate   -> FOUND
2+ candidates -> MULTIPLE_RESULTS
```

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

The representative \(\pi_9^5\) proof yields

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

The recursive representation preserves one node per `ProofStep` identity, all proof edges, original premise indices, shared dependencies, stable traversal order, cycle-safe traversal, and shortest-depth metadata.

The key identity invariant is:

```text
group_result.proof_step
is dependency_result.root_step
is recursive_provenance.root_step
```

## Presentation and proof-report layer

The presentation architecture is one-way:

```text
proof / calculation truth
↓
structured presentation
↓
human-readable renderer
```

Presentation never changes proof truth.

The structured presentation layer covers:

```text
target
group structure
generators
generator orders
EHP sequence
exactness uses
proof-step role
repository / theorem / phase metadata
calculation goal source
dependency-first proof flow
shared-dependency information
```

The main presentation modules are:

```text
toda_presentation.py
toda_ehp_presentation.py
toda_proof_presentation.py
toda_proof_flow_presentation.py
toda_end_to_end_presentation.py
```

The renderer modules are:

```text
toda_human_readable_renderer.py
toda_proof_narrative_renderer.py
toda_full_proof_report_renderer.py
```

The unified presentation-level report renderer is:

```python
render_toda_full_proof_report_markdown(
  presentation,
)
```

It combines:

```text
Result
Source
EHP sequence
Exactness
Proof flow
Readable proof narrative
```

Unknown statement types are kept as explicit safe fallbacks rather than guessed into mathematical prose.

## User-facing calculation-to-report API

Phase 97 added the structured top-level reporting layer. Phase 98 adds a thin convenience boundary without changing calculation or proof semantics.

The lowest-level general reporting entry point remains:

```python
build_toda_calculation_report_result(
  repository,
  query,
)
```

with:

```python
query = TodaGroupQuery(
  n=n,
  k=k,
)
```

The user-facing convenience entry point is:

```python
build_toda_report(
  repository,
  n=n,
  k=k,
)
```

The complete convenience flow is:

```text
raw n, k
↓
build_toda_report()
↓
TodaGroupQuery
↓
build_toda_calculation_report_result()
↓
TodaCalculationReportResult
```

`build_toda_report()` is intentionally thin. It constructs `TodaGroupQuery` and delegates to the existing Phase 97 reporting API. It does not reimplement validation, lookup, normalization, provenance, presentation, or rendering.

`TodaCalculationReportResult` retains the original `TodaCalculationResult` and an ordered tuple of `TodaCalculationReportCandidate` objects.

Each report candidate retains:

```text
source_candidate
presentation
report
```

The identity invariant is:

```text
report_result.candidates[i].source_candidate
is report_result.calculation_result.candidates[i]
```

For `NOT_FOUND`:

```text
report_result.candidates == ()
report_result.reports == ()
report_result.report raises ValueError
```

For `FOUND`:

```text
one report candidate
report_result.report
report_result.reports == (report_result.report,)
```

For `MULTIPLE_RESULTS`:

```text
all report candidates are preserved in calculation order
report_result.reports contains every report in candidate order
report_result.report raises ValueError
```

The reporting layer never silently selects a preferred result.

A stricter query-object-based single-result API is also available:

```python
build_toda_found_calculation_report_result(
  repository,
  query,
)
```

It requires calculation status `FOUND`.

A fixed human-readable `NOT_FOUND` message is intentionally not part of the core result model. Message wording belongs to a future CLI, Web UI, or other presentation surface.

## Representative end-to-end coverage

Using aggregate theorem entries in a `ProofRepository`, the shortest user-facing calculation-to-report path is regression-tested for:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5.
\]

These cases cover:

```text
raw n,k facade input
direct sums
finite cyclic groups
zero groups
nested aggregate branches
generator orders
goal-source provenance
EHP provenance
exactness provenance
recursive provenance
dependency-first presentation
LaTeX / Markdown rendering
mathematical statement rendering
unified reports
single FOUND report access
ordered report collection access
repository non-mutation
```

For actual \(\pi_9^5\), the report can present:

\[
\Delta:\pi_9^9\to\pi_7^4
\]

as injective,

\[
H:\pi_9^5\to\pi_9^9
\]

as the zero map,

\[
E:\pi_8^4\to\pi_9^5
\]

as surjective, and the final result

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}.
\]

## Current boundaries

The calculation and reporting layers currently handle concrete finite-dimensional theorem branches.

The following are intentionally deferred:

- automatic instantiation of symbolic higher-range branches,
- target-only generation of unknown right-hand-side proof goals,
- bounded proof-search fallback from a target-only query,
- detailed calculation-failure taxonomy beyond `NOT_FOUND / FOUND / MULTIPLE_RESULTS`,
- automatic ranking or best-result selection,
- full mathematical prose rendering for every historical aggregate statement type,
- fixed human-readable `NOT_FOUND` messages in the core result model,
- CLI and Web UI surfaces,
- general theorem proving,
- odd-primary full integration,
- an all-primary ordinary sphere-homotopy calculator.

## Verification

Latest confirmed Phase 98 validation:

```text
Phase 98-6 focused:
8 passed in 8.64s

Phase 98 related:
27 passed in 9.94s

repository-wide:
7643 passed in 123.73s

git diff --check:
clean
```

Wall-clock time is machine-dependent. Test count, semantic coverage, identity preservation, provenance coverage, report determinism, and repository-wide regression are the primary cross-machine signals.

## Current project state

Phases 90 through 98 establish:

```text
query
→ theorem-backed lookup
→ normalized group result
→ EHP / exactness provenance
→ flat proof dependencies
→ recursive proof provenance
→ calculation orchestration
→ structured presentation
→ dependency-first proof flow
→ LaTeX / Markdown rendering
→ mathematical statement rendering
→ readable proof narrative
→ unified full proof report
→ top-level calculation-to-report result
→ raw n,k convenience facade
→ single FOUND report access
→ ordered report collection access
```

Phase 98 is formally COMPLETE after the final documentation audit.

The next development phase should start with an audit of the next actual user-facing need rather than adding speculative convenience. Natural candidates include CLI / Web UI work or mathematical exploration/query capabilities, but the exact next phase should be chosen from observed usage pressure.

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
