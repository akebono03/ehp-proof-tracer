# Phase 178 R6 — Finite Group Cardinality Isolated

Adds one conditional rule: a proved finite cyclic presentation has its listed order as cardinality, and a proved explicit direct sum of finite cyclic groups has cardinality equal to the product of the summand orders. Reuses `FiniteGroupCardinality`, typed endpoints and the existing nontrivial finite cyclic order guard. No source leaves, DB adoption policy, public provider, or renderer are changed. Zero-group cardinality and other group representations are outside this step.

Extract at the repository root. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase178_r6_finite_group_cardinality_isolated\run.ps1 -DryRun`, then repeat without `-DryRun`. The runner accepts the exact reviewed R5 hook, either committed or as the sole unstaged tracked edit. It requires the reviewed base as an ancestor, matching local and remote develop, exact dependency pins, and an unchanged tracked state after testing. Pytest cache writes are disabled. No full suite is run.

The isolated test suite uses synthetic proof premises only. A passing gate does not certify a homotopy group or connect the rule publicly.
