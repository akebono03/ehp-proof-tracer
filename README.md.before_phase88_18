# EHP Proof Tracer

EHP Proof Tracer is an experimental Python project for representing and checking proof dependencies in Toda-style calculations of homotopy groups of spheres, with a particular focus on EHP sequences and low stable stems.

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

Proof provenance is preserved with `ProofStep` objects instead of storing only final conclusions.

## Current proof-search capability

The current high-level flow is:

```text
goal
-> goal-compatible final-rule selection
-> missing-premise analysis
-> bounded producer search
-> finite explicit producer retry when authorized
-> search diagnostics
-> execution diagnostics
-> unified search report
-> exact selected-path execution
-> goal ProofStep
```

The bounded search uses an explicit `max_depth`. The validator accepts integer values `>= 2`, with formal regression coverage through:

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

Phase 87 adds an explicit, finite retry policy:

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
-> selected second producer is executed
-> final rule uses the selected producer ProofStep
-> requested goal ProofStep is derived
```

A failed candidate and its discarded dependency branch do not appear in execution provenance.

## Search policy and safety boundaries

The current bounded search preserves:

```text
finite explicit depth limit
finite explicit retry budget
safe producer filtering
catalog-order deterministic attempts
cycle detection
shared producer identity reuse
deterministic dependency-first ordering
failed-attempt state rollback
exact selected-path execution
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

The Phase 87 probe verifies:

```text
retry_policy=None -> AMBIGUOUS_PRODUCER
max_attempts=1 -> PRODUCER_RETRY_EXHAUSTED
max_attempts=2 -> SUCCESS
selected second producer -> final -> goal
failed first branch absent from execution provenance
repository non-mutation
```

## Verification

Latest confirmed repository-wide regression before the Phase 87-6 probe/documentation additions:

```text
7043 passed in 41.53s
```

Run the Phase 87 completion verification with:

```powershell
python -m py_compile `
  repository_inference.py `
  probes/probe_phase87_capabilities.py `
  tests/test_phase87_minimal_retry_policy_representation.py `
  tests/test_phase87_selection_side_finite_retry.py `
  tests/test_phase87_retry_diagnostics_report.py `
  tests/test_phase87_selected_path_execution_retry_provenance.py `
  tests/test_phase87_probe.py

python -m pytest `
  tests/test_phase87_minimal_retry_policy_representation.py `
  tests/test_phase87_selection_side_finite_retry.py `
  tests/test_phase87_retry_diagnostics_report.py `
  tests/test_phase87_selected_path_execution_retry_provenance.py `
  tests/test_phase87_probe.py `
  tests/test_phase85_execution_failure_diagnostics.py `
  tests/test_phase86_explicit_max_depth_parameterization.py `
  tests/test_phase86_depth_three_bounded_search.py `
  tests/test_phase86_depth_four_bounded_search.py `
  -x --tb=line -q

python -m probes.probe_phase87_capabilities
python -m pytest -q
git diff --check
```

Wall-clock time is machine-dependent. Test count, semantic coverage, provenance coverage, focused regression, and repository-wide regression are the primary cross-machine signals.

## Documentation

```text
README.md
= current status and capabilities

docs/design.md
= architecture, semantics, and design boundaries

docs/development_log.md
= chronological implementation history

docs/code_reference.md
= code navigation

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
