# EHP Proof Tracer — Phase 173 R4-R15R9

## Purpose

Surface a separately certified abstract homotopy-group structure in the **existing common Web proof adapter**, without changing or completing a pending named-generator goal. This change adds no alternative narrative, specialized n/k branch, mathematical inference rule, or source assertion.

An example for the registered group `pi_35^4` is the **abstract-only** conclusion `pi_35^4 ≅ (Z/2)^8`. Eight individually named generators remain unproved. The standard result retains `generic-partial-proof`, its original `status`, `conclusion`, `open_goals`, and proof citation scope.

## Production change

Only `phase165_r52_r3_web_adapter.py` is edited, in the complete function `build_partial_web_group_proof_view`. Its module imports are unchanged. The existing model-backed and fallback narrative renderers still render their own proof text. The adapter uses one shared read-only projection for either path. Trace mode remains unchanged.

The new package includes:

- `projection.py`: pure abstract-invariant formatting and a certificate-only Markdown section.
- `patch_source.py`: one-guarded-function source transformation.
- `install.py`: Git source and lineage guards, dry-run, atomic install and rollback.
- `audit.py`: independently checks the real registered public selector and Web presentation for `k=8` and `k=31`.
- `tests/`: standalone and repository-backed focused regression tests.
- `reviewed_source/`: exact reviewed original and complete proposed adapter (text copies only).
- `FULL_CHANGED_UNITS.md`: entire revised production function and full unchanged import block.
- `SOURCE_CODE.md`: complete changed and added source, tests, and commands.

## Prerequisites

Use a local checkout of `akebono03/ehp-proof-tracer`, branch `develop`, with a matching `origin/develop` HEAD and the Phase 173 R4-R15R8 abstract sidecar **installed and committed**. The baseline ancestor is `e3fa8cf71777b1bf5bb431ec06cd2147bce69086`. The installer checks exact source blob identities for the unchanged renderer and the committed R15R8 result model and selector.

## PowerShell

From the repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r9_shared_abstract_renderer\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r9_shared_abstract_renderer\run.ps1"
```

DryRun performs only a guarded preview and eighteen standalone tests. Normal execution applies one production-file patch, runs focused `pytest`, checks the common Web path, and writes `shared_abstract_web_report.json`. The installer automatically restores the previous module if a subsequent test or audit fails. No complete repository-wide test run is performed.

## Proof boundary

An abstract invariant is displayed only when the `PartialProofResult.abstract_structure` is a validated `CertifiedAbstractStructure`, accepted by the source-first proof construction already installed in R15R7 and R15R8. This adapter does not create a proof step, generator identification, new GIVEN statement, or completion. A missing certificate changes **no** rendered text. The exact cited proof is preserved in the sidecar's proof tree; the shared narrative is not replaced.

R15R9 is not a Phase 173 closeout. The remaining generator-image proof obligations are not addressed here.
