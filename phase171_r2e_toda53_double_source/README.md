# Phase 171 R2E-R4 — Cited Toda (5.3) Double Identity with Compatibility Repair

This is a corrective release for the R2E installer. The first run reverted safely after six focused test failures. Five failures were caused by a pre-existing incompatibility between the explicit `sources=` argument to `build_shared_typed_bridge()` and full-production-only reference-position binding. One failure was a stale UI heading expectation in `test_phase165_r52_r9_shared_math.py`, introduced when the public narrative renderer changed.

The second retry (R2) cleared the KeyError and obsolete heading but exposed another old test assumption: the original nine-reference-only partial source snapshot does not contain all premises needed for the current pi3^2 completed proof. It returned PARTIAL; this is not evidence that the full production search failed. R3 updates that test to use the **full production source bridge**, matching the established Phase 166 R3-R verification path; the test retains all mathematical COMPLETE/conclusion/INFERENCE assertions. The explicit partial-source tests continue to test only their actual source and fail-closed contracts.

The R2E mathematical scope is unchanged: register precisely the adopted Toda equation (5.3) `2ν′ = η₃∘η₄∘η₅` as a source-verified typed `GIVEN`. This is **not** a proof of the order of ν′, cyclic generation, or the complete group π₆³. The original printed source has not been independently verified. The previously adopted archive text, fixed SHA-256 and source publication order are used.

## Modified files

- `phase165_r52_r9_shared_math.py`: replace the complete existing `build_shared_typed_bridge()` function. Retain all existing default source indices, append the new cited source to the default bridge, and apply `place_r3p_reference_positions()` only when the complete default source set is present. This avoids looking for nonexistent source references in explicit partial-source calls.
- `test_phase165_r52_r9_shared_math.py`: replace the complete `test_r9_public_pi32_narrative_unchanged()` and `test_r9_pi32_regenerated_by_shared_mathematical_expansion()` test functions by checking the current narrative's references, proof and mathematical conclusion rather than an obsolete heading. All other existing test functions are untouched. The pi3^2 completion test now uses `build_shared_typed_bridge()` (full default sources), while still requiring a completed INFERENCE proof.
- `phase171_r2e_toda53_double_reference.py`: new repository-root source module with `build_adopted_toda53_double_reference()` and its exact typed source verification.
- `phase171_r2e_toda53_double_source/`: the installer, focused tests, audit, complete replacement function/test, English README, and Japanese audit specification.

No database files, numerical group conclusions, actual proof rules, completed proof histories, web renderer implementations or official project documentation are modified.

## Windows execution

Run from the repository root on the reviewed `develop` checkout, after confirming the previous R2E restore completed successfully.

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2E_R4.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2e_toda53_double_source\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2e_toda53_double_source\run.ps1"
git status -sb
```

`run.ps1` performs focused tests, checks the screened Toda (5.3) `GIVEN`, and rejects a direct proof of the target group. If the focused tests or audit fail, it attempts to restore **both** modified tracked files and to remove the new module, using byte-exact backups under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2e_toda53_double_source_backup`.

Installer-focused unit tests were executed when assembling this release, but repository-dependent proof tests must still run on the Windows checkout. Repository-dependent focused tests must run on the actual Windows checkout. The full project test suite is deferred until the phase closes.

## R4 correction: exact test function text

R3 did not pass its preflight because its full-function replacement anchor included a blank line after `from hopf_facts import ETA_2`. The reviewed GitHub `develop` version has **no blank line there**. R4 corrects both the old and new full-function literals and the packaged complete test file. The intended mathematical test assertions and all production changes are unchanged. Additional installer unit tests guard this exact layout. No application files are modified by preflight failure.

The complete replacement test file was additionally brought into alignment with all reviewed blank lines in the unchanged test functions. When the changed functions are reversed and CRLF restored, the resulting complete test file reproduces the exact Git blob SHA `c6dcfb3cda9c9115fb802f4a1b2141e0502506bd`. A unit test now enforces this identity; the installer still changes only the two intended test functions.
