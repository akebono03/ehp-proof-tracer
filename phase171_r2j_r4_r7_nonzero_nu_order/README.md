# EHP Proof Tracer — Phase 171 R2J-R4-R7

This independent, read-only audit reconstructs two typed inferences:

1. $2\nu'\neq0$ in $\pi_6^3$ from the already proved $2\nu'=E(\eta_2^3)$, the injectivity of $E:\pi_5^2\to\pi_6^3$, and the earlier cited $\pi_5^2\cong\mathbb Z/2\{\eta_2^3\}$.
2. $\nu'$ has order exactly four using the R4-R6 inferred cardinality $|\pi_6^3|=4$ and the inferred nonzero double.

The rules are structural and work with typed group endpoints and matched generator identity, not printed expressions. The earlier cited group is an existing screened `GIVEN` leaf and is never recreated or promoted from database metadata. The R4-R3 relation, E-injectivity, and R4-R6 cardinality remain independently inferred proof subtrees.

## Scope

The package adds only `phase171_r2j_r4_r7_nonzero_nu_order/`: `source.py`, `audit.py`, focused tests, launcher, and full source records. It does not modify production Providers, prior phase packages, the tracked documentation, or the Git index. It does not assert a completed cyclic presentation of $\pi_6^3$; that final step belongs to R4-R8.

## Windows PowerShell

From the repository root, extract the ZIP and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r7_nonzero_nu_order\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r7_nonzero_nu_order\run.ps1"
git status -sb
git diff --stat
```

The runner checks the `develop` branch, runs 31 focused tests (12 new, 10 R4-R6 and 9 R4-R3), then reconstructs the actual proof trees. It leaves the entire test suite for Phase 171 closeout. Real-repository test and replay success must be verified on the local worktree.

## Success criteria

The audit must report `PHASE171_R2J_R4_R7_DOUBLE_NONZERO=INFERRED`, `PHASE171_R2J_R4_R7_NU_PRIME_ORDER_FOUR=INFERRED`, `PHASE171_R2J_R4_R7_NEW_GIVEN=0`, and `PHASE171_R2J_R4_R7_PI63_PROVEN=False`. Every `GIVEN` ancestor must uniquely match an earlier publication-screened fixed assertion; a completed middle-group presentation must not enter the proof.
