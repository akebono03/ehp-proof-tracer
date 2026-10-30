# Phase 171 R2J-R4-R9-R1 — Public Proof Search and Web Boundary Audit

This **read-only** package audits whether the already inferred $\pi_6^3\cong\mathbb Z/4\{\nu'\}$ Proof Tree from R4-R8 is discoverable through the canonical shared backward search and displayed via the verified Web narrative route.

The package performs independent checks of the R4-R8 root, shared-provider candidate expansions, canonical search status, and `build_standard_web_group_proof_view()`. It never supplies an already completed proof as a search result, manufactures a `GIVEN`, alters the trust boundary, or upgrades a partial Web result.

No production or existing test files are changed. The full repository test suite is deferred to the Phase closeout.

Unpack the ZIP in the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r1_public_path_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r1_public_path_audit\run.ps1"
git status -sb
git diff --stat
```

The audit writes `output/audit.json` and reports separately whether the R4-R8 root has a matching public rule, whether the public search returns `complete`, and whether the existing Web trust-gated narrative is complete. A missing public integration is a valid audit finding, **not** a successful Web integration.
