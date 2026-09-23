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
- a Flask Web UI for group queries, operation queries, operation proof replay, generator proof replay, direct generator exploration, recursive generator proof-scope exploration, applicability exploration, and qualified generator execution,
- explicit candidate selection when an execution request is ambiguous,
- browser-side KaTeX rendering of existing LaTeX output,
- Web proof replay with selectable depth 0, 1, or 2,
- safe type-name fallback for unsupported proof statements,
- workflow navigation that groups the single-page Web forms by calculation/query, proof/exploration, and applicability/execution.

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
- user-facing qualified execution with explicit `NONE`, `AMBIGUOUS`, and `EXECUTED` states,
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

The Web UI is intentionally a thin presentation layer over existing calculation, operation-query, proof-replay, exploration, applicability, and qualified-execution infrastructure.

It does not parse CLI output or Markdown and does not implement a second mathematical engine.

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
web_generator_execution.py
templates/index.html
static/web_math.js
```

The Python dependency is Flask 3.1.3. Browser-side mathematical rendering uses KaTeX 0.18.7.

Run the local development server with

```powershell
python -m flask --app web_app:create_app run
```

and open

```text
http://127.0.0.1:5000/
```

### Web workflow

The single-page UI is grouped as follows.

```text
Calculation and queries
→ Group query
→ Operation query

Proof and exploration
→ Generator proof
→ Generator exploration
→ Generator proof-scope exploration

Applicability
→ Applicable theorem / lemma candidates
→ Execute theorem / lemma candidate
```

The navigation links are presentation-only anchors. Their order is not a theorem ranking.

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

### Operation query and query-proof

Representative Web operation queries are

```text
H(nu_prime)
Delta(iota_9)
E(nu_5)
E(sigma_11)
```

Multiple mathematical facts are listed explicitly. A fact is not automatically selected for proof replay.

The selected fact is replayed from its own existing `ProofStep`. The Web result can show theorem / phase provenance, bounded proof steps, rule names, KaTeX-renderable statements, and safe type-name fallback.

### Generator proof

Representative inputs are

```text
sigma_11
nu_prime
nu_5
```

For `nu_prime`:

\[
\pi_6^3=\mathbb Z/4\{\nu'\}.
\]

The browser exposes replay depth choices `0`, `1`, and `2`. Depth selection changes only visible existing ancestry; it does not perform new proof search.

### Generator exploration

Representative inputs are

```text
nu_prime
nu_5
sigma_11
eta_999
```

For `nu_prime`, the direct repository exploration returns six occurrences.

Unknown indexed generators preserve zero-result semantics:

```text
eta_999
→ Occurrences: 0
```

This is a normal result, not a not-found error.

### Generator proof-scope exploration

Representative inputs are

```text
nu_prime
sigma_11
eta_999
```

For `sigma_11`:

```text
direct exploration
→ Occurrences: 0

proof-scope exploration
→ Proof-scope occurrences: 1
```

For `eta_999`:

```text
Proof-scope occurrences: 0
Toda memberships: 0
Map relations: 0
```

### Applicability exploration

The browser can inspect read-only theorem / lemma applicability candidates.

The presentation hierarchy is

```text
generator
→ proof-scope occurrences
→ applicability candidates
→ source statements with candidates
→ rule groups
→ rule families
```

Representative `nu_prime` counts are

```text
Proof-scope occurrences: 626
Applicability candidates: 176616
Source statements with candidates: 542
Rule groups: 123300
Rule families: 29308
```

To keep browser output bounded while preserving the underlying result:

```text
at most 5 source statements are rendered per category
at most 10 rule families are rendered per displayed source
rule-family details use a collapsed <details> element
full aggregate counts remain visible
omitted counts are shown explicitly
```

### Generator execution

Phase 125 connects the existing qualified user-execution workflow to the Web UI.

The path is

```text
generator input
→ thin Web execution adapter
→ existing execution workflow facade
→ executable target resolution
→ NONE / AMBIGUOUS / EXECUTED
→ candidate selection when required
→ existing qualified execution
→ existing executed ProofStep
→ structured result + proof
→ Jinja
→ KaTeX
```

The Web adapter does not resolve candidates independently, rank targets, add a new execution family, or parse CLI Markdown.

`NONE` is presented as a normal no-target result.

```text
eta_999
→ No executable target found for this generator.
```

`AMBIGUOUS` presents existing candidates and requires explicit selection.

For `nu_prime`, the browser exposes the same two executable targets as the CLI:

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\},
\]

and

\[
\Delta(\iota_9)=\pm(2\nu_4-E\nu').
\]

Selecting candidate 1 or 2 delegates the candidate number back to the existing execution facade.

`EXECUTED` presents:

```text
Result
Premises
Rule
Conclusion
Provenance
```

The browser/manual audit also confirmed that the current `nu_5` execution result matches the existing CLI behavior. Phase 125 deliberately does not change generator-to-target resolution semantics.

## Operation query

Operation query remains lookup-first.

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

The narrow theorem-specific handoffs do not turn `query` into a general inference engine or evaluator.

## Phase 125 closure

Phase 125 connected the existing `execute` workflow to the single-page Web UI without changing mathematical or execution semantics.

```text
Phase 125-1
→ current execution workflow and Phase 108 tests audited
→ NONE / AMBIGUOUS / EXECUTED structure confirmed
→ candidate and execution presentations confirmed reusable

Phase 125-2
→ Web integration scope frozen
→ generator → candidates → explicit selection → execution → Result + Proof
→ no ranking, new qualified family, or general proof search

Phase 125-3
→ thin Web adapter design fixed
→ structured facade/presentation reuse
→ no CLI Markdown parsing

Phase 125-4
→ web_generator_execution.py added
→ web_app.py and templates/index.html connected
→ focused regression: 14 passed in 29.80s

Phase 125-5
→ browser/manual audit
→ nu_prime candidate list and selection verified
→ eta_999 NONE verified
→ KaTeX verified
→ existing Web capabilities coexist
→ nu_5 Web result confirmed equal to existing CLI result

Phase 125-final
→ documentation updated
→ repository-wide regression passed
```

The final repository-wide Phase 125 regression was

```text
9243 passed in 555.37s (0:09:15)
```

No new theorem root, proof-search rule, query grammar, general \(E/H/\Delta\) evaluator, Toda-bracket solver, qualified execution family, theorem ranking, candidate ranking, or generator-to-target resolution semantics were added in Phase 125.

## Near-term roadmap

The next phase should audit user-execution target resolution before adding more execution capability.

The main pressure observed during Phase 125 is that a generator input can participate in an executable proof whose conclusion is not the most obvious generator-centered result. For example, the current `nu_5` Web execution matches the CLI and resolves to the existing \(\pi_6^2\) qualified execution path.

Phase 126 should therefore audit:

```text
generator occurrence / relevance
→ executable target resolution
→ target ordering / inclusion semantics
→ user expectation
```

This is an audit first. It should not introduce ranking or new execution semantics unless an actual defect is demonstrated.

## Current boundaries

The following remain intentionally deferred:

- semantic executable-target ranking,
- automatic "best target" selection,
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
