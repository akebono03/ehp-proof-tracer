# EHP Proof Tracer

EHP Proof Tracer is a Python project for representing, checking, searching, explaining, presenting, exploring, replaying, and safely executing theorem-backed Toda-style homotopy-group calculations.

The project focuses on the free part plus the 2-primary component used by Toda-style calculations. It is not an all-primary calculator for the ordinary homotopy groups of spheres.

The current system provides:

- theorem-backed Toda group queries,
- EHP and proof provenance,
- generator-centered repository exploration,
- recursive proof-scope exploration,
- applicable theorem / lemma discovery,
- bounded qualified execution,
- known-group proof replay,
- operation-fact lookup,
- operation-query proof replay,
- theorem-specific indexed \(\sigma_n\) specialization,
- deliberately narrow existing-proof handoffs for \(E(\nu_5)=\nu_6\) and \(E(\sigma_{11})=\sigma_{12}\),
- a Flask Web UI for group queries, operation queries, operation proof replay, generator known-group proof replay, direct generator exploration, recursive generator proof-scope exploration, and read-only applicability exploration,
- explicit operation-fact selection for proof replay,
- browser-side KaTeX rendering of existing LaTeX output,
- Web proof replay with selectable depth 0, 1, or 2,
- safe type-name fallback for unsupported proof statements,
- read-only direct Web exploration that preserves existing repository grouping and metadata,
- read-only recursive proof-scope Web exploration that preserves existing root / depth / match semantics,
- read-only compact applicability Web exploration that preserves existing source / rule-family presentation semantics while bounding browser output volume.

## Mathematical scope

The project quantity

\[
\pi_{n+k}^n
\]

means the free part plus the 2-primary component represented by this project.

Representative finite-dimensional results include

\[
\pi_5^2=\mathbb Z/2\{\eta_2^3\},
\qquad
\pi_6^3=\mathbb Z/4\{\nu'\},
\]

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\},
\]

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\qquad
\pi_{10}^4=\mathbb Z/8\{\nu_4^2\},
\]

\[
\pi_{11}^5=\mathbb Z/2\{\nu_5^2\},
\qquad
\pi_9^2=0.
\]

Toda Proposition 5.15 coverage includes

\[
\pi_{12}^5=\mathbb Z/2\{\sigma'''\},
\qquad
\pi_{13}^6=\mathbb Z/4\{\sigma''\},
\qquad
\pi_{14}^7=\mathbb Z/8\{\sigma'\},
\]

\[
\pi_{15}^8=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\},
\]

and

\[
\pi_{n+7}^n=
\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
\]

For concrete indexed \(\sigma_n\) with \(n\ge 10\), the existing symbolic Proposition 5.15 proof can be specialized without creating a new independent theorem root.

The consolidated stable 2-primary stem data is

\[
G_0=\mathbb Z\{\iota\},
\quad
(G_1;2)=\mathbb Z/2\{\eta\},
\quad
(G_2;2)=\mathbb Z/2\{\eta^2\},
\]

\[
(G_3;2)=\mathbb Z/8\{\nu\},
\quad
(G_4;2)=0,
\quad
(G_5;2)=0,
\]

\[
(G_6;2)=\mathbb Z/2\{\nu^2\},
\quad
(G_7;2)=\mathbb Z/16\{\sigma\}.
\]

## Proof infrastructure

The proof infrastructure supports:

- an in-memory `ProofRepository`,
- inference-rule catalogs,
- fixed-point-safe producer selection,
- concrete theorem-instance compatibility,
- bounded dependency search with explicit `max_depth`,
- finite producer retry and cycle detection,
- selected-path execution,
- recursive proof ancestry,
- repository-nonmutating exploration and execution planning,
- exact multi-premise production-application recovery,
- qualified execution across admitted production rule families,
- proof-derived known-group identity lookup,
- theorem-specific indexed \(\sigma_n\) specialization,
- reuse of that specialization from the standard `TodaGroupQuery` path,
- user-facing known-group proof replay,
- generator-centered repository occurrence exploration,
- recursive generator proof-scope exploration,
- applicable theorem / lemma discovery grouped by source statement and rule family,
- existing operation-fact lookup,
- operation-query result deduplication without losing raw provenance,
- operation-query proof replay rooted at the selected fact's actual `ProofStep`,
- theorem-specific `E(nu_5)` and `E(sigma_11)` handoffs that preserve existing symbolic proof provenance,
- user-selected replay depth,
- safe mathematical rendering with explicit type-name fallback for unsupported aggregate statements.

General unbounded proof search, theorem ranking, producer ranking, proof-cost optimization, arbitrary operation-query inference fallback, and general \(E/H/\Delta\) evaluation are intentionally not implemented.

## Toda group calculation API

The production one-shot entry point is

```python
build_standard_toda_report(
  n,
  k,
)
```

and the calculation CLI is

```powershell
python main.py n k
```

For example,

```powershell
python main.py 11 7
```

returns

\[
\pi_{18}^{11}\cong
\mathbb Z/16\{\sigma_{11}\}.
\]

## Web UI

The Web UI is intentionally a thin presentation layer over existing calculation, operation-query, proof-replay, direct exploration, recursive proof-scope, and applicability infrastructure.

The group-query path is

```text
browser form
→ Flask route
→ thin Web group-query adapter
→ build_standard_toda_report(n, k)
→ structured presentation
→ existing LaTeX renderer
→ Jinja template
→ KaTeX
```

The operation-query path is

```text
browser operation query
→ Flask route
→ thin Web operation-query adapter
→ existing operation-query facade
→ existing structured presentation
→ statement_latex
→ Jinja template
→ KaTeX
```

The operation proof path is

```text
selected fact
→ existing operation-query proof replay
→ existing replay presentation
→ statement presentation
→ provenance + proof steps
→ Jinja template
→ KaTeX
```

The generator proof path is

```text
generator input
→ thin Web generator-proof adapter
→ existing known-group proof replay
→ existing replay presentation
→ existing statement / generator LaTeX rendering
→ proof steps + safe fallback
→ Jinja template
→ KaTeX
```

The direct generator exploration path is

```text
generator input
→ thin Web generator-exploration adapter
→ explore_standard_repository_generator_input(...)
→ existing RepositoryGeneratorExplorationPresentation
→ Web-only immutable view
→ grouped occurrence metadata + LaTeX
→ Jinja template
→ KaTeX
```

The recursive proof-scope exploration path is

```text
generator input
→ thin Web generator-proof-scope adapter
→ explore_standard_repository_generator_proof_scope_input(...)
→ existing RepositoryProofScopeExplorationResult
→ Web-only immutable view
→ occurrence / Toda membership / map relation counts
→ root / depth / match metadata
→ Jinja template
→ KaTeX
```

The applicability exploration path is

```text
generator input
→ thin Web generator-applicability adapter
→ explore_standard_repository_generator_applicability_input(...)
→ existing RepositoryGeneratorApplicabilityExplorationResult
→ existing RepositoryGeneratorApplicabilityPresentation
→ compact Web-only immutable view
→ source groups + rule families + counts
→ Jinja template
→ KaTeX
```

The Web UI does not parse CLI output or Markdown and does not implement a second mathematical engine.

Current Web files include

```text
web_app.py
web_group_query.py
web_operation_query.py
web_operation_query_proof.py
web_generator_proof.py
web_generator_exploration.py
web_generator_proof_scope.py
web_generator_applicability.py
templates/index.html
static/web_math.js
```

The Python dependency is Flask 3.1.3. Browser-side mathematical rendering uses KaTeX 0.18.7.

Run the local development server with

```powershell
python -m flask --app web_app run --debug
```

and open

```text
http://127.0.0.1:5000/
```

### Group query

A representative query is

```text
n = 11
k = 7
```

which is rendered as

\[
\pi_{18}^{11}\cong
\mathbb Z/16\{\sigma_{11}\}.
\]

### Operation query

Representative Web operation queries are

```text
H(nu_prime)
Delta(iota_9)
E(nu_5)
E(sigma_11)
```

Multiple mathematical facts are listed explicitly. A fact is not automatically selected for proof replay.

### Web query-proof

Each presented operation fact has an explicit proof-selection action.

The selected fact is replayed from its own existing `ProofStep`, and the Web result shows:

- the selected conclusion,
- theorem / phase provenance when available,
- repository depth,
- bounded proof steps,
- rule names,
- KaTeX-renderable statements,
- safe type-name fallback for unsupported aggregate statements.

### Web generator proof

The browser can replay an existing known-group proof by generator input.

Representative inputs are

```text
sigma_11
nu_prime
nu_5
```

For `sigma_11`, the result is

\[
\pi_{18}^{11}
=
\mathbb Z/16\{\sigma_{11}\}.
\]

For `nu_prime`, the result is

\[
\pi_6^3
=
\mathbb Z/4\{\nu'\}.
\]

The browser exposes replay depth choices

```text
0
1
2
```

for both operation proof replay and generator proof replay.

Depth 0 shows only the replay root. Depth selection changes only the visible existing ancestry. It does not perform new proof search.

### Web generator exploration

The browser can inspect where one generator occurs directly in the standard production repository.

Representative inputs are

```text
nu_prime
nu_5
sigma_11
eta_999
```

For `nu_prime`, the Phase 121 browser check showed six direct repository occurrences. The Web view preserves existing grouping and displays conclusion LaTeX, roles, phase, and theorem metadata.

Unknown indexed generators preserve the existing exploration semantics:

```text
eta_999
→ Occurrences: 0
```

This is a normal exploration result, not a not-found error.

`explore sigma_11` returns zero direct standard-repository occurrences.

### Web generator proof-scope exploration

The browser can inspect recursive proof ancestry for one generator without changing proof-scope semantics.

Representative inputs are

```text
nu_prime
sigma_11
eta_999
```

For `sigma_11`, the direct and recursive exploration semantics intentionally differ:

```text
generator explore sigma_11
→ Occurrences: 0

generator proof-scope exploration sigma_11
→ Proof-scope occurrences: 1
```

For `eta_999`:

```text
Proof-scope occurrences: 0
Toda memberships: 0
Map relations: 0
```

This is a normal result, not an error.

### Web applicability exploration

The browser can inspect read-only applicable theorem / lemma candidates for one generator.

The Web path preserves the existing applicability presentation hierarchy:

```text
generator
→ proof-scope occurrences
→ applicability candidates
→ source statements with candidates
→ rule groups
→ rule families
```

The Web adapter does not select a candidate, execute a rule, expose candidate identity as an execution control, or parse CLI Markdown.

Representative Phase 123 browser results:

```text
nu_prime
Proof-scope occurrences: 626
Applicability candidates: 176616
Source statements with candidates: 542
Rule groups: 123300
Rule families: 29308
```

The `nu_prime` source categories were

```text
Toda memberships: 46
Map relations: 44
Other statements: 452
```

To keep the generated browser page bounded without changing the underlying result:

```text
at most 5 source statements are rendered per category
at most 10 rule families are rendered per displayed source
rule-family details use a collapsed <details> element
full summary counts remain visible
omitted source / rule-family counts are shown explicitly
```

For `sigma_11`:

```text
Proof-scope occurrences: 1
Applicability candidates: 686
Source statements with candidates: 1
Rule groups: 472
Rule families: 112
```

The source statement includes

\[
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\}.
\]

For `eta_999`:

```text
Proof-scope occurrences: 0
Applicability candidates: 0
Source statements with candidates: 0
Rule groups: 0
Rule families: 0
```

This is a normal result, not an error.

## Operation query

Operation query is lookup-first.

Representative results include

\[
H(\nu')=\eta_5,
\]

\[
\Delta(\iota_9)=\pm(2\nu_4-E\nu'),
\]

\[
E(\eta_2\nu')=0,
\]

\[
E(\nu_5)=\nu_6,
\]

and

\[
E(\sigma_{11})=\sigma_{12}.
\]

The two narrow theorem-specific handoffs do not turn `query` into a general inference engine or evaluator.

## Phase 123 closure

Phase 123 exposed the existing `explore-applicable` capability as a read-only compact Web surface.

```text
Phase 123-1
→ current applicability facade / presentation / compact and detailed renderer audit

Phase 123-2
→ read-only compact Web exposure selected
→ candidate selection / execute / detailed toggle excluded

Phase 123-3
→ thin Web adapter boundary fixed
→ existing applicability facade and presentation reused
→ source classification and relevance ordering reused
→ no CLI Markdown parsing

Phase 123-4
→ web_generator_applicability.py
→ immutable Web applicability views
→ full summary counts
→ source statement / root / depth / type / raw-candidate metadata
→ rule-family name / catalog-entry count / raw-candidate count
→ normal zero-result handling
→ focused tests: 13 passed

Phase 123-5
→ browser/manual audit
→ nu_prime / sigma_11 / eta_999 verified
→ very large nu_prime page identified as a browser-scale presentation problem

Phase 123-5A
→ compact browser-volume fix
→ max 5 sources per category
→ max 10 rule families per displayed source
→ collapsed rule-family details
→ omitted-count messages
→ underlying applicability result unchanged
→ focused regression: 17 passed

Phase 123-5B
→ browser/manual re-audit passed
→ nu_prime full summary counts preserved
→ sigma_11 compact display verified
→ eta_999 zero-result semantics preserved

Phase 123-final
→ documentation update
→ repository-wide regression
```

The final repository-wide Phase 123 regression was

```text
9229 passed in 509.16s (0:08:29)
```

No new theorem root, proof-search rule, query grammar, general \(E/H/\Delta\) evaluator, Toda-bracket solver, qualified execution family, candidate-selection semantics, or new applicability semantics were added in Phase 123.

## Near-term roadmap

Phase 123 completes the remaining read-only Web integration that had been prioritized before `execute`.

The next phase should audit the boundary between:

```text
execute Web integration
and
Web UI usability / organization cleanup
```

before implementing either broadly.

`execute` remains a separate capability because it includes candidate selection, ambiguity handling, and execution semantics rather than read-only inspection.

## Current boundaries

The following remain intentionally deferred:

- `execute` Web integration,
- candidate-selection UI,
- theorem ranking and proof-cost optimization,
- producer ranking,
- general unbounded backtracking,
- persistent proof cache,
- repository snapshot/versioning,
- free-form natural-language element search,
- wildcard family search,
- arbitrary nested operation-query grammar,
- Unicode-composition and LaTeX input parsing,
- four-or-more-term operation-query composition,
- three-term composition as a map-operation operand,
- general composition evaluation,
- general Toda-bracket solving,
- bracket-value and coset / indeterminacy computation,
- general \(E/H/\Delta\) evaluation,
- arbitrary operation-query inference fallback,
- unrestricted symbolic AST substitution,
- rich graph proof visualization,
- odd-primary full integration,
- an all-primary ordinary sphere-homotopy calculator.

## Project principle

```text
actual mathematical or proof-search need
→ smallest missing representation or orchestration
→ preserve existing semantics and provenance
→ add focused regression coverage
→ measure pressure before expanding or optimizing
→ do not pre-implement future phases
```
