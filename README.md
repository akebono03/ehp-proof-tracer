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
- a Flask Web UI for group queries, operation queries, operation proof replay, generator known-group proof replay, and generator exploration,
- explicit operation-fact selection for proof replay,
- browser-side KaTeX rendering of existing LaTeX output,
- Web proof replay with selectable depth 0, 1, or 2,
- safe type-name fallback for unsupported proof statements,
- read-only Web exploration that preserves existing repository grouping and metadata.

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

The Web UI is intentionally a thin presentation layer over existing calculation, operation-query, proof-replay, and exploration infrastructure.

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

The generator exploration path is

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

The Web UI does not parse CLI output or Markdown and does not implement a second mathematical engine.

Current Web files include

```text
web_app.py
web_group_query.py
web_operation_query.py
web_operation_query_proof.py
web_generator_proof.py
web_generator_exploration.py
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

The browser can inspect where one generator occurs in the standard production repository.

Representative inputs are

```text
nu_prime
nu_5
sigma_11
eta_999
```

For `nu_prime`, the Phase 121 browser check showed six direct repository occurrences. The Web view preserves existing grouping and displays conclusion LaTeX, roles, phase, and theorem metadata.

A grouped section may legitimately be empty. Web exploration does not require every existing grouping category to contain an occurrence.

Unknown indexed generators preserve the existing exploration semantics:

```text
eta_999
→ Occurrences: 0
```

This is a normal exploration result, not a not-found error.

`explore sigma_11` currently returns zero direct standard-repository occurrences. This is distinct from recursive proof-scope exploration: `explore-proof sigma_11` can obtain specialized recursive proof-scope occurrences through the existing indexed-\(\sigma_n\) specialization path. The Web `explore` feature intentionally preserves the direct `explore` semantics and does not silently upgrade to `explore-proof`.

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

## Phase 121 closure

Phase 121 re-audited the remaining read-only Web capabilities and selected `explore` ahead of `explore-proof` and `explore-applicable`.

```text
Phase 121-1
→ current explore / explore-proof / explore-applicable audit

Phase 121-2
→ explore selected as the next read-only Web capability

Phase 121-3
→ thin Web adapter boundary fixed
→ existing structured exploration presentation reused
→ no Markdown parsing

Phase 121-4
→ web_generator_exploration.py
→ grouped immutable Web view
→ generator LaTeX
→ conclusion LaTeX
→ roles / phase / theorem metadata
→ normal zero-occurrence handling
→ focused tests: 13 passed
→ Web compatibility tests: 40 passed

Phase 121-5
→ browser/manual integration
→ nu_prime: 6 direct occurrences
→ sigma_11: 0 direct explore occurrences
→ eta_999: 0 occurrences as a normal result
→ group / operation / query-proof coexistence
→ KaTeX rendering confirmed

Phase 121-final
→ documentation update
→ repository-wide regression
```

The final repository-wide Phase 121 regression was

```text
9197 passed in 455.68s (0:07:35)
```

No new theorem root, proof-search rule, query grammar, general \(E/H/\Delta\) evaluator, Toda-bracket solver, qualified execution family, or recursive proof-scope semantics were added in Phase 121.

## Near-term roadmap

The next planning target is the remaining read-only Web surface:

```text
explore-proof
explore-applicable
```

`execute` remains later because it includes candidate selection, ambiguity, and execution semantics rather than read-only inspection.

The next phase should audit which of the remaining read-only capabilities has the clearest structured presentation boundary and strongest user-facing value before implementing anything.

## Current boundaries

The following remain intentionally deferred:

- `explore-proof` Web integration,
- `explore-applicable` Web integration,
- `execute` Web integration,
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
