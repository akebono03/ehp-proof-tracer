# Phase 171 R2J–R4–R9–R17 — Public Context / Dependency Audit

This package audits why the independent EHP map obligations proved in R16 do not assemble into a completed public proof for π₆(S³). **It does not patch production code or change a mathematical theorem.**

R16 independently verified both Hopf surjectivity obligations, the vanishing of Δ, and suspension injectivity using the canonical `reconstruct_registered_goal` search. The ordinary public group proof remains partial. A rejected cyclic route alone cannot explain all failures because the resolver tries alternative proposals. R17 therefore compares the *actual public search screened context*, obtained via `context_sink`, with the R16 audit context and independently re-runs the canonical resolver using both contexts.

Eight exact typed goals are checked in each context: Hopf surjectivity at degrees 7 and 6, Δ=0, E injective, EHP short exact sequence, middle group cardinality four, order of the generator identified by cited root expansions, and cyclic structure. The target group is not supplied as a proof premise, no verified proof tree is replayed, and no `GIVEN` source is registered. Every independently proved goal is still only a subgoal, not completion of the public root.

## Prerequisites

- `develop` branch with reviewed R11 provider blob `10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac`.
- R16 audit package and successful `phase171_r2j_r4_r9_r16_hopf_route_audit/output/audit.json` in the repository.
- The original Phase 171 source registry and pytest environment.

## Run with Windows PowerShell

Extract `EHP_Phase171_R2J_R4_R9_R17_PUBLIC_CONTEXT_PATH_AUDIT_ONLY.zip` into the repository root. From that directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r17_public_context_path_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r17_public_context_path_audit\run.ps1"
```

The script executes only six focused tests with pytest's cache provider disabled and then writes `output/audit.json`. The full test suite is deliberately not run. The output prints `PHASE171_R17_CONTEXT_SAME_ID_SET`, `PHASE171_R17_PROBE_STATUSES`, and `PHASE171_R17_CLASSIFICATION`.

## Safety and scope

R17 is read-only with regard to all tracked files. It requires a reviewed R16 audit report and checks unchanged tracked Git status. No provider is modified, no completed proof imported, no asserted generator order assumed, and no invalid suspension isomorphism introduced. R18, if needed, may implement a narrowly reviewed connection or search-path correction based on the observed evidence; R17 does not implement it in advance.
