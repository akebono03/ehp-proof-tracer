# EHP Proof Tracer

EHP Proof Tracer is a Python project for representing, checking, searching, explaining, presenting, exploring, replaying, and safely executing theorem-backed Toda-style homotopy-group calculations.

The project focuses on the free part plus the 2-primary component used by Toda-style calculations. It is not an all-primary calculator for the ordinary homotopy groups of spheres.

The current system provides:

- theorem-backed Toda group queries,
- foundational query semantics for diagonal, below-diagonal, and circle cases,
- EHP and proof provenance,
- generator-centered repository exploration,
- recursive proof-scope exploration,
- applicable theorem / lemma discovery,
- bounded qualified execution,
- known-group proof replay,
- operation-fact lookup,
- operation-query proof replay,
- theorem-specific indexed \(\sigma_n\) specialization,
- theorem-specific standard-query recovery from existing proof ancestry,
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

\[
\pi_{16}^9=
\mathbb Z/16\{\sigma_9\},
\]

and

\[
\pi_{n+7}^n=
\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
\]

For concrete indexed \(\sigma_n\) with \(n\ge 10\), the existing symbolic Proposition 5.15 proof is specialized without creating a new independent theorem root. The boundary case \(n=9\) reuses the existing concrete \(\pi_{16}^9\) proof from Proposition 5.15 ancestry.

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

## Standard group-query semantics

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

The sphere dimension must satisfy

```text
n > 0
```

while the stem \(k\) may be negative.

Phase 130 established the following foundational semantics:

\[
k=0
\quad\Longrightarrow\quad
\pi_n^n\cong\mathbb Z\{\iota_n\}.
\]

For the circle,

\[
n=1,\quad k\ge1
\quad\Longrightarrow\quad
\pi_{1+k}^1=0,
\]

using the existing symbolic Phase 56 result.

For a positive target dimension strictly below the sphere dimension,

\[
1\le n+k<n
\quad\Longrightarrow\quad
\pi_{n+k}^n=0.
\]

When

\[
n+k=0,
\]

the CLI/Web path returns boundary information: \(S^n\) is path-connected and \(\pi_0(S^n)\) has one path component. This is not normalized as an ordinary group result.

When

\[
n+k<0,
\]

the query is reported as outside the classical unstable homotopy-group domain handled by this project.

Examples:

```powershell
python main.py 10 0
python main.py 1 5
python main.py 7 -5
python main.py 3 -3
python main.py 2 -3
```

## Standard-query coverage through stem 7

Phase 130 connected or specialized existing theorem-backed results so that standard queries now cover the intended project semantics through \(k=7\), including low-dimensional boundary cases.

Representative stable/symbolic families include:

\[
\pi_{n+1}^n=\mathbb Z/2\{\eta_n\},
\]

\[
\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\},
\]

\[
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
\]

\[
\pi_{n+4}^n=0
\qquad (n\ge6),
\]

\[
\pi_{n+5}^n=0
\qquad (n\ge7),
\]

\[
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\},
\]

and

\[
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\}
\qquad (n\ge9).
\]

Concrete low-dimensional branches are preserved and preferred where the literature proof already supplies them.

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
- standard-query specialization for stable families,
- theorem-specific recovery of existing concrete proof nodes,
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

## Phase 130 closure

Phase 130 changed standard-query orchestration, not the underlying Toda mathematics.

The phase:

- recovered low-dimensional results already present in proof ancestry,
- specialized stable families for stems \(1\) through \(6\),
- connected foundational diagonal / below-diagonal / circle semantics,
- admitted negative stem input while distinguishing positive target dimension, \(\pi_0\) boundary information, and negative dimensions,
- connected the existing concrete \(\pi_{16}^9=\mathbb Z/16\{\sigma_9\}\) proof to the standard query,
- preserved existing repository roots and proof provenance,
- corrected stale regression tests whose old CLI contract rejected negative stems.

Final Phase 130 regression:

```text
9308 passed in 577.02s (0:09:37)
```

## Near-term roadmap

Phase 130 is complete.

Phase 131 should begin with a capability and usage-pressure audit. It should not assume that the next step is a general evaluator or a higher stem.

The decision order remains:

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

## Test and backup hygiene

Repository-wide regression should be run as

```powershell
python -m pytest tests -q
```

so only the intended test tree is collected.

Temporary backup directories containing copied `test_*.py` files must not be created inside the repository root because pytest may collect them and produce duplicate-module import mismatches. Backup artifacts should be stored outside the repository, for example under the user's Downloads directory.

## Project principle

```text
actual mathematical or proof-search need
→ smallest missing representation or orchestration
→ preserve existing semantics and provenance
→ add focused regression coverage
→ measure pressure before expanding or optimizing
→ do not pre-implement future phases
```
