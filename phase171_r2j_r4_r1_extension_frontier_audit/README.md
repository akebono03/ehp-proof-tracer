# Phase 171 R2J-R4-R1 — Read-only Extension Frontier Audit

This package inspects the remaining typed obligations for proving the cyclic order-four presentation of $\pi_6^3$. It requires the installed R2J-R3 code and existing cited R2I/R2J-R2 modules. It makes **no changes** to production files, existing tests, or global project documentation.

Nested composite generators are validated through the existing recursive endpoint checker. In particular, the candidate for $\pi_5^2$ must have the type of $\eta_2^3 : S^5 \to S^2$; a bare $\eta_2$ is rejected. This check creates a **candidate goal only**, not a proof step.

It checks the genuine inferred proof of $E:\pi_5^2\to\pi_6^3$ injectivity, earlier screened Toda (5.3) identities, the typed Proposition 4.2 $E$–$H$ window, a database goal for $\pi_5^2$, and the backward-search frontier of the proposed generator suspension image.

This is a diagnostic, **not** a completed proof of $\pi_6^3$. It never creates an independent `GIVEN` from a DB row, treats a proposed subgoal as proved, or imports the target Proposition 5.6 conclusion.

## Run

Extract into the repository root on the `develop` branch. From that root, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r1_extension_frontier_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r1_extension_frontier_audit\run.ps1"
```

The second command runs four focused pytest tests with cache persistence disabled, then writes `output/audit.json` and `output/audit.md` under this untracked audit package. It does **not** run the full test suite.
