# EHP Proof Tracer — Phase 173 R4-R15R8

## Purpose

Attach an independently verified, source-first Toda Proposition 4.4 **abstract group certificate** to an incomplete canonical named-group query without changing its completion status. This is a minimal public-result-model connection; it does **not** change the renderer or claim a proof of named generator identities.

For a registered n=4 target with k>=3, the source-first R15R7 certificate is attached only after the normal named proof has failed or remained partial and after its exact target and proof guard are reverified. Every other group query preserves its previous result.

The example pi_35^4 has certified abstract invariants (Z/2)^8 using two adopted DB priors. The eight displayed named generators are still not certified by this certificate.

## Production changes

- `phase165_r52_partial_proof.py`: add `CertifiedAbstractStructure` and an optional `PartialProofResult.abstract_structure` field; reject a sidecar that changes the named group's completion or structure status.
- `phase165_r55_nk_only_goal.py`: update the complete `search_group_from_registered_goal` function at its existing named search return and proof-order diagnostic exit, to attach the certificate when appropriate.

The selector's module imports are unchanged. The result module's complete updated import section adds `ProofRule`. No changes to core mathematics, the database, public Web renderer, or existing result fields are made.

## Preconditions

The install runner verifies GitHub/local `develop` HEAD lineage, exact reviewed Git blobs, and the R15R7 and R15R6 source files. The only permitted tracked worktree changes before installation are the existing pytest node IDs. Subsequent reruns also accept exactly the two reviewed installed files. Other changes fail closed.

## PowerShell

From `C:\Users\user\Dropbox\Python\fitz\ehp_proof`:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_R4_R15R8_PUBLIC_ABSTRACT_SIDECAR.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r8_public_abstract_sidecar\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R15R8 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r8_public_abstract_sidecar\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R15R8 failed" }
git status -sb
git diff --stat
```

DryRun checks and previews code without editing production. Normal execution installs only two files and runs focused pytest, then runs the existing public zero/Web regression, audits n=4,k=4,7,8,31 and invokes the actual registered Group Query selector for k=31 (without changing Web rendering). A failure in the focused tests or audit triggers a guarded rollback to the reviewed original files. The generated `FULL_CHANGED_UNITS.md` contains the complete revised production classes and function extracted from the actual checked-out repository.

## Completion conditions

- `PHASE173_R4_R15R8_SOURCE_GUARD=PASS`
- `PHASE173_R4_R15R8_FOCUSED_PYTEST=PASS`
- `PHASE173_R4_R15R8_K31_REAL_PUBLIC_SELECTOR=PASS`
- `PHASE173_R4_R15R8_K31_PUBLIC_RESULT_ABSTRACT=PASS`
- `PHASE173_R4_R15R8_AUDIT=PASS`
- The named result remains incomplete with its original open goals, while `abstract_structure` contains a checked inference root.

Full pytest is deferred until the end of Phase 173. The next step is a generic projection of abstract evidence in the shared Web view, still without promoting named-generator completeness.
