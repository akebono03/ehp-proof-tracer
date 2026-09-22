# EHP Proof Tracer

EHP Proof Tracer is a Python project for representing, checking, searching, explaining, presenting, exploring, replaying, and safely executing theorem-backed Toda-style homotopy-group calculations.

The project focuses on the free part plus the 2-primary component used by Toda-style calculations. It is not an all-primary calculator for the ordinary homotopy groups of spheres.

The current system provides:

- theorem-backed Toda group queries,
- EHP and proof provenance,
- recursive proof-scope exploration,
- applicable theorem / lemma discovery,
- bounded qualified execution,
- known-group proof replay,
- operation-fact lookup,
- operation-query proof replay,
- theorem-specific indexed \(\sigma_n\) specialization,
- deliberately narrow existing-proof handoffs for \(E(\nu_5)=\nu_6\) and \(E(\sigma_{11})=\sigma_{12}\),
- a Flask Web UI for group queries and operation queries,
- explicit operation-fact selection for proof replay,
- browser-side KaTeX rendering of existing LaTeX output,
- Web proof replay with selectable depth 0, 1, or 2,
- safe type-name fallback for unsupported proof statements.

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

The Web UI is intentionally a thin presentation layer over existing calculation, operation-query, and proof-replay infrastructure.

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

The Web UI does not parse CLI output and does not implement a second mathematical engine.

Current Web files include

```text
web_app.py
web_group_query.py
web_operation_query.py
web_operation_query_proof.py
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

The browser exposes replay depth choices

```text
0
1
2
```

where depth 0 shows only the replay root.

Depth selection changes only the visible existing ancestry. It does not perform new proof search.

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

## Phase 118 closure

Phase 118 connected the existing operation-query and query-proof capabilities to the Web UI without adding new mathematics.

```text
Phase 118-1
→ Web operation-query boundary audit
→ existing structured presentation selected as Web boundary

Phase 118-2
→ operation-query Web UI
→ existing statement_latex rendered through KaTeX
→ multiple facts listed without auto-selection

Phase 118-3
→ explicit fact selection
→ existing query-proof replay connected to Web
→ conclusion / provenance / proof steps displayed

Phase 118-4
→ Web replay depth 0 / 1 / 2
→ unsupported-statement safe fallback
→ multiple-fact selection regression
→ KaTeX browser smoke
```

The final repository-wide Phase 118 regression was

```text
9169 passed in 465.97s (0:07:45)
```

No new theorem root, query grammar, general \(E/H/\Delta\) evaluator, or Toda-bracket solver was added in Phase 118.

## Near-term roadmap

The next phase is Phase 119.

Phase 119 will re-audit which existing user-facing capabilities should be connected to the Web next, especially:

```text
show-proof
explore
explore-proof
explore-applicable
execute
```

`execute` has more semantic and selection complexity than read-only query / replay, so it should not be exposed automatically without a dedicated boundary audit.

## Current boundaries

The following remain intentionally deferred:

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
