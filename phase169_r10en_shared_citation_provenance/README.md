# Phase 169 R10EN — Shared Citation Provenance

This patch consolidates *presentation-only* citation-provenance checking for two already verified generator-transport projections. It does not alter proof rules, backward search, the Proof Tree, the model renderer, the source registry, or existing public projection APIs.

## Prerequisites

- Windows PowerShell 5.1 or later, Python and pytest configured for EHP Proof Tracer.
- Repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- The current GitHub `develop` includes R10EL and R10EM; the package validates the exact reviewed blob IDs of both target projection files.
- No uncommitted modifications in the two target `projection.py` files.

## Installation and execution

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10en_shared_citation_provenance.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10en_shared_citation_provenance\run.ps1"
git status -sb
```

The script validates Git dependencies and checks 16 independent tests before replacing the two reviewed functions. It then runs only the targeted R10A, R10EC, R10EL and R10EM tests and a four-group live-proof audit. The entire pytest suite is **not** executed. The pytest cache provider is disabled.

## Modified production functions

- `phase169_r10a_verified_stable_chain_projection/projection.py::project_verified_stable_image_chain`: now calls the shared helper with `require_each=False` (original nonempty-union policy).
- `phase169_r10ec_direct_sum_narrative_projection/projection.py::project_verified_direct_sum_transport`: now calls the shared helper with `require_each=True` (original per-image policy).
- New `phase169_r10en_shared_citation_provenance/core.py::verified_generator_image_citation_numbers` is shared by both existing projections.

All imports are inside the modified functions; their module-level import sections remain untouched. Full replacement units are exported as `r10a_after.py.FULL`, `r10ec_after.py.FULL`, `project_verified_stable_image_chain_FULL.py`, and `project_verified_direct_sum_transport_FULL.py`.

## Fail-closed checks

The helper accepts only GIVEN-ancestor citations registered in the supplied model, traced by exact ProofStep identity. It rejects missing ancestors, ambiguous image indices, duplicate image references, unregistered citations, or a missing required citation. A failed check yields `None`; it never invents a source or a mathematical claim.

The audit checks complete proofs, Trust Boundary verification, unchanged citation numbers, exact prior hidden-step counts (31/40/10/110), unchanged proof trees and references, and zero repeated one-step image equations. On any failed test or audit, the two production files are restored byte-for-byte from backups in `output/run_*`.

## Scope boundary

R10EN does not unify mathematical inference or formatting of cyclic and direct-sum groups. It does not modify incomplete 11-/14-stem goals or add free-cyclic or zero-group behavior. Full-suite pytest belongs only to the end of Phase 169.
