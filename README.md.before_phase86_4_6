# EHP Proof Tracer

EHP Proof Tracer is an experimental Python project for representing and checking proof dependencies in Toda-style calculations of homotopy groups of spheres, with a particular focus on EHP sequences and low stable stems.

## Current mathematical frontier

The repository currently formalizes the concrete proof spine through Toda Lemma 5.16 and consolidates the stable groups through stem 7:

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

The project records proof provenance with `ProofStep` objects rather than storing only final conclusions.

## Current proof-search capability

The current high-level flow is:

```text
goal
-> goal-compatible final-rule selection
-> missing-premise analysis
-> bounded producer search
-> search-failure diagnostics
-> execution-failure diagnostics
-> unified search report
-> exact selected-path execution
-> goal ProofStep
```

Phase 86 adds an explicit bounded depth parameter. The supported values are currently:

```text
max_depth = 2
max_depth = 3
```

The default remains:

```text
max_depth = 2
```

The following APIs support both depth 2 and depth 3 while preserving the existing API names for compatibility:

```text
select_unique_depth_two_producer_chain()
diagnose_depth_two_producer_search_failure()
build_depth_two_producer_search_report()
execute_depth_two_producer_search()
```

The names still contain `depth_two` because Phase 86 intentionally avoids a compatibility-breaking rename.

## Depth-3 behavior

For a unique chain

```text
final
<- A   depth 1
<- B   depth 2
<- C   depth 3
```

Phase 86-3 verifies the paired behavior:

```text
max_depth=2
-> DEPTH_LIMIT

max_depth=3
-> select C, B, A in dependency-first order
-> execute C
-> execute B using C's ProofStep
-> execute A using B's ProofStep
-> execute final using A's ProofStep
-> derive the requested goal ProofStep
```

The repository remains unchanged during search and execution; generated steps are returned in inference results rather than auto-registered.

## Search policy and safety boundaries

The bounded search intentionally remains conservative:

```text
finite explicit depth limit
unique safe producer policy
cycle detection
shared producer identity reuse
deterministic dependency-first ordering
exact selected-path execution
repository non-mutation
```

Still intentionally not implemented:

```text
max_depth > 3
retry / backtracking
alternative producer planning
producer ranking
proof-cost models
best-proof selection
DFS / BFS / A*
unbounded recursive theorem search
persistent search cache
automatic proof narrative generation
generic theorem proving
```

## Representative probes

Phase 86 representative probe:

```powershell
python -m probes.probe_phase86_capabilities
```

It checks both:

```text
Phase 86-2 compatibility baseline
+
Phase 86-3 depth=3 end-to-end execution
```

The representative synthetic depth-3 chain is deliberately small so that bounded-search semantics, diagnostic depth, dependency ordering, provenance, and repository non-mutation are directly visible.

## Verification

Latest confirmed repository-wide regression before the Phase 86-3-6 completion update:

```text
6989 passed in 35.32s
```

Phase 86-3-6 adds representative-probe and completion-regression coverage. Run:

```powershell
python -m py_compile `
  repository_inference.py `
  probes/probe_phase86_capabilities.py `
  tests/test_phase86_depth_three_bounded_search.py `
  tests/test_phase86_explicit_max_depth_parameterization.py `
  tests/test_phase86_probe.py

python -m pytest `
  tests/test_phase86_depth_three_bounded_search.py `
  tests/test_phase86_explicit_max_depth_parameterization.py `
  tests/test_phase86_probe.py `
  tests/test_phase84_bounded_depth_two_execution.py `
  tests/test_phase84_depth_two_safety_regression.py `
  tests/test_phase85_nested_producer_cycle_depth_classification.py `
  -x --tb=line -q

python -m probes.probe_phase86_capabilities
python -m pytest -q
git diff --check
```

Wall-clock time is machine-dependent; test count, semantics, provenance coverage, and focused regression are the primary cross-machine signals.

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
