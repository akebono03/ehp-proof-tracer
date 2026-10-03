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
- KaTeX rendering for the static Group query quantity \(\pi_{n+k}^{n}\), with input syntax examples kept as plain text,
- Web group-proof display defaulting to Narrative at depth 2, with selectable depth 0, 1, or 2 and Trace / Outline / Narrative modes,
- semantic Narrative rendering for the audited proof-statement inventory, with no rule-name fallback remaining in the Phase 143 completion audit,
- workflow navigation that groups the single-page Web forms by calculation/query, proof/exploration, and applicability/execution.

## Mathematical scope

The project quantity

$$
\pi_{n+k}^n
$$

means the free part plus the 2-primary component represented by this project.

Representative finite-dimensional results include

$$
\pi_5^2=\mathbb Z/2\{\eta_2^3\},
\qquad
\pi_6^3=\mathbb Z/4\{\nu'\},
$$

$$
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\},
$$

$$
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},
\qquad
\pi_{10}^4=\mathbb Z/8\{\nu_4^2\},
$$

$$
\pi_{11}^5=\mathbb Z/2\{\nu_5^2\},
\qquad
\pi_9^2=0.
$$

Toda Proposition 5.15 coverage includes

$$
\pi_{12}^5=\mathbb Z/2\{\sigma'''\},
\qquad
\pi_{13}^6=\mathbb Z/4\{\sigma''\},
\qquad
\pi_{14}^7=\mathbb Z/8\{\sigma'\},
$$

$$
\pi_{15}^8=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\},
$$

$$
\pi_{16}^9=
\mathbb Z/16\{\sigma_9\},
$$

and

$$
\pi_{n+7}^n=
\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
$$

For concrete indexed \(\sigma_n\) with \(n\ge 10\), the existing symbolic Proposition 5.15 proof is specialized without creating a new independent theorem root. The boundary case \(n=9\) reuses the existing concrete \(\pi_{16}^9\) proof from Proposition 5.15 ancestry.

The consolidated stable 2-primary stem data is

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

$$
k=0
\quad\Longrightarrow\quad
\pi_n^n\cong\mathbb Z\{\iota_n\}.
$$

For the circle,

$$
n=1,\quad k\ge1
\quad\Longrightarrow\quad
\pi_{1+k}^1=0,
$$

using the existing symbolic Phase 56 result.

For a positive target dimension strictly below the sphere dimension,

$$
1\le n+k<n
\quad\Longrightarrow\quad
\pi_{n+k}^n=0.
$$

When

$$
n+k=0,
$$

the CLI/Web path returns boundary information: \(S^n\) is path-connected and \(\pi_0(S^n)\) has one path component. This is not normalized as an ordinary group result.

When

$$
n+k<0,
$$

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

$$
\pi_{n+1}^n=\mathbb Z/2\{\eta_n\},
$$

$$
\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\},
$$

$$
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
$$

$$
\pi_{n+4}^n=0
\qquad (n\ge6),
$$

$$
\pi_{n+5}^n=0
\qquad (n\ge7),
$$

$$
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\},
$$

and

$$
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\}
\qquad (n\ge9).
$$

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
- semantic mathematical rendering for the audited Narrative statement inventory, while preserving proof provenance and avoiding invented mathematical prose.

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

Narrative uses deterministic presentation rules over the same proof graph. Phase 143 moved the audited proof-statement inventory from internal rule-name fallback toward first-class semantic statement rendering. The completion audit found no remaining rule-name fallback in the audited current-entrypoint Narrative output.

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

The default mode is `narrative` and the default depth is `2`. Trace and Outline remain available through explicit selection.

Representative behavior:

$$
\pi_{16}^{9}\cong\mathbb Z/16\{\sigma_9\}
$$

replays from the existing Toda Proposition 5.15 `ProofStep`.

The zero group

$$
\pi_9^2=0
$$

can also be replayed because replay begins from the group result rather than from a generator.

The foundational connectivity result

$$
\pi_{10}^{11}=0
$$

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

$$
H(\nu')=\eta_5,
$$

$$
\Delta(\iota_9)=\pm(2\nu_4-E\nu'),
$$

$$
E(\eta_2\nu')=0,
$$

$$
E(\nu_5)=\nu_6,
$$

$$
E(\sigma_{11})=\sigma_{12},
$$

$$
E(\nu_5\eta_8)=0,
$$

and

$$
E\nu' \in \pi_7^4.
$$

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

$$
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

The final Narrative now presents the argument in mathematical order:

$$
2\eta_3=0
$$

is checked before defining the Toda bracket

$$
\{\eta_3,2\iota_4,\eta_4\}_1,
$$

and \(\nu'\) is explicitly chosen as an element of that bracket. Toda Lemma 5.2 then gives

$$
\nu'\in\pi_6^3,
\qquad
H(\nu')=\eta_5,
\qquad
2\nu'=\eta_3^3.
$$

Toda Proposition 2.2 is used explicitly in

$$
H(\nu'\eta_6)
=
H(\nu'\circ E\eta_5)
=
H(\nu')\circ E\eta_5
=
\eta_5^2.
$$

The EHP exact sequence is shown as

$$
\pi_7^3
\xrightarrow{H}
\pi_7^5
\xrightarrow{\Delta}
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5,
$$

and the final group-structure step uses the short exact sequence

$$
0
\longrightarrow
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5
\longrightarrow
0.
$$

The final Phase 136-2 repository-wide regression is:

```text
9517 passed in 575.31s (0:09:35)
```

## Phase 137 Web presentation cleanup

Phase 137 keeps mathematical semantics, proof provenance, query parsing, and execution behavior unchanged. It cleans up presentation-only issues found in the Phase 136-2 Web audit.

The static Group query description now sends

$$
\pi_{n+k}^{n}
$$

through the existing `data-latex` / KaTeX path instead of showing the literal text `pi_(n+k)^n`.

The phase also restores the intended em-dash separators in Web provenance and compact applicability summaries, removing the mojibake marker `窶・` from `templates/index.html`.

Operation and generator examples such as `H(nu_prime)`, `E(nu_5)`, and `sigma_11` remain plain input syntax and are deliberately not converted to TeX.

Phase 137 focused regression so far:

```text
Phase 137-2: 3 passed in 6.96s
Phase 137-3 Web related regression: 56 passed in 20.23s
```

Phase 137-4 manual Web verification confirmed the KaTeX display, plain-text input syntax, restored separators, and the absence of visible `窶・` mojibake.

Phase 137-5 also standardizes display-math delimiters in the main project documentation to GitHub-friendly `$$ ... $$` blocks. This is documentation presentation only; mathematical content is unchanged.

The repository-wide Phase 137 final regression is intentionally left for the Phase-final step after documentation is updated.

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

Historical canonical repository-wide Phase 144 run:

```text
10298 collected
10273 passed, 25 failed in 2321.20s (0:38:41)
```

The 25 failures were historical R5-39 through R5-43 snapshot assertions. After
focused historical-test maintenance, the affected regression passed:

```text
66 passed in 1308.82s (0:21:48)
```

The repository-wide suite was not rerun after that maintenance.

## Project principle

```text
actual mathematical or proof-search need
→ smallest missing representation or orchestration
→ preserve existing semantics and provenance
→ add focused regression coverage
→ measure pressure before expanding or optimizing
→ do not pre-implement future phases
```

## Phase 143 closure

Phase 143 generalized Narrative presentation away from internal rule-name fallback and toward semantic mathematical rendering backed by stored proof statements.

The phase did not add new Toda theorems, change the proof graph, or introduce a second proof engine. Instead, it audited the statement structures already carried by proof steps and added or refined semantic rendering for those structures.

Representative semantic output now includes mathematical content such as:

$$
\Delta(\iota_{13})
\in
\{\nu_6,\eta_9,2\iota_{10}\}
\pmod{2\pi_{11}^{6}},
$$

$$
\ker\left(
\Delta:\pi_8^5\to\pi_6^2
\right)
=
\mathbb Z/2\{4\nu_5\},
$$

and the transported decomposition

$$
\pi_{15}^{8}
\cong
\mathbb Z/8\{E\sigma'\}
\oplus
\mathbb Z\{\sigma_8\}.
$$

The Narrative layer preserves the distinction between a transported decomposition and the final standard-order group statement

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}.
$$

It also preserves direct-premise relocation behavior such as the single, dependency-ordered occurrence of

$$
2\nu_5=E^2\nu'.
$$

Phase 143 completion checks:

```text
Focused regression:
33 passed in 20.96s

Current-entrypoint completion audit:
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0

Repository-wide final regression:
9980 passed in 807.31s (0:13:27)
```

The Phase 143 boundary is presentation semantics only:

```text
semantic Narrative rendering
!= new theorem fact
!= new proof edge
!= proof search
!= operation evaluation
!= theorem ranking
```

## Phase 144 closure

Phase 144 audited how semantic Narrative presentation scales from the representative
$\pi_6^3$ proof to other group-result proofs. It did not add new Toda theorem facts
or a second proof engine.

The phase established a generic contribution-aware Narrative route over the existing
`ProofStep` graph, semantic sidecar, Narrative blocks, arguments, and proof chains.
The audit also established a complete replay API for Narrative use when an explicit
positive depth requires the semantic dependency closure. Explicit depth 0 remains a
bounded replay and is not silently expanded to the complete replay.

The Phase 144-6 R25-30-R3 boundary audit is the technical investigation endpoint
for the phase. Across the six representative groups, the current ownership /
argument-boundary classification was consistent with the existing child-argument
model. The audit identified a separate remaining pressure: some owned group-structure
or definition entries can recursively re-expand a large proof subtree. This is a
result-reuse problem, not an ownership-boundary leak, and it is deliberately deferred
until a concrete proof requires a general repair.

Representative current boundary inventory:

```text
pi_6^3:  selected=6   participating=6/6   detached=0/0    transport=1
pi_8^5:  selected=10  participating=7/7   detached=3/3    transport=1
pi_10^4: selected=22  participating=0/0   detached=22/0   transport=2
pi_12^5: selected=46  participating=2/2   detached=44/0   transport=4
pi_15^8: selected=54  participating=10/10 detached=44/0   transport=4
pi_16^9: selected=54  participating=10/10 detached=44/0   transport=4

TOTAL selected=192
TOTAL participating=35
TOTAL detached=157
TOTAL detached_insertable=3
TOTAL missing=0
```

The final canonical repository-wide run after the Phase 144 regression repairs
collected 10,298 tests:

```text
10273 passed, 25 failed in 2321.20s (0:38:41)
```

All 25 failures were confined to historical R5-39 through R5-43 completion /
fixed-count snapshot assertions whose pre-R25 assumptions no longer represented
the current ownership/boundary semantics. They were maintained without changing
the production renderer and without replacing the old fixed totals with new fixed
totals. The affected focused regression then passed:

```text
66 passed in 1308.82s (0:21:48)
```

The whole repository suite was intentionally not rerun after that historical-test
maintenance. Therefore the closure record preserves both pieces of evidence rather
than reporting an unobserved all-green repository-wide run.

Phase 145 is intentionally narrow: change the default group-proof presentation to
Narrative with depth 2. It must not implement result reuse or other new
generalization machinery.

From Phase 146 onward, development follows one concrete proof pressure at a time:

```text
one Phase
→ one concrete issue
→ the minimum general rule needed for that issue
→ focused regression
→ preserve existing proofs
```

A future phase is complete when its one target issue is solved by a general rule
rather than target-specific special handling, without breaking existing proofs.

## Phase 145 closure

Phase 145 intentionally kept its functional scope narrow: it changed the default
group-proof presentation to Narrative at depth 2 without changing proof semantics,
stored provenance, theorem facts, or explicit user selections.

The default CLI behavior is now equivalent to:

```powershell
python main.py group-proof n k --mode narrative --depth 2
```

Explicit selections remain available:

```powershell
python main.py group-proof 9 7 --mode trace --depth 0
python main.py group-proof 9 7 --mode outline --depth 1
python main.py group-proof 9 7 --mode narrative --depth 2
```

The Web group-proof form likewise defaults to Narrative and depth 2 while preserving
the existing Trace / Outline / Narrative and depth 0 / 1 / 2 choices.

Phase 145 also completed repository cleanup by moving historical Phase artifacts under
`archive/phases/`. The cleanup exposed mixed canonical-test import conventions:
some tests import `tests.test_*`, while older tests import bare `test_*` modules.
The final compatibility repair preserves both conventions with an explicit
`tests` package marker and a test-only import compatibility layer. Production code
and existing canonical test bodies were not changed for that repair.

Phase 145 focused regression:

```text
46 passed in 15.62s
```

Canonical collection after the compatibility repair:

```text
10303 tests collected
```

Final repository-wide regression:

```text
10303 passed in 2375.31s (0:39:35)
```

Phase 145 does not implement result reuse, new Narrative generalization rules,
new theorem facts, or new proof search. From Phase 146 onward, one concrete
generalization issue is handled per Phase with the minimum general rule needed for
that issue.

## Phase 148 closure — recursive exactness evidence exposure

Phase 148 completed RC2, `Recursive exactness evidence exposure`, without adding new Toda theorem facts or changing the stored proof graph.

The Narrative pipeline now distinguishes exactness method evidence as:

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

For an `OWNED_PRIMARY` exactness component, raw exactness-window prose is suppressed while the owned higher-level method contribution, including an appropriate derived short exact sequence, may remain visible.

For `UNOWNED_RECURSIVE` evidence, recursive exactness body contributions are not automatically expanded into the Narrative. The proof provenance remains available; the suppression is presentation-only.

`AMBIGUOUS_RELEVANT` remains conservative and preserves the existing display behavior rather than guessing an owner.

The Web Narrative path now respects the selected bounded replay depth instead of replacing it with complete replay. Semantic closure remains presentation-side and adds only the narrowly required existing provenance for Narrative rendering. At depth 0, semantic closure is the identity. For positive depth, the Phase 148 calculation closure is limited to the equality-premise chain needed beneath an existing order relation, while the previously registered definition closure remains available.

The Phase 148 boundary is therefore:

```text
proof provenance
→ RC1 argument-method ownership
→ RC2 exactness evidence exposure
→ Narrative body
```

It does not include contribution ordering. In particular, ordering pressure such as a final group conclusion appearing before its explanatory short exact sequence is deferred to Phase 149 / RC3.

Final verification evidence:

```text
focused RC2 regression:
92 passed in 36.15s

canonical repository regression:
10398 passed, 3 failed in 1316.54s (0:21:56)

failure classification:
the three failures were confined to
tests/test_phase144_6_pi6_generic_production_route.py
and were stale expectations introduced by earlier Phase 148 repair work.

restored Phase 144-6 contract:
4 passed in 1.71s
```

The repository-wide suite was not rerun after restoring those three stale expectations, in accordance with the Phase-final test policy. The final record therefore preserves the measured whole-suite result and the focused restoration result separately rather than inventing an inferred all-pass count.

---

<!-- PHASE149_RC3_CLOSURE -->
## Phase 149 closure — Narrative contribution ordering

Phase 149 completed RC3, Narrative contribution ordering, without adding new Toda theorem facts or changing the stored proof graph.

Phase 147 established which Narrative Argument owns a primary exactness method. Phase 148 established which exactness evidence is exposed. Phase 149 adds the corresponding placement rule:

```text
RC1: Argument -> method ownership
RC2: method -> visible evidence
RC3: visible evidence -> Narrative placement
```

For visible `OWNED_PRIMARY` exactness evidence, the Narrative body now collects the existing RC2 display contributions and places them before the owning Argument conclusion. This placement is independent of the global Narrative block order.

For the representative proof

$$
\\pi_6^3=\\mathbb{Z}/4\\{\\nu'\\},
$$

the group-structure explanation now presents the EHP exactness method and the derived short exact sequence

$$
0
\\longrightarrow
\\pi_5^2
\\xrightarrow{E}
\\pi_6^3
\\xrightarrow{H}
\\pi_6^5
\\longrightarrow
0
$$

before the final group-structure conclusion.

The RC3-4 cross-group audit covered

$$
\\pi_6^3,\\quad
\\pi_8^5,\\quad
\\pi_{10}^4,\\quad
\\pi_{12}^5,\\quad
\\pi_{15}^8,\\quad
\\pi_{16}^9.
$$

Audit result:

```text
pi_6^3:  owned_primary_visible=1, ordering_ok=True
pi_8^5:  owned_primary_visible=1, ordering_ok=True
pi_10^4: owned_primary_visible=0, ordering_ok=True
pi_12^5: owned_primary_visible=0, ordering_ok=True
pi_15^8: owned_primary_visible=0, ordering_ok=True
pi_16^9: owned_primary_visible=0, ordering_ok=True

failures=[]
AUDIT_RESULT=PASS
```

Focused RC3-4 / RC3-3 / RC2 regression:

```text
57 passed in 10.85s
```

Final repository-wide regression:

```text
﻿10416 passed in 1315.93s (0:21:55)
```

Phase 149 changes presentation ordering only:

```text
Narrative contribution placement
!= ProofStep ordering
!= proof edge mutation
!= theorem inference
!= exactness exposure classification
```

The observed placement of the derived calculation

$$
2\\nu'=\\eta_3^3
$$

inside the order Argument remains a separate calculation/derivation-ordering pressure. It is not treated as an RC3 exactness-placement failure and is not changed in Phase 149.

The next planned pressure is Phase 150 / RC4, generic provenance / reason prose.
<!-- PHASE150_CLOSURE -->
## Phase 150 closure — generic provenance / reason prose

Phase 150 completed RC4, generic provenance / reason prose, without adding new
Toda theorem facts or changing the stored proof graph.

The phase introduced typed Narrative reason information derived from existing proof
provenance and connected that information to generic Narrative prose. The work also
confirmed an architectural limitation in the current transition strategy: multiple
renderer routes still coexist, and route-by-route migration itself can create
group-dependent presentation differences.

Phase 150 therefore closes without continuing group-by-group renderer migration.
The next phase starts from a whole-population generic baseline instead.

The six representative groups used throughout the RC4 audit were

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9.
$$

The final visible-reason contract is instance-based. If several typed reasons render
to the same generic sentence, the Narrative may contain that sentence several times;
the number of occurrences must match the number of typed reason instances producing
that sentence.

Phase 150 final repository-wide regression:

```text
10478 passed in 2505.44s (0:41:45)
pytest exit code: 0
wall-clock elapsed: 00:41:56.919
```

This run is the Phase 150 closure baseline. Future development does not treat the
complete historical suite as a mandatory end-of-every-phase operation. Focused tests
and a maintained canonical regression set are the normal development checks; the
complete historical suite is reserved for major integration or release milestones.

Phase 151 begins with an all-group generic baseline. It will force the audited group
population through the same generic Narrative route for observation and
classification while leaving the public renderer selection unchanged.

---

<!-- PHASE153_CLOSURE -->
## Phase 153 closure — Reference selection and granularity

Phase 153 refined Narrative Reference selection, granularity, reuse, and display
boundaries without adding new Toda theorem facts or changing the stored proof graph.

The phase established general Reference rules across legacy, generic, and specialized
Narrative routes:

- semantic classification for the audited scalar-order statement,
- recovery of existing concrete proof scope before stable specialization where a
  concrete proof already exists,
- proof-ancestry-based Reference selection for the audited low-dimensional
  \(n=2\) groups,
- boundary-oriented Reference granularity,
- suppression of irrelevant aggregate ancestry from the visible proof body,
- normalization of Reference-use prose,
- reuse of an already displayed Reference as a proof boundary instead of recursively
  re-expanding the same derivation,
- filtering of unused References,
- structural Reference attribution for generic routes that do not use explicit
  `[Rk]` body markers,
- exclusion of the current root theorem from the external Reference section across
  all renderer routes,
- locator-based literature-reference identity when labels differ but the cited
  locator is the same.

The final depth-2 closure audit covered the project population

$$
n=2,\ldots,15,
\qquad
k=0,\ldots,7,
$$

for a total of 112 groups.

Measured closure evidence:

```text
focused Phase 153 regression:
30 passed in 7.97s

112-group depth-2 closure audit:
scanned groups: 112
render errors: 0
groups with Reference section: 93
marker-bearing groups: 90
generic/reference-only groups: 3
Reference headers: 147
body Reference markers: 146
maximum References in one group: 6
groups at maximum: pi_6^3
violations: 0

AUDIT_RESULT=PASS
```

The complete historical test suite was not used as the Phase 153 completion gate.
A canonical `tests/` run collected 10,554 tests and exposed multiple stale
presentation expectations from earlier phases. One stale Phase 132 Narrative
expectation was repaired and its focused verification passed, while broader historical
test consolidation was deliberately deferred.

Accordingly, Phase 153 closes on its focused regression and whole-population Reference
invariant audit. It does not claim an unobserved repository-wide all-pass result.

Phase 154 has completed its proof-prose generation refinement and 112-group closure audit. The repository-wide final full regression remains the Phase-final step. Test-suite consolidation remains a
separate deferred maintenance task.

## Phase 154 proof-prose generation refinement

Phase 154 refined the public Narrative prose generated from existing proof provenance. It did not add new Toda theorem facts, proof edges, proof search, or a second proof engine.

The phase addressed the following presentation defects through shared rules rather than group-specific fixes:

- internal inference-rule / type-name leakage in public prose,
- English semantic statements such as `is injective` and `is exact`,
- repeated semantic reason prose,
- Reference-to-proof-body linkage,
- malformed sentence composition around reused References and semantic facts,
- Narrative transition wording,
- ASCII punctuation normalization for Japanese proof prose.

The final Narrative punctuation policy is:

```text
prose comma  = ", "
prose period = "."
```

This policy applies to prose only. TeX / mathematical punctuation and literature-title punctuation such as `Proposition 5.8.` are preserved.

The punctuation closure audit covered all standard depth-2 public Narratives

$$
n=2,\ldots,15,
\qquad
k=0,\ldots,7,
$$

for a total of 112 groups:

```text
scanned groups: 112
rendered groups: 112
exceptions: 0
japanese comma violations: 0
japanese period violations: 0
affected groups: 0
ascii comma prose lines: 484
groups with ascii comma prose: 112
ascii period prose endings: 587
groups with ascii period prose: 112
```

The Phase 154 closure audit then rechecked the full proof-prose contract:

```text
Phase 154 focused regression:
44 passed

ordering / reason regression boundary:
57 passed

112-group closure audit:
scanned groups: 112
rendered groups: 112
exceptions: 0
violations: 0
affected groups: 0

transition_repetition: 0
semantic_duplication: 0
internal_fallback_leakage: 0
english_prose: 0
reference_linkage: 0
ordering: 0
punctuation: 0
```

Reference coverage at closure was:

```text
groups with Reference section: 93
groups with body Reference markers: 89
```

Two apparent ordering findings for the dedicated $\pi_8^5$ and $\pi_{15}^8$ routes were audit false positives caused by substring matching between `## 証明` and `## 証明対象`. Exact heading-line counting and ordering confirmed that both routes have

```text
## 証明対象
→ ## 使用する結果
→ ## 証明
```

in the intended order.

Some Phase 149 / Phase 150 historical presentation tests were updated to the current Phase 154 contract:

- numbered derivation punctuation now expects `より, `,
- duplicate `FINAL_RESULT_DERIVATION` prose is expected only once in the public Narrative,
- reason-vocabulary punctuation now uses ASCII commas.

These were test-contract maintenance changes; production proof semantics were not changed.

Phase 154 documentation closure does not claim a repository-wide all-pass result. The final full regression remains the Phase-final step.

<!-- PHASE155_TEST_CONSOLIDATION_CLOSURE_START -->
## Phase 155 closure — Test Suite Consolidation

Phase 155 reorganized test evidence without changing Toda mathematics, proof search, stored provenance, or public proof APIs.

The final collection is:

```text
10384 tests total
10382 routine tests
2 audit-only tests
```

Routine regression is executed in file-based shards with checkpoint/resume semantics. Passed shards are not rerun after unrelated repairs. The working target is about five minutes per shard; ten minutes is a split/review boundary rather than a normal feedback unit.

The final two audit-only tests are explicit Phase-closure integration audits:

```text
Phase153 all-group public Reference structural audit
Phase97 representative cross-layer provenance audit
```

Three earlier audit-only candidates were removed from the Phase155 closure boundary. Two Phase144 audits fixed historical renderer implementation shape. The Phase153 exact Reference/body duplicate audit measured 117 duplicate candidates; that observation is retained as Phase156 input because Reference statement relevance and minimal display belong to Phase156.

Final Phase155 evidence:

```text
routine sharded regression: PASS
final audit-only explicit closure: 2/2 PASS
monolithic repository-wide pytest: not run
```
<!-- PHASE155_TEST_CONSOLIDATION_CLOSURE_END -->
