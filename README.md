# EHP Proof Tracer

EHP Proof Tracer is a Python project for representing, checking, searching, explaining, presenting, exploring, replaying, and safely executing theorem-backed Toda-style homotopy-group calculations.

The project currently focuses on the free part plus the 2-primary Toda groups, EHP exactness, explicit proof provenance, the calculation spine through stable stems \(G_0\) to \(G_7\), theorem-backed repository exploration, recursive proof-ancestry exploration, applicable theorem / lemma discovery, relevance classification, bounded candidate handoff, multi-family qualified production execution, proof-derived known-group identity lookup, indexed \(\sigma_n\) specialization, user-facing known-group proof replay, existing-operation-fact lookup, and operation-query proof replay.

This is not an all-primary calculator for ordinary homotopy groups of spheres.

## Current mathematical coverage

Representative finite-dimensional results include

\[
\pi_5^2=\mathbb Z/2\{\eta_2^3\},
\qquad
\pi_6^3=\mathbb Z/4\{\nu'\},
\]

\[
\pi_7^4=\mathbb Z\{\nu_4\}\oplus\mathbb Z/4\{E\nu'\},
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
\pi_{15}^8
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\},
\]

and

\[
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
\]

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
- explicit-final-rule bounded search,
- end-to-end rule-identity provenance,
- qualified execution across multiple admitted production rule families,
- exact multi-premise production-application recovery,
- proof-derived known-group identity lookup,
- theorem-specific indexed \(\sigma_n\) specialization,
- user-facing known-group proof replay,
- existing operation-fact lookup,
- operation-query result deduplication without losing raw provenance,
- operation-query proof replay rooted at the selected fact's actual `ProofStep`,
- safe mathematical rendering with explicit type-name fallback for unsupported aggregate statements.

General unbounded proof search, theorem ranking, producer ranking, proof-cost optimization, best-proof selection, and semantic automatic target preference are intentionally not implemented.

## Toda group calculation API

The calculation entry point is

```python
build_toda_calculation_result(
  repository,
  query,
)
```

where `query` is a `TodaGroupQuery(n, k)` representing the project quantity

\[
\pi_{n+k}^n,
\]

meaning the free part plus the 2-primary component used by this project.

The production one-shot entry point is

```python
build_standard_toda_report(
  n,
  k,
)
```

and the minimal calculation CLI is

```powershell
python main.py n k
```

Direct theorem-backed results take precedence over aggregate fallback results. Multiple valid results are preserved; the calculation layer does not silently rank or choose one result.

## EHP and exactness provenance

For theorem-backed proofs containing actual EHP ancestry, the project can extract EHP exactness windows, a contiguous EHP sequence, exactness-use provenance, and known group information on EHP terms.

A representative \(\pi_9^5\) proof yields

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

## Standard production repository

The production builder is

```python
build_standard_production_proof_repository()
```

It assembles theorem-backed entries needed by supported production paths without creating new theorem truth.

Concrete indexed \(\sigma_n\) specialization is derived from the existing Proposition 5.15 proof scope rather than registered as a new independent theorem root.

## Generator-centered exploration

Generator-centered exploration supports exact aliases such as

```text
eta_2
nu_5
sigma_8
sigma_11
iota_4
nu_prime
sigma_prime
sigma_double_prime
sigma_triple_prime
```

An unindexed family is not a wildcard.

The standard recursive proof-scope entry point is

```python
explore_standard_repository_generator_proof_scope_input(
  generator_input,
)
```

Representative `nu_prime` results include

\[
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1
\]

and

\[
H(\nu')=\eta_5.
\]

For concrete indexed \(\sigma_n\) with \(n\ge 10\), proof-scope exploration can materialize the theorem-specific Proposition 5.15 specialization

\[
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\}.
\]

The exploration layer finds or specializes already represented proof facts. It does not evaluate \(E\), \(H\), or \(\Delta\), and it does not solve Toda brackets.

## Applicable theorem / lemma discovery

Read-only applicability discovery is available through

```python
explore_standard_repository_generator_applicability_input(
  generator_input,
)
```

and

```powershell
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

Applicability discovery does not execute a rule and does not establish a theorem conclusion.

Relevance categories are

```text
THEOREM_SPECIFIC
MAP_PROPERTY
STRUCTURAL
BRIDGE
GENERIC_RELATION
UNCLASSIFIED
```

## Qualified production execution

The admitted qualified production execution families are

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

The second family derives

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}.
\]

For multi-premise rules, the engine does not search arbitrarily for companion premises. It recovers the unique existing production application under the same root and reuses the exact premise tuple by `ProofStep` identity and original order.

The standard user-facing workflow is

```python
run_standard_repository_generator_user_execution_workflow(
  generator_input,
  candidate_number=None,
  max_depth=2,
  retry_policy=None,
)
```

Candidate numbers are one-based addressing only:

```text
candidate number != theorem ranking
candidate order != mathematical priority
```

## Known-group identity and proof replay

Known-group proof replay is separate from qualified theorem execution.

```text
generator
→ unique known-group identity node
→ existing ProofStep
→ direct provenance replay
→ show-proof
```

```text
show-proof != execute
```

The standard replay API is

```python
build_standard_repository_generator_known_group_proof_replay_input(
  generator_input,
  max_depth=1,
)
```

Examples:

```powershell
python main.py show-proof nu_prime
python main.py show-proof sigma_11
```

For `nu_prime`, the replay begins with

\[
\pi_6^3=\mathbb Z/4\{\nu'\}.
\]

For `sigma_11`, the replay begins with

\[
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\}
\]

and preserves the symbolic Proposition 5.15 provenance.

## Existing operation-fact query

Phase 110 added a read-only operation-query path for already represented proof facts.

Examples:

```powershell
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"
```

The minimal query grammar currently supports:

```text
H(<expression>)
E(<expression>)
Delta(<expression>)
<generator> o <generator>
```

Representative results include

\[
H(\nu')=\eta_5,
\]

\[
H(\nu')=E^2\eta_3,
\]

\[
\Delta(\iota_9)
=
\pm(2\nu_4-E\nu'),
\]

\[
E(\eta_2\nu')=0.
\]

The operation-query layer is intentionally a lookup over existing repository / proof-scope facts:

```text
lookup != inference != evaluation
```

No result means that no matching represented repository fact was found. It does not prove mathematical nonexistence.

## Operation-query deduplication and provenance

Raw proof-scope occurrences remain intact.

User-facing presentation groups equal mathematical statements while preserving all contributing provenance matches.

For example,

```powershell
python main.py query "H(nu_prime)"
```

presents two mathematical facts rather than every repeated proof-scope occurrence:

\[
H(\nu')=\eta_5,
\qquad
H(\nu')=E^2\eta_3.
\]

Presentation order is based on shallowest proof-scope depth and stable source order. This is not theorem ranking.

## Operation-query proof replay

Phase 110 also added proof replay for a selected query fact.

Examples:

```powershell
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "H(nu_prime)" --fact 2
python main.py query-proof "E(eta_2 o nu_prime)"
python main.py query-proof "eta_2 o nu_prime" --fact 4
```

If a query has exactly one presented fact, `--fact` is optional. If multiple facts are available, no fact is selected automatically.

The replay root is the selected fact's own `ProofStep`, not the enclosing repository theorem root.

For

\[
H(\nu')=\eta_5,
\]

the direct replay includes

\[
H(\nu')=E^2\eta_3,
\qquad
E^2\eta_3=\eta_5.
\]

The default operation-query replay depth is one direct premise level.

Known special statement types are rendered mathematically, for example

\[
\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1,
\]

\[
E^2\nu'\in2\iota_5\circ\pi_8^5,
\]

and

\[
\Delta:\pi_8^5\to\pi_6^2
\quad\text{is surjective}.
\]

Unsupported aggregate statements use a safe type-name fallback instead of leaking a Python dataclass representation.

## Command-line interface

Current commands are

```powershell
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
python main.py show-proof nu_prime
python main.py show-proof sigma_11
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "E(eta_2 o nu_prime)"
```

The CLI script boundary configures stdout and stderr as UTF-8 so that mathematical Unicode is safe on Windows systems whose default console encoding is CP932.

## Phase 110 closure

Phase 110 closed the first user-facing existing-operation-fact lookup and proof-replay path.

Major outcomes:

```text
operation query input
→ parsed query specification
→ existing repository / proof-scope lookup
→ raw occurrence preservation
→ mathematical-statement deduplication
→ prioritized presentation
→ query CLI
```

```text
selected query fact
→ primary provenance
→ fact's own ProofStep
→ bounded direct proof replay
→ safe mathematical statement rendering
→ query-proof CLI
```

The phase deliberately did not introduce a general composition evaluator or a general \(E/H/\Delta\) evaluator.

Final repository-wide regression:

```text
9055 passed in 455.09s (0:07:35)
```

Final whitespace check:

```text
git diff --check
clean
```

## Current boundaries

The following remain intentionally deferred:

- target-only unknown-right-hand-side proof search,
- theorem ranking and proof-cost optimization,
- semantic automatic target preference,
- producer ranking,
- general unbounded backtracking,
- persistent proof cache,
- repository snapshot/versioning,
- stale-search-report detection,
- free-form natural-language element search,
- wildcard family search,
- arbitrary nested operation-query grammar,
- Unicode-composition and LaTeX input parsing,
- general composition evaluation,
- general Toda-bracket solving,
- bracket-value and coset / indeterminacy computation,
- general \(E/H/\Delta\) evaluation,
- recursive theorem solving beyond already represented proof ancestry,
- automatic enumeration of unstated mathematical consequences,
- execution qualification across all production rule families,
- third and later qualified families without demonstrated production pressure,
- unrestricted symbolic AST substitution,
- rich recursive proof visualization,
- Web UI,
- odd-primary full integration,
- an all-primary ordinary sphere-homotopy calculator.

## Current project state

```text
calculation
→ theorem-backed result
→ provenance
→ report

generator
→ proof-scope exploration
→ applicability discovery
→ relevance-classified candidates

generator
→ known-group identity
→ direct proof replay
→ show-proof

generator
→ executable-target resolution
→ ambiguity-safe candidate selection
→ qualified execution
→ final ProofStep
→ Result + Proof
→ execute

operation query
→ existing proof fact lookup
→ deduplicated mathematical facts
→ preserved provenance
→ query

selected operation fact
→ primary provenance
→ direct proof replay
→ safe mathematical rendering
→ query-proof
```

Phase 100 closed the production calculation path.

Phase 101 closed the production top-level generator-exploration path.

Phase 102 closed recursive proof-scope exploration for already represented Toda memberships and known map relations.

Phase 103 closed read-only applicable theorem / lemma discovery and the first production relevance-classification pass.

Phase 104 closed safe applicability-candidate consumption through bounded search and actual execution.

Phase 105 closed the first explicit standard-production applicability-to-execution path.

Phase 106 removed the dominant applicability-materialization bottleneck while preserving semantics and provenance.

Phase 107 closed the first multi-family qualified-production execution path.

Phase 108 closed the first user-facing execution path.

Phase 109 closed known-group identity fallback, indexed \(\sigma_n\) specialization, known-group proof replay, and the `show-proof` / `execute` boundary.

Phase 110 closed existing operation-fact query, deduplicated presentation, provenance-preserving query output, selected-fact proof replay, and safe replay statement rendering.

## Project principle

```text
actual mathematical or proof-search need
→ smallest missing representation or orchestration
→ preserve existing semantics and provenance
→ add focused regression coverage
→ measure pressure before expanding or optimizing
→ do not pre-implement future phases
```
