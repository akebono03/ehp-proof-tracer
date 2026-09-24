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
- generator-first known-group proof replay,
- group-result-first proof replay,
- deterministic Trace / Outline / Narrative proof presentation,
- human-readable Narrative labels for representative aggregate proof statements,
- deterministic shared-dependency Narrative reuse with natural Japanese references,
- operation-fact lookup,
- operation-query proof replay,
- theorem-specific indexed \(\sigma_n\) specialization,
- theorem-specific standard-query recovery from existing proof ancestry,
- deliberately narrow existing-proof handoffs for \(E(\nu_5)=\nu_6\), \(E(\sigma_{11})=\sigma_{12}\), \(E(\nu_5\eta_8)=0\), and \(E\nu' \in \pi_7^4\),
- a Flask Web UI for group queries, group-result proof replay, operation queries, operation proof replay, generator proof replay, direct generator exploration, recursive generator proof-scope exploration, applicability exploration, and qualified generator execution,
- explicit candidate selection when an execution request is ambiguous,
- browser-side KaTeX rendering of existing LaTeX output,
- Web group-proof display with selectable depth 0, 1, or 2 and Trace / Outline / Narrative modes,
- safe rule-name or type-name fallback when no explicit mathematical or presentation label is available,
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

Phase 130 connected or specialized existing theorem-backed results so that standard queries cover the intended project semantics through \(k=7\), including low-dimensional boundary cases.

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
- generator-first known-group proof replay,
- group-result-first proof replay rooted at `TodaGroupResult.proof_step`,
- preservation of `TodaGroupResult.source_entry` theorem / phase / repository-key provenance,
- zero-group proof replay without requiring a generator,
- connectivity-zero proof replay when a repository-backed `TodaGroupResult` exists,
- a thin `TodaGroupProofPresentation` over group-result replay,
- deterministic Outline rendering from actual premise edges,
- deterministic Narrative rendering from the same proof graph,
- shared-dependency deduplication in Narrative presentation without deleting graph edges,
- explicit human-readable Narrative labels for representative aggregate statements,
- generator-centered repository occurrence exploration,
- recursive generator proof-scope exploration,
- applicable theorem / lemma discovery grouped by source statement and rule family,
- existing operation-fact lookup,
- operation-query result deduplication without losing raw provenance,
- operation-query proof replay rooted at the selected fact's actual `ProofStep`,
- theorem-specific `E(nu_5)`, `E(sigma_11)`, `E(nu_5 o eta_8)`, and `E(nu_prime)` handoffs that preserve existing proof provenance,
- user-facing qualified execution with explicit `NONE`, `AMBIGUOUS`, and `EXECUTED` states,
- user-selected replay depth,
- safe mathematical rendering with explicit fallback for unsupported aggregate statements.

General unbounded proof search, theorem ranking, producer ranking, proof-cost optimization, arbitrary operation-query inference fallback, general membership evaluation, and general \(E/H/\Delta\) evaluation are intentionally not implemented.

## Group-result proof replay and presentation

Phase 131 connected a group query result directly to its existing proof provenance.

The core path is

```text
TodaGroupResult
→ source_entry / proof_step
→ existing recursive proof provenance
→ depth-limited replay
```

Phase 132 added presentation on top of that replay:

```text
TodaGroupResultProofReplayResult
→ TodaGroupProofPresentation
→ Trace / Outline / Narrative
→ CLI / Web
```

`TodaGroupProofPresentation` does not perform a new proof search. Its nodes are the replay-selected `ProofStep` values and its edges are existing provenance edges filtered to those selected nodes.

Trace remains the audit-oriented ground truth.

Outline follows actual `ProofStep.premises` ancestry and `premise_index`; it does not infer parent-child relations from flat replay depth.

Narrative uses fixed deterministic templates over the same graph. Unsupported statements use safe existing renderers or rule/type fallbacks instead of inventing mathematical prose.

Phase 133 refined this presentation layer without changing proof semantics. Representative aggregate statement types now receive explicit human-readable labels before the renderer falls back to rule or type names. This keeps proof ancestry deterministic while reducing internal implementation vocabulary in ordinary Narrative output.

When one `ProofStep` is used by multiple parents, Narrative expands that shared dependency subtree once and later refers to it as already established. Phase 133 also refined the connective wording so nested reuse is not redundantly repeated.

This remains display-only behavior:

```text
narrative wording
!= new proof fact
!= proof graph deletion
!= provenance deletion
```

CLI examples:

```powershell
python main.py group-proof 9 7
python main.py group-proof 9 7 --depth 2
python main.py group-proof 9 7 --mode trace
python main.py group-proof 9 7 --mode outline
python main.py group-proof 9 7 --mode narrative
python main.py group-proof 9 7 --depth 2 --mode narrative
```

The default mode is `trace`, preserving Phase 131 behavior.

Representative behavior:

\[
\pi_{16}^{9}\cong\mathbb Z/16\{\sigma_9\}
\]

replays from the existing Toda Proposition 5.15 `ProofStep`.

The zero group

\[
\pi_9^2=0
\]

can also be replayed because replay begins from the group result rather than from a generator.

The foundational connectivity result

\[
\pi_{10}^{11}=0
\]

is also replayable because Phase 130 represents it as a repository-backed `TodaGroupResult` with theorem metadata `Sphere connectivity`, Phase 130.

By contrast, \(\pi_0\) boundary information and negative-dimensional out-of-domain information are not ordinary `TodaGroupResult` values and do not expose a proof-replay action.

## Web UI

The Web UI is intentionally a thin presentation layer over existing calculation, operation-query, proof-replay, exploration, applicability, and qualified-execution infrastructure.

It does not implement a second mathematical engine.

Current Web files include

```text
web_app.py
web_group_query.py
web_group_proof.py
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

For a repository-backed group result, the Web UI exposes `Show proof` directly below the result.

Proof depth can be selected as 0, 1, or 2.

Proof view can be selected as:

```text
Trace
Outline
Narrative
```

Trace uses the existing structured replay view.

Outline and Narrative reuse the group-proof renderers. The Web adapter separates mathematical fragments so existing `data-latex` / KaTeX rendering remains available rather than introducing a separate mathematical renderer.

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

## Phase 132 closure

Phase 132 changed proof presentation, not the underlying Toda mathematics.

The phase:

- audited the existing narrative renderer and group-result replay path,
- established that actual `ProofStep.premises` edges are the source of proof structure,
- added `TodaGroupProofPresentation` as a thin common presentation core,
- added deterministic Outline rendering,
- added deterministic Narrative rendering,
- kept unsupported mathematical statements on safe LaTeX / rule-name / type-name fallback paths,
- preserved source theorem, phase, repository key, `ProofStep` identity, and replay depth semantics,
- added shared-dependency Narrative deduplication without changing the proof graph,
- connected Trace / Outline / Narrative to CLI `group-proof`,
- kept Trace as the default CLI mode,
- connected Trace / Outline / Narrative to the Web group-proof flow,
- preserved browser-side KaTeX rendering for mathematical fragments,
- preserved Phase 131 group-result replay and all existing proof-search semantics.

Final Phase 132 regression:

```text
9392 passed in 587.98s (0:09:47)
```

## Phase 133 closure

Phase 133 selected Narrative readability as the concrete post-Phase-132 workflow pressure and refined presentation only.

The phase:

- audited representative group proofs at depth 1 and 2,
- kept Trace, Outline, proof graph, repository, theorem roots, and replay semantics unchanged,
- changed shared-dependency wording from internal/repetitive phrasing to deterministic natural reuse such as `すでに得た...を用いる`,
- used singular `このことから` and plural `これらから` according to the actual premise count,
- added explicit human-readable labels for representative low-dimensional, \(\nu\)-family, Proposition 5.11, Proposition 5.15, and \(\sigma\)-family aggregate statements,
- removed representative internal rule names such as `finite-dimensional integration`, `isomorphism semantics`, `bridge`, and `branch` from the final audited Narrative output,
- kept safe rule/type fallback available for statement types that do not have an explicit label,
- verified the representative groups
  \(\pi_6^3\),
  \(\pi_8^5\),
  \(\pi_{10}^4\),
  \(\pi_{12}^5\), and
  \(\pi_{16}^9\)
  at depth 1 and 2.

Final Phase 133 regression:

```text
9403 passed in 605.52s (0:10:05)
```

## Phase 134–136 presentation refinement

Phase 134 extended Narrative from readable labels to theorem-specific mathematical proof prose for representative groups and extracted only presentation-safe common helpers.

Phase 135 audited the Web Narrative path and preserved browser-side KaTeX for both display and inline mathematical fragments. Inline Narrative math uses inline KaTeX mode while display blocks use display mode.

Phase 136 refined the representative proof

\[
\pi_6^3=\mathbb Z/4\{\nu'\}.
\]

The final Narrative now presents the argument in mathematical order:

\[
2\eta_3=0
\]

is checked before defining the Toda bracket

\[
\{\eta_3,2\iota_4,\eta_4\}_1,
\]

and \(\nu'\) is explicitly chosen as an element of that bracket. Toda Lemma 5.2 then gives

\[
\nu'\in\pi_6^3,
\qquad
H(\nu')=\eta_5,
\qquad
2\nu'=\eta_3^3.
\]

Toda Proposition 2.2 is used explicitly in

\[
H(\nu'\eta_6)
=
H(\nu'\circ E\eta_5)
=
H(\nu')\circ E\eta_5
=
\eta_5^2.
\]

The EHP exact sequence is shown as

\[
\pi_7^3
\xrightarrow{H}
\pi_7^5
\xrightarrow{\Delta}
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5,
\]

and the final group-structure step uses the short exact sequence

\[
0
\longrightarrow
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5
\longrightarrow
0.
\]

The final Phase 136-2 repository-wide regression is:

```text
9517 passed in 575.31s (0:09:35)
```

The next concrete presentation pressure found during the Phase 136-2 closure audit is Web static mathematical text that still bypasses KaTeX. In particular, the Group query description still contains the literal text `pi_(n+k)^n`. This should be handled as a Web presentation cleanup without changing mathematical semantics or the query syntax examples.

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
- free-form LLM proof generation detached from stored `ProofStep` provenance,
- odd-primary full integration,
- an all-primary ordinary sphere-homotopy calculator.

## Test and backup hygiene

Repository-wide regression should be run as

```powershell
python -m pytest tests -q
```

so only the intended test tree is collected.

Temporary backup directories containing copied `test_*.py` files must not be created inside the repository root because pytest may collect them and produce duplicate-module import mismatches. Backup artifacts should be stored outside the repository, for example under the user's Downloads directory.

Latest repository-wide regression:

```text
9517 passed in 575.31s (0:09:35)
```

## Project principle

```text
actual mathematical or proof-search need
→ smallest missing representation or orchestration
→ preserve existing semantics and provenance
→ add focused regression coverage
→ measure pressure before expanding or optimizing
→ do not pre-implement future phases
```
