# Phase 169 R10E8-R3 — Distinct Family Guard Fix

This is a **guard correction** for Phase 169 R10E8. The original patch incorrectly expected two occurrences of `source.family_id`, whereas the actual R10D2 module uses `source.family_id` in `canonical_member()` and `statement.family_id` in `cited_family_reference_sentence()`.

No mathematical inference rule, database row, publication source, or proof renderer is changed beyond the **original intended R10E8 patch**. This package corrects the application mechanism only; it reuses the original R10E8 implementation and the R10E8-R2 LF/CRLF adapter.

## Required environment

- Windows PowerShell and Python 3.10 or newer
- Git `develop` at reviewed commit `940d1d1cc2e9943e9d2955c7204a4392984d65e9` or a reviewed descendant whose only new tracked files belong to the R10E8-R1/R2/R3 package directories
- Original R10E8 and R10E8-R2 packages already extracted in the repository root
- Clean tracked working copies of the two target production modules

## Run

From the repository root, extract `phase169_r10e8r3_family_guard_fix.zip` into `.` and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e8r3_family_guard_fix\run.ps1"
```

The script checks Git branch/HEAD, exact reviewed blobs, and local tracked changes. It applies the two intended original R10E8 source changes without changing newline style, runs **focused** pytest on R10E8-R3/R2/R10E8/R10D2/R10E5/R10E4 tests, and audits `pi_23^15` and `pi_24^15`. On failure, the two production modules and any overwritten R10E8 result artifacts are restored to their exact prior bytes. A full test suite is **not** run.

## Modified and new functions

The new `patch.py` has complete implementations of `_function_body`, `transformed_sources_r3`, `apply_guarded_r3_patch`, and `main`. It reuses the original R10E8 patch constants and exact-text substitution. R10D2 functions `canonical_member` and `cited_family_reference_sentence`, and `build_shared_typed_bridge` are emitted in full under the original R10E8 package's `output/` folder, along with both full transformed source files and the complete import section.

The new test module contains entire tests for the distinct source/statement guards, duplicate/changed guard rejection, CRLF/LF application, and byte preservation on failure.

## Completion boundary

Passing the focused suite and rerun audit establishes source-backed generator-image inference only if the observed proof search and Trust Boundary support it. Any remaining open goals leave a group `partial`. Proof presentation and Phase 169 full-suite closure remain out of scope.
