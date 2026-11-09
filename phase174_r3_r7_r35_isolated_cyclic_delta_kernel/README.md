# Phase 174 R3-R7-R35 — Isolated General Cyclic Delta Kernel Rule

This package audits a general inference for the kernel of a homomorphism from
an infinite cyclic group to a finite cyclic group. Its conclusion requires
three separately certified premises and preserves the actual composite target
generator. It never registers a new literature fact, creates a trusted proof
step, or changes the public shared provider.

## Reviewed state

The reviewed remote `develop` HEAD is
`4200211563834028ed6c4e2eeb01004646b92ba9`. The handoff also accepts the
previous `89fcf47a22dbb212fe635381fa5af3095d5c1527` local HEAD when the
only tracked edit is the already reviewed R34 six-line source connection.

## Execution

Extract into the existing repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r35_isolated_cyclic_delta_kernel\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r35_isolated_cyclic_delta_kernel\run.ps1"
```

The normal run performs only focused pytest groups; no full-suite run or Web
HTTP completion is claimed. The printed R35 gate means that the **isolated**
rule was validated against existing source leaves. Publication to the shared
provider and proof of the root remain separate future work.

The complete added Python sources and tests are included in `CODE_FULL_JA.md`.
