# EHP Proof Tracer — Phase 171 R2J-R4-R9-R8

This package connects the **existing generic finite-middle-group cardinality inference rule** to the shared backward expansion provider. It deliberately does not add a fixed group result, a proof step, a new mathematical theorem, a Web shortcut, or a special-case completed proof.

## Scope and prerequisites

The verified R9-R7 root hook must be present in `phase165_r52_r9_shared_math.py`. The R9-R8 installer accepts either its uncommitted exact four-line patch or an identical committed revision. It verifies the reviewed pre-R7 Git blob (`68846671215c38e3e0a572932b8ed955a7880edc`), rejects all unknown changes in that provider, and never calls Git reset, checkout, pull, or commit.

Only `shared_expansion_provider()` changes in that existing module. The new module `phase171_r2j_r4_r9_r8_public_cardinality/source.py` offers a `GoalExpansion` for a typed `FiniteGroupCardinality` goal when both EHP end-group candidates are uniquely determined from already screened fixed statements or a checked eta specialization. The general short-exact inference and group-order inference rules are reused; search must prove every premise.

This is one incremental production-provider connection. The complete public proof and Web presentation may remain unavailable. The audit records the actual status and unresolved goals rather than upgrading status.

## PowerShell

Unpack the ZIP at the repository root and execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r8_public_cardinality\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r8_public_cardinality\run.ps1"
git status -sb
git diff --stat
```

The runner executes eight new and eight R9-R7 focused regression tests; repository-wide pytest is deferred until Phase closeout. The installer writes the **full post-change** provider function, full production module, and pre-change backup into `output/`. Re-running the package after a successful installation is idempotent.
