# EHP Proof Tracer

EHP Proof Tracer is a Python project for representing, checking, searching, explaining, presenting, exploring, and safely executing theorem-backed Toda-style homotopy-group calculations.

The project currently focuses on the 2-primary Toda groups, EHP exactness, explicit proof provenance, the calculation spine through stable stems $G_0$ to $G_7$, theorem-backed repository exploration, recursive proof-ancestry exploration, applicable theorem / lemma discovery, relevance classification, bounded candidate handoff, multi-family qualified production execution, exact multi-premise production-application recovery, and applicability-performance stabilization.

## Current mathematical coverage

Representative finite-dimensional results include

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

This is not an all-primary calculator for ordinary homotopy groups of spheres.

## Proof infrastructure

The proof infrastructure supports:

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
- recursive proof ancestry,
- repository-nonmutating exploration and execution planning,
- explicit-final-rule bounded search,
- execution of a prebuilt bounded-search report without rebuilding the search,
- end-to-end rule-identity provenance from applicability candidate to derived `ProofStep`,
- qualified execution across more than one production rule family,
- exact recovery of an existing production application from candidate / goal / source identity,
- exact multi-premise seed reconstruction without cloning proof steps,
- explicit family-name dispatch,
- a multi-family standard execution facade.

General unbounded proof search, theorem ranking, producer ranking, proof-cost optimization, and best-proof selection are intentionally not implemented.

## Toda group calculation API

The calculation entry point is

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

A representative $\pi_9^5$ proof yields

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

## Standard production repository

The production builder is

```python
build_standard_production_proof_repository()
```

It assembles theorem-backed entries needed by supported production paths without creating new theorem truth.

## Generator-centered exploration

Generator-centered exploration supports exact aliases such as

```text
eta_2
nu_5
sigma_8
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

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1
$$

and

$$
H(\nu')=\eta_5.
$$

The exploration layer finds already represented proof facts. It does not evaluate $E$, $H$, or $\Delta$, and it does not solve Toda brackets.

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

## Safe applicability-candidate handoff

Phase 104 established

```text
selected applicability candidate
↓
candidate handoff
↓
execution-catalog validation
↓
READY
↓
explicit validated final rule
↓
bounded producer search
↓
prebuilt search report
↓
selected-path execution
↓
actual ProofStep provenance
```

The central identity invariant is

```text
candidate rule
is validation.execution_entry.rule
is search_result.final_rule
is goal_step.inference_rule
```

## First-family standard execution

Phase 105 connected one qualified production family to standard applicability execution.

The first qualified family is

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

The Phase 105 compatibility facade remains available:

```python
execute_standard_repository_generator_applicability_result_by_root_and_source(
  applicability_result,
  root_entry,
  source_step,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

It remains intentionally first-family-only.

## Applicability performance stabilization

Phase 106 identified full-scope applicability materialization as the main bottleneck.

```text
3889 proof-scope nodes
→ 797573 full-scope candidates
→ generator-node filtering
→ 176616 retained candidates
```

A generator-relevant scope prefilter reduced measured `nu_prime` applicability exploration from approximately

```text
27.89 s / 274.10 MiB peak
```

to

```text
8.16 s / 62.42 MiB peak
```

while preserving candidate semantics and provenance identity.

Repository-wide Phase 106 closure:

```text
8712 passed in 337.86s
```

## Multi-family qualified execution

Phase 107 expanded qualified production execution only where a concrete production need was demonstrated.

The currently admitted qualified production execution families are

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

The second family derives

$$
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}.
$$

Because the second family has two direct premises, a single applicability candidate is not enough to seed execution. Phase 107 therefore recovers the unique existing production application under the same root using

```text
same root_entry identity
same inference_rule identity
same explicit goal
candidate premise index
candidate source_step identity
```

A unique recovery contributes the exact original `premises` tuple. Those `ProofStep` objects are reused by identity and in original order; they are not cloned.

The explicit multi-family selection contract is

```text
root_entry identity
+
source_step identity
+
family_name
+
caller-supplied goal
```

The standard multi-family facade is

```python
execute_standard_repository_generator_applicability_result_by_root_source_and_family(
  applicability_result,
  root_entry,
  source_step,
  family_name,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

The operational path is

```text
standard applicability result
↓
all-qualified candidate filtering
↓
execution-family grouping
↓
explicit root + source + family selection
↓
family representative
↓
family-name dispatch
├─ first family
│  → exact one-source seed
│  → bounded execution
└─ second family
   → exact production-application recovery
   → exact two-premise seed
   → bounded execution
↓
actual ProofStep provenance
```

For `nu_prime` standard applicability exploration, the second family is visible through the premise containing `nu_prime`. The companion premise is recovered from the existing production application rather than discovered by an arbitrary cross-root search.

Phase 107 deliberately does not add automatic root/source/family selection, automatic goal discovery, theorem ranking, a new execution CLI, execution-result presentation integration, or a third qualified family without new architectural pressure.

Repository-wide Phase 107 closure:

```text
8783 passed in 290.63s
```

## Command-line interface

Existing commands remain

```powershell
python main.py n k
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

Phase 107 adds no new CLI command. Qualified execution remains a Python infrastructure capability because the current contract depends on proof-graph object identity and an explicit goal.

## Current boundaries

The following remain intentionally deferred:

- automatic symbolic higher-range instantiation,
- target-only unknown-right-hand-side proof search,
- theorem ranking and proof-cost optimization,
- producer ranking,
- general unbounded backtracking,
- persistent proof cache,
- repository snapshot/versioning,
- stale-search-report detection,
- free-form natural-language element search,
- wildcard family search,
- general composition evaluation,
- general Toda-bracket solving,
- bracket-value and coset / indeterminacy computation,
- general $E/H/\Delta$ evaluation,
- recursive theorem solving beyond already represented proof ancestry,
- automatic enumeration of unstated mathematical consequences,
- automatic production root/source/family selection,
- automatic execution-goal discovery,
- execution qualification across all production rule families,
- user-facing execution addressing / serialization,
- user-facing execution CLI,
- execution-result presentation integration,
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

standard applicability result
→ all-qualified filtering
→ execution-family grouping
→ explicit root + source + family selection
→ family-name dispatch
→ exact one- or multi-premise execution seed
→ bounded execution
→ actual ProofStep provenance
```

Phase 100 closed the production calculation path.

Phase 101 closed the production top-level generator-exploration path.

Phase 102 closed recursive proof-scope exploration for already represented Toda memberships and known map relations.

Phase 103 closed read-only applicable theorem / lemma discovery and the first production relevance-classification pass.

Phase 104 closed safe applicability-candidate consumption through bounded search and actual execution.

Phase 105 closed the first explicit standard-production applicability-to-execution path.

Phase 106 removed the dominant applicability-materialization bottleneck while preserving semantics and provenance.

Phase 107 closed the first multi-family qualified-production execution path, including exact multi-premise recovery, family dispatch, and a standard multi-family facade.

## Project principle

```text
actual mathematical or proof-search need
→ smallest missing representation or orchestration
→ preserve existing semantics and provenance
→ add focused regression coverage
→ measure pressure before expanding or optimizing
→ do not pre-implement future phases
```
