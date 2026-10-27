# Phase 169 R10E2-R1 — Source-first Citation Repair

This is a **replacement** for the earlier `phase169_r10e2_unpositioned_citation.zip`.
Extract the new ZIP at the project root with `-Force`, then run the existing
`phase169_r10e2_unpositioned_citation/run.ps1`. The prior R10E2 run reported
7 failed tests and rolled back its five production changes. This repair includes
its full code, new tests, and a six-file guarded patch.

## Repair scope

- Supply the mandatory diagnostic when constructing a deliberately failed
  `PartialProofResult` in the test fixture.
- Test guarded double patching against the **unpatched backup** created by
  `patch.py`, rather than the already-patched production module.
- Preserve the legacy three-argument verification call for positioned goals.
  Only derived, unpositioned group goals pass the new opt-in keyword.
- Preserve the frozen reference title `Chapter V, i)`; remove only the renderer's
  series-specific alias that changed the earlier complete-proof baseline.

No new mathematical axioms or DB-derived proof steps are introduced.
Publication-positioned source records, the independent source screen, and the
existing proof-tree trust checks remain mandatory.

## Install and run

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10e2r1_unpositioned_citation_repair.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e2_unpositioned_citation\run.ps1"
```

`run.ps1` applies guarded changes, emits the full changed functions/files,
runs only relevant focused tests (including the Phase 168 trust-boundary
regressions), and audits representative 1-, 2-, 3- and higher-stem queries.
On failure all six production files are restored. The full pytest suite is
not run in this step.

## Production files

- `phase165_r52_r9_shared_math.py`: `search_shared_group_goal`
- `phase165_r55_nk_only_goal.py`: `search_group_from_registered_goal`
- `web_group_proof.py`: `build_standard_web_group_proof_view`
- `phase168_r3_41p13_trust_boundary/verification.py`: `verify_proof_tree_for_narrative`
- `phase169_r10e1_general_group_transport/transport.py`: `expand_prior_general_group_transport`
- `phase168_r3_5_model_renderer.py`: `render_model_backed_narrative_markdown`

No existing module-level imports are changed. All changes are scoped to the
functions listed above; complete versions are written into `output/`.

## R10E2-R2: tracked-file side-effect diagnosis

The previous 115 focused tests passed, but the post-run worktree check stopped
before installation could be accepted. This revision changes **only `run.ps1`**;
all mathematical source changes, Python patch logic, and tests are the same as
R10E2-R1. A complete snapshot of the tracked-file names outside the six patch
targets is taken before applying the patch and again after focused validation.

If the set changes, the script prints `R10E2R2_UNRELATED_ADDED` and
`R10E2R2_UNRELATED_REMOVED`, saves a machine-readable report at
`output/r10e2r2_tracked_diff.json`, and restores the six patched production
files. It never performs git checkout/reset or modifies unrelated files.
This makes the cause of the previous integrity failure observable; it does not
presume the detected change is safe or declare the mathematical search complete.
