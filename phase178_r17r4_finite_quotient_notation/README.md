# Phase 178 R17R4 — Finite cyclic quotient notation

Display-only follow-up to R17R3. The previous package and its successful public proof are prerequisites. The reviewed GitHub baseline is `720a7e8658a3f7e94f92a20ab530f763f1b421e1` on develop. R17R3 may be uncommitted (as in the reported successful run) or committed, provided all checked contents match.

For a finite cyclic group $A=\mathbb Z/N\{a\}$ and a signed generator image $\Delta(z)=\pm ta$, the already certified quotient rule implies that the image subgroup has order $N/\gcd(N,t)$. The narrative now displays $\mathbb Z/(N/\gcd(N,t))\{|t|a\}$, or $0$ when the subgroup is trivial, rather than angle brackets. Both the kernel equality and quotient denominator use the same notation. The existing rule replay and six-premise checks are unchanged.

## Changes

- `phase178_r17r3_common_renderer/projection.py`: add a display-only formatter and use it in `finite_cyclic_quotient_reason`.
- `phase178_r17r3_common_renderer/tests/test_display.py`: strengthen actual public narrative assertions; add parameterized formatter tests for distinct orders, nondividing and negative multiples, and trivial subgroups.
- This package contains the full replacement files as UTF-8 text, a hash manifest, an installer, and a PowerShell entry point.

## Execution

Extract into the repository root, run `run.ps1 -DryRun`, then `run.ps1`. The installer checks the previous distribution hashes, exact previously installed renderer hooks, dependency blobs, branch, upstream HEAD, and unrelated tracked changes. Dry run exports the full proposed files to `%LOCALAPPDATA%/EHPProofTracerAudit/phase178_r17r4_finite_quotient_notation`; application preserves original bytes as backups. No GitHub write or commit is performed.

The focused suite includes the previous R17R3 public proof and Phase 177 regressions, with seven additional formatter cases. The actual proof must still be complete with 18 steps, six model citations, no open goals, VERIFIED trust, and no target GIVEN. Full pytest is not run. The complete repository was not available in the artifact environment, so local integration tests must pass before accepting R17R4.
