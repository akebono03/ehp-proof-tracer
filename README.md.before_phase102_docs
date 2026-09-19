# EHP Proof Tracer

EHP Proof Tracer is a Python project for representing, checking, searching, explaining, presenting, and exploring theorem-backed Toda-style homotopy-group calculations.

The project currently focuses on the 2-primary Toda groups, EHP exactness, explicit proof provenance, the calculation spine through stable stems $G_0$ to $G_7$, theorem-backed repository exploration, and production user-facing paths for both group calculation and generator-centered exploration.

## Current mathematical coverage

Representative finite-dimensional results include:

$$
\pi_5^2=\mathbb Z/2\{\eta_2^3\},
\qquad
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

$$
\pi_7^4=\mathbb Z\{\nu_4\}\oplus\mathbb Z/4\{E\nu'\}.
$$

$$
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\qquad
\pi_{10}^4=\mathbb Z/8\{\nu_4^2\}.
$$

$$
\pi_{11}^5=\mathbb Z/2\{\nu_5^2\},
\qquad
\pi_9^2=0.
$$

$$
\pi_{12}^5=\mathbb Z/2\{\sigma'''\}.
$$

The stable 2-primary stem data currently consolidated in the project is:

$$
G_0=\mathbb Z\{\iota\},
\quad
(G_1;2)=\mathbb Z/2\{\eta\},
\quad
(G_2;2)=\mathbb Z/2\{\eta^2\},
$$

$$
(G_3;2)=\mathbb Z/8\{\nu\},
\quad
(G_4;2)=0,
\quad
(G_5;2)=0,
$$

$$
(G_6;2)=\mathbb Z/2\{\nu^2\},
\quad
(G_7;2)=\mathbb Z/16\{\sigma\}.
$$

This is not an all-primary calculator for ordinary homotopy groups of spheres.

## Proof infrastructure

The proof-search infrastructure supports:

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

$$
\pi_{n+k}^n.
$$

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

For the zero group:

```text
group_structure = None
generators = ()
generator_orders = ()
```

## EHP and exactness provenance

For theorem-backed proofs containing actual EHP ancestry, the project can extract EHP exactness windows, a contiguous EHP sequence, exactness-use provenance, and known group information on EHP terms.

The representative $\pi_9^5$ proof yields

$$
\pi_{10}^9
\xrightarrow{\Delta}
\pi_8^4
\xrightarrow{E}
\pi_9^5
\xrightarrow{H}
\pi_9^9
\xrightarrow{\Delta}
\pi_7^4.
$$

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

The unified presentation-level report renderer is:

```python
render_toda_full_proof_report_markdown(
  presentation,
)
```

Unknown statement types are kept as explicit safe fallbacks rather than guessed into mathematical prose.

## Standard production repository

The production builder is:

```python
build_standard_production_proof_repository()
```

It assembles theorem-backed entries needed by the supported production paths without reproducing Phase-specific bootstrap logic at each call site.

Production repository assembly does not create new theorem truth.

## Repository-free one-shot calculation API

The production calculation entry point is:

```python
build_standard_toda_report(
  n,
  k,
)
```

The production calculation path is:

```text
raw n,k
↓
build_standard_toda_report()
↓
build_standard_production_proof_repository()
↓
build_toda_report(repository, n, k)
↓
TodaCalculationReportResult
```

A representative call:

```python
result = build_standard_toda_report(
  5,
  7,
)
```

reaches

$$
\pi_{12}^5=\mathbb Z/2\{\sigma'''\}.
$$

## Generator input resolution

Generator-centered exploration accepts a small explicit input language.

Supported family aliases include:

```text
η / eta
ν / nu
σ / sigma
ι / iota
```

Indexed examples include:

```text
eta_2
nu_5
sigma_8
iota_4
```

Decorated aliases include:

```text
ν′
ν'
nu'
nu_prime

σ'
sigma_prime
σ''
sigma_double_prime
σ'''
sigma_triple_prime
```

Resolution produces an exact `GeneratorSymbol`. An unindexed family is not a wildcard.

## Generator-centered repository exploration

The repository-explicit entry point is:

```python
explore_repository_generator(
  repository,
  generator,
)
```

The production one-shot entry point is:

```python
explore_standard_repository_generator_input(
  generator_input,
)
```

The production exploration path is:

```text
generator string
↓
resolve_generator_input()
↓
build_standard_production_proof_repository()
↓
explore_repository_generator()
↓
RepositoryGeneratorExplorationReport
↓
grouped Markdown
```

Exploration is occurrence-based, not entry-deduplicated. Different structural paths remain distinct occurrences even when they occur in the same repository entry.

For `nu_prime`, the current production repository yields six structural occurrences, including:

$$
\pi_6^3=\mathbb Z/4\{\nu'\},
$$

$$
\pi_7^4=\mathbb Z\{\nu_4\}\oplus\mathbb Z/4\{E\nu'\},
$$

$$
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\},
$$

$$
\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}.
$$

Unknown but syntactically valid indexed generators return a normal zero-occurrence report.

## Command-line interface

The existing group-calculation command remains:

```powershell
python main.py n k
```

For example:

```powershell
python main.py 5 7
```

prints the human-readable proof report for $\pi_{12}^5$.

Phase 101 adds generator exploration without breaking the positional calculation command:

```powershell
python main.py explore "nu'"
```

Equivalent aliases such as `nu_prime` are accepted.

Exploration help:

```powershell
python main.py explore --help
```

Calculation CLI behavior:

```text
FOUND
→ print report(s)
→ exit 0

MULTIPLE_RESULTS
→ print all reports in candidate order
→ exit 0

NOT_FOUND
→ explicit not-found message
→ exit 1

invalid calculation syntax or semantic input
→ argparse error
→ exit 2
```

Exploration CLI behavior:

```text
valid input with occurrence(s)
→ grouped Markdown
→ exit 0

valid input with zero occurrences
→ Occurrences: 0
→ exit 0

invalid / malformed generator
→ argparse error
→ exit 2

missing / extra explore argument
→ argparse error
→ exit 2

explore --help
→ stdout
→ exit 0
```

The calculation CLI validates

$$
n>0,
\qquad
k\ge 0
$$

before constructing the production repository.

## Current boundaries

The following are intentionally deferred:

- automatic symbolic higher-range instantiation,
- target-only unknown-right-hand-side proof search,
- best-proof ranking or proof-cost optimization,
- full prose rendering for every historical aggregate statement,
- free-form natural-language element search,
- wildcard family search,
- general composition evaluation,
- general Toda-bracket solving,
- coset / indeterminacy computation,
- automatic applicable-lemma discovery,
- automatic enumeration of unstated mathematical consequences,
- Web UI,
- odd-primary full integration,
- an all-primary ordinary sphere-homotopy calculator.

## Verification

Latest confirmed Phase 101 validation:

```text
Phase 101-2 related:
108 passed in 9.43s

Phase 101-4 related:
104 passed in 11.12s

Phase 101-5 related:
57 passed in 8.49s

repository-wide:
8058 passed in 133.01s

git diff --check:
clean
```

## Current project state

Calculation:

```text
raw n,k
→ CLI or direct Python call
→ semantic validation
→ standard production repository
→ calculation
→ provenance extraction
→ structured presentation
→ human-readable proof report
```

Generator exploration:

```text
generator string
→ CLI or production one-shot facade
→ canonical generator resolution
→ standard production repository
→ structural occurrence lookup
→ role classification
→ grouped presentation
→ Markdown report
```

Phase 100 closes the production calculation path.

Phase 101 closes the production generator-exploration path.

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
= mathematical and infrastructure proof records

docs/code_reference.md
= code navigation reference
```

## Project principle

```text
actual mathematical or proof-search need
→ smallest missing representation or orchestration
→ preserve existing semantics and provenance
→ add focused regression coverage
→ do not pre-implement future phases
```
