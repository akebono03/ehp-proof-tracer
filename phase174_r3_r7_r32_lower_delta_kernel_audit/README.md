# Phase 174 R3-R7-R32 — Lower Delta Kernel General Audit

This package performs a **read-only, source-first audit** of the conditional
free-to-finite cyclic kernel computation for the lower EHP Delta map. It does
not modify the production search, registry, renderer, database, or source files.
It creates no GIVEN, verified ProofStep, or registered mathematical rule.

## Reviewed baseline

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed GitHub HEAD: `25118e281445ca17b30c60c8fd02d00acaa25ea5`.
- R30's ten-line shared-provider change is already merged at this HEAD.
- The R31 audit package must be retained unchanged, whether untracked or
  otherwise locally available. No reset, checkout, or write to R31 occurs.

## Mathematical contract

For a genuine homomorphism of abelian groups

`Delta: Z{g} -> (Z/m){h}`, with `m >= 1` and `Delta(g) = +/- h`, the kernel
is `<m*g>`. All three mathematical premises require independent proof. The
reviewed source states the finite codomain in Toda Proposition 5.8 and the
image of the diagonal generator in equation (5.10); the kernel mentioned in
Proposition 5.9 is a **consequence**, never a new premise.

R32 does not claim that these textual statements are certified typed proof
steps in the public search. A database prior, if found, is reported as such
and is not silently treated as a literature citation.

## Install and run

Extract the ZIP directly into the existing repository root. In Windows
PowerShell, run the following commands from the root directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r32_lower_delta_kernel_audit\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r32_lower_delta_kernel_audit\run.ps1'
```

The complete PowerShell command including exit-code checks is included in
`AUDIT_PLAN_JA.md`. The normal run performs Source Guard, a report-only
source/proof-frontier audit, and five groups of **focused** pytest runs.
The full test suite is intentionally not run.

Reports are written outside the Git working tree to
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r32\`.

## Success and non-claims

A successful R32 audit establishes only the validity of the **conditional**
cyclic-kernel reasoning and the integrity of the inspected source evidence.
It leaves the lower Delta kernel, upper Delta surjectivity, and target group
zero statement **unproved**. A changed GitHub HEAD or modified pinned source
must halt the audit for review rather than be reset or overwritten.
