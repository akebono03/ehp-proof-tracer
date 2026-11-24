# Phase 176 R3R43R1 — Isolated finite cyclic subgroup lift

This additive package implements one typed EHP inference, without editing shared files or registering new GIVEN statements.

For injective $H:A\to B$, $\operatorname{Im}H=\ker\Delta$, $B=\mathbb Z/m\{b\}$, $\ker\Delta=\langle qb\rangle$ and $H(a)=qb$, the conclusion is $A=\mathbb Z/(m/\gcd(m,q))\{a\}$. The five antecedents must be independently inferred proof steps. The candidate constructor does not certify any antecedent. Positive integer $m,q$ are required, including the order-one case at the `CyclicStructureStatement` level. The proof uses strict typed expression equality, not display-name aliases.

## Files and execution

Extract the archive into the repository root on `develop`. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated\run.ps1
```

The guard checks clean tracked files and reviewed Git blob IDs, not remote merge ancestry. If a reviewed file changed, stop and review rather than bypassing the guard. A fresh checkout of the full project and its dependencies is required. Tests use `--import-mode=importlib` to avoid duplicate test module names. No full pytest run. No public provider connection. The synthetic fixtures only verify rule mechanics; the actual group is not proved here. The archive creator checked syntax, but did not run pytest against the full repository.

Success: `PASS_R3R43R1_ISOLATED_FOCUSED_TESTS`. Next: verify the independent kernel premise and candidate binding before any public provider connection. Do not register the target group as GIVEN.
