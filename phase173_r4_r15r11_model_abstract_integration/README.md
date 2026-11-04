# EHP Proof Tracer — Phase 173 R4-R15R11

## Purpose

Move already-certified abstract group structure into the existing `ProofNarrativeModel` and the standard Model-backed rendering route, without adding a dimension-specific narrative, changing mathematical inference, or completing pending named-generator goals.

This stage deliberately retains the legacy Web route as a compatibility path. The default Model-backed Web route no longer appends abstract Markdown from `PartialProofResult` after the renderer. The existing `render_model_backed_narrative_markdown` reads the certificate directly from `ProofNarrativeModel`, checks its identity against the canonical result, and includes the abstract section before the final unresolved-goal disclaimer. No wrapper or second post-render narrative is added.

## Reviewed revision and changes

Expected GitHub `develop` HEAD: `7e9e00f42e8b125480cd2928b0ee7ec2c5269d3a`.

Four production files change:

1. `phase168_r3_3_proof_narrative_model.py`: add an optional typed abstract certificate field and propagate it from the canonical search result.
2. `phase168_r3_5_model_renderer.py`: extend the existing shared renderer itself with a certified abstract section and result/model identity check, without replacing other rendering logic.
3. `phase173_r4_r15r9_shared_abstract_renderer/projection.py`: retain the existing result-based formatter, factor its identical prose through one shared formatter, and add a Model-based entry.
4. `phase165_r52_r3_web_adapter.py`: use the Model-based helper only for the existing Model-backed branch; retain legacy/trace behavior.

No existing public API is removed. No original ProofStep is modified, no new GIVEN is created, no special `n`/`k` rule is added, and no public completion status changes.

## Run (PowerShell)

Extract `EHP_Phase173_R4_R15R11R1_HEAD_LINEAGE_FIX.zip` into the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r11_model_abstract_integration\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r11_model_abstract_integration\run.ps1"
```

The DryRun verifies exact reviewed source hashes and generates `FULL_CHANGED_UNITS.md`, containing the **complete revised class/function and complete changed import block** extracted from the proposed source code. It makes no changes to production files. Normal execution installs four file replacements and runs only focused tests. A failed test/audit restores each original file from a hash-checked backup.

The installer refuses unreviewed source content, mismatched GitHub HEAD, staged modifications, repeated application, and a corrupted backup. Untracked audit folders from previous stages are allowed.

## Testing and boundary

Focus tests exercise `k=8` and `k=31`, both default Model and legacy Web projection, `n=3, k=3` and `n=4, k=3` complete proofs, sidecar proof provenance, unchanged unresolved goals, duplicate headings, mismatch rejection, and source-specific branch detection.

The abstract root is still not a proof of named generators. Its independent citation ancestry is not newly merged into named ProofStep citations. This stage does **not** claim a fully unified literature bibliography or Phase 173 closeout. Do not run the full test suite until Phase closeout.

## R15R11R1 — Verified HEAD lineage adjustment

The previous DryRun correctly stopped because GitHub `develop` moved from
`8bfa13946251c5618530641c572e8c756bb49af4` to
`7e9e00f42e8b125480cd2928b0ee7ec2c5269d3a`.
The only intervening commit adds the R15R10 read-only audit package.
The Git blob SHAs of all four reviewed production targets are unchanged.
Consequently, the original R15R11 implementation is retained verbatim.
Only the expected HEAD guards and correction documentation were updated;
`run.ps1` now emits `PHASE173_R4_R15R11R1_HEAD_LINEAGE=PASS` after verifying both local and remote HEADs.

If your local HEAD does not match the reviewed GitHub HEAD, inspect your changes and
use a safe fast-forward (`git pull --ff-only origin develop`) only after verifying
that it will not overwrite local work. No automatic pull, checkout, or reset occurs.

## R15R11R2 — Fail-closed repeated patch repair

The R15R11R1 DryRun exposed a real guard defect: the model-renderer replacement
contained the original anchor, allowing a second invocation to duplicate
its abstract-certificate identity check. The Source Guard correctly passed
the unmodified production files, but `test_patch_is_fail_closed_on_repetition_and_crlf`
failed with `DID NOT RAISE RuntimeError`. No production file was edited.

R15R11R2 changes only the package implementation `patch.py::_replace_once`
and adds one focused regression test to `tests/test_static.py`. The replacement
now rejects an already present output block *before* searching for the original
anchor. It continues to reject missing/duplicate anchors and preserves CRLF.
The four proposed production changes, mathematical evidence, HEAD and Git blobs,
public status, and existing API remain unchanged.

Use `EHP_Phase173_R4_R15R11R2_REPEAT_APPLY_GUARD_FIX.zip` and extract it
with `-Force`, then run the same `run.ps1 -DryRun` and normal `run.ps1`.
No complete pytest suite should be run until Phase 173 closeout.
