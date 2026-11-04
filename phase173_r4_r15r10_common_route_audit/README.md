# EHP Proof Tracer — Phase 173 R4-R15R10

## Purpose

A read-only regression audit of the common Web proof route following R15R9. No mathematics, generator identity, narrative renderer, common data model, production module, or documentation at repository root is changed. The audit checks that genuine abstract-group certificates remain distinct from incomplete named-generator proofs.

## Reviewed GitHub baseline

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed HEAD: `8bfa13946251c5618530641c572e8c756bb49af4`.
- Source-blob checks cover the common Web adapter, partial-result model, citation model, model renderer, existing abstract projection, and Web entry point.
- The R15R9 change is already included in that GitHub HEAD. An older local HEAD containing the exact same R15R9 working-tree code may pass the blob guards; this audit does not stage, merge, or commit anything.

## Tests and runtime checks

DryRun performs the reviewed-source guard, four small tests, and the existing isolated formatter tests. Normal mode also runs the four existing focused test modules for R15R7, R15R8, R15R9, and earlier complete Web regression, then checks live public Group Query results for n=4/k=8 and n=4/k=31, and representative completed n=3/k=3 and n=4/k=3. It writes `regression_report.json` only under this audit directory.

The audit refuses to run if the remote HEAD or reviewed source blobs differ. In that event the sources must be reviewed anew; do not disable the guards. No full pytest is run.

## Commands

From the local repository root, extract the ZIP, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r10_common_route_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r10_common_route_audit\run.ps1"
```

## Known boundary

`ProofNarrativeModel` currently projects citations from its `steps`; the R15R9 abstract certificate lives in `PartialProofResult.abstract_structure`. The shared Web adapter appends one abstract section after the existing Markdown renderer. This audit documents that architectural separation but deliberately does not migrate or reproduce abstract proof citations as new inferred facts. A future focused phase can decide whether to project the verified abstract certificate into the existing common model, with explicit citation ownership and without any n/k-specific branches.
