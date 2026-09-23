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
- deliberately narrow existing-proof handoffs for \(E(\nu_5)=\nu_6\), \(E(\sigma_{11})=\sigma_{12}\), \(E(\nu_5\eta_8)=0\), and \(E\nu' \in \pi_7^4\),
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
- theorem-specific `E(nu_5)`, `E(sigma_11)`, `E(nu_5 o eta_8)`, and `E(nu_prime)` handoffs that preserve existing proof provenance,
- user-facing qualified execution with explicit `NONE`, `AMBIGUOUS`, and `EXECUTED` states,
- user-selected replay depth,
- safe mathematical rendering with explicit type-name fallback for unsupported aggregate statements.

General unbounded proof search, theorem ranking, producer ranking, proof-cost optimization, arbitrary operation-query inference fallback, general membership evaluation, and general \(E/H/\Delta\) evaluation are intentionally not implemented.

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

\[
E(\sigma_{11})=\sigma_{12},
\]

\[
E(\nu_5\eta_8)=0,
\]

and

\[
E\nu' \in \pi_7^4.
\]

The `E(nu_prime)` result is deliberately a membership result, not a synthetic equality \(E(\nu')=E\nu'\).

Its theorem-specific handoff reuses the existing Toda Proposition 5.6 decomposition

\[
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}.
\]

The specialized membership `ProofStep` has that existing decomposition step as its direct premise, so `query-proof` preserves the actual Proposition 5.6 ancestry.

The handoff is exact and narrow:

```text
query "E(nu_prime)"
→ direct lookup first
→ exact theorem-specific guard
→ Proposition 5.6 decomposition match
→ E nu' in pi_7^4
→ query-proof replay
```

It does not recursively scan arbitrary group structures for suspensions and does not introduce a general membership evaluator or general \(E\) evaluator.

The `GROUP_MEMBERSHIP` operation-query match kind classifies this user-facing result. It does not change direct lookup semantics or turn arbitrary containment into an operation result.

## Phase 126–129 closure

Phase 126 separated proof-scope relevance, applicability relevance, and executable relevance.

Phase 127 audited remaining operation-query pressure.

Phase 128 implemented the exact theorem-specific handoff

\[
E(\nu_5\eta_8)=0
\]

from existing Proposition 5.8 provenance.

Phase 129 audited the remaining `E(nu_prime)` pressure before implementation. The repository already contained \(E\nu'\) as the order-four generator in the Proposition 5.6 decomposition of \(\pi_7^4\). The audit selected membership as the natural operation result:

\[
E\nu' \in \pi_7^4.
\]

Phase 129 then implemented a theorem-specific membership handoff without broadening direct lookup or containment semantics.

Focused validation:

```text
12 passed
63 passed
```

Manual CLI validation:

```text
python main.py query "E(nu_prime)"
→ E nu' in pi_7^4

python main.py query-proof "E(nu_prime)" --depth 1
→ Depth 0: E nu' in pi_7^4
→ Depth 1: pi_7^4 = Z{nu_4} ⊕ Z/4{E nu'}
```

Final repository-wide regression:

```text
9268 passed in 569.71s (0:09:29)
```

Phase 129 did not add a general \(E\) evaluator, general membership evaluator, recursive arbitrary containment lookup, parser expansion, new independent theorem root, new qualified execution family, theorem ranking, or automatic target selection.

## Near-term roadmap

Phase 129 is complete.

The next phase should begin with a capability re-audit rather than pre-implementing a general evaluator.

The remaining operation pressures include queries such as:

```text
H(nu_5)
Delta(nu_prime)
H(sigma_11)
Delta(sigma_11)
```

These were previously classified as requiring additional mathematical proof support rather than a small existing-proof handoff.

The next decision order remains:

```text
actual user pressure
→ current repository/proof support
→ result semantics
→ provenance reuse
→ smallest missing capability
→ scope freeze before implementation
```

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
- general membership evaluation,
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
