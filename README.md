# EHP Proof Tracer

EHP Proof Tracer is an experimental Python project for representing, checking, and increasingly automating proof dependencies in Toda-style calculations of homotopy groups of spheres, with a particular focus on EHP sequences and low stable stems.

## Current mathematical frontier

The repository formalizes the concrete proof spine through Toda Lemma 5.16 and consolidates the stable groups through stem 7:

```text
G_0 = Z{iota}
(G_1;2) = Z/2{eta}
(G_2;2) = Z/2{eta^2}
(G_3;2) = Z/8{nu}
(G_4;2) = 0
(G_5;2) = 0
(G_6;2) = Z/2{nu^2}
(G_7;2) = Z/16{sigma}
```

Proof provenance is preserved with `ProofStep` objects rather than storing only final conclusions.

## Current proof-search capability

The current high-level flow is:

```text
goal
-> goal-compatible final-rule selection
-> missing-premise analysis
-> binding preservation
-> concrete requested-statement construction when fully bound
-> concrete producer compatibility filtering
-> bounded producer search
-> finite explicit producer retry only for remaining true ambiguity
-> search diagnostics
-> execution diagnostics
-> unified search report
-> exact selected-path execution
-> concrete producer-output validation
-> goal ProofStep
```

The bounded search uses an explicit `max_depth`. Formal regression currently covers:

```text
max_depth = 2
max_depth = 3
max_depth = 4
```

The default remains:

```text
max_depth = 2
```

The existing compatibility API names are intentionally preserved:

```text
select_unique_depth_two_producer_chain()
diagnose_depth_two_producer_search_failure()
build_depth_two_producer_search_report()
execute_depth_two_producer_search()
```

## Phase 87: finite producer retry

Phase 87 introduced:

```text
FiniteProducerRetryPolicy(max_attempts=N)
```

The default remains conservative:

```text
retry_policy=None
-> multiple safe producer candidates
-> AMBIGUOUS_PRODUCER
-> stop
```

With an explicit retry policy, safe producer candidates are attempted in deterministic catalog registration order, bounded by `max_attempts`.

Representative behavior:

```text
no retry policy
-> AMBIGUOUS_PRODUCER

max_attempts=1
-> first candidate fails during selection
-> PRODUCER_RETRY_EXHAUSTED

max_attempts=2
-> first candidate fails during selection
-> temporary selection state is rolled back
-> second candidate is selected
-> report SUCCESS
-> selected producer is executed
-> final rule uses the selected producer ProofStep
-> requested goal ProofStep is derived
```

A failed candidate and its discarded dependency branch do not appear in execution provenance.

## Phase 88: concrete theorem-instance producer compatibility

Phase 88 distinguishes a type-level producer collision from a real ambiguity for one concrete theorem instance.

Representative realistic collision:

```text
TodaDeltaImageUpToSignStatement producers:

Delta(iota_5)
Delta(iota_9)
Delta(iota_17)
```

A type-only lookup can see all three rules. When the requesting premise is concrete, the search now carries that concrete requested statement forward:

```text
known sibling premises
-> variable bindings
-> fully bound missing premise
-> requested_statement
-> producer conclusion-type filter
-> goal_compatibility(requested_statement)
-> concrete-compatible producer candidates
```

For example:

```text
requested statement = Delta(iota_17)

type-level candidates:
  Delta(iota_5) rule
  Delta(iota_9) rule
  Delta(iota_17) rule

concrete-compatible candidates:
  Delta(iota_17) rule
```

This removes false `AMBIGUOUS_PRODUCER` failures before retry is considered.

The boundary is now:

```text
different theorem instances with the same conclusion type
-> Phase 88 concrete compatibility filtering

multiple producers still compatible with the same concrete requested statement
-> true ambiguity
-> Phase 87 finite retry, if explicitly authorized
```

Phase 88 also makes unsafe-producer diagnostics use the same concrete compatibility semantics, preserves the concrete requested statement in the selected search node, and validates producer output against that concrete statement during execution.

If no concrete requested statement can safely be constructed, the legacy type-only behavior remains in effect.

## Phase 88 end-to-end regression

The final Phase 88 regression uses real Delta producer rules from the existing Toda development:

```text
Phase 52: Delta(iota_5)
Phase 66: Delta(iota_9)
Phase 76: Delta(iota_17)
```

with real Phase 76 prerequisites and a minimal synthetic final shell.

It verifies:

```text
type-only lookup sees the realistic collision
-> concrete Delta(iota_17) request
-> unrelated Delta rules are filtered out
-> unique Delta(iota_17) producer is selected
-> selected node preserves requested_statement
-> search report is SUCCESS
-> execution derives the concrete producer ProofStep
-> final goal ProofStep is derived
-> selected rule identity is preserved
-> repository is not mutated
```

## Search policy and safety boundaries

The current bounded search preserves:

```text
finite explicit depth limit
finite explicit retry budget
fixed-point-safe producer filtering
concrete theorem-instance filtering when available
legacy type-only compatibility when concrete context is unavailable
catalog-order deterministic retry attempts
cycle detection
shared producer identity reuse
deterministic dependency-first ordering
failed-attempt state rollback
exact selected-path execution
concrete producer-output validation
ProofStep provenance
repository non-mutation
default retry-policy compatibility
default max_depth=2 compatibility
```

Still intentionally not implemented:

```text
unbounded search
general backtracking
producer ranking
proof-cost models
best-proof selection
DFS / BFS / A*
formal max_depth > 4 regression coverage
persistent search cache
automatic proof narrative generation
generic theorem proving
```

## Representative probes

Phase 86 bounded-depth probe:

```powershell
python -m probes.probe_phase86_capabilities
```

Phase 87 finite-retry probe:

```powershell
python -m probes.probe_phase87_capabilities
```

Phase 88 is currently fixed by focused and end-to-end regression tests rather than a new production probe.

## Verification

Latest confirmed repository-wide regression after Phase 88-17:

```text
7096 passed in 35.90s
```

Key Phase 88 completion checks:

```text
Phase 88 end-to-end regression:
8 passed in 2.06s

Phase 88 related regression:
47 passed in 2.96s

search / retry / execution related regression:
34 passed in 2.41s

repository-wide:
7096 passed in 35.90s

git diff --check:
clean
```

Wall-clock time is machine-dependent. Test count, semantic coverage, provenance coverage, focused regression, and repository-wide regression are the primary cross-machine signals.

## Documentation

```text
README.md
= current status and capabilities

docs/design.md
= current architecture, semantics, and design boundaries

docs/development_log.md
= chronological implementation history

docs/code_reference.md
= current code navigation

docs/proof_records.md
= representative mathematical and infrastructure records

docs/roadmap.md
= future-oriented plan and deferred boundaries
```

## Project principle

The implementation follows a narrow-extension policy:

```text
actual mathematical or proof-search need
-> smallest missing representation or orchestration
-> preserve existing semantics and provenance
-> add focused regression coverage
-> do not pre-implement future phases
```
