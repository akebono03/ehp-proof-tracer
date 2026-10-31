# Phase 172 R2R1 — Typed Generator Identity Correction

This package corrects a false negative in the R2 display-only projection and its targeted tests. In the verified proof for π₆³, the indexed generator η₅ is stored with a Unicode-subscript name in one `HomotopyElement` and an underscore-subscript name in another, although their typed `GeneratorSymbol`, dimension, source, and target coincide.

The original R2 projection mistakenly compared the complete `HomotopyElement` objects, including their display names. R2R1 instead compares those four structured fields. A completed root ancestry, a visible cited suspension witness, and the exact direct/symmetry ProofStep premises are still required. No mathematical equality is inferred from visual text.

## Files changed

- `phase172_r2_suspension_relation_display/projection.py`: full replacement of the untracked R2 module; one new `same_typed_generator` function and one corrected existing function.
- `phase172_r2_suspension_relation_display/tests/test_projection.py`: full replacement of the R2 test module, including its helper; one additional typed-identity regression test.
- The original R2 installer applies its already-reviewed insertion to `phase168_r3_5_model_renderer.py` only after the correction files are installed. No new Renderer change is introduced by R2R1.

The installer checks the current `develop` branch and the reviewed Git blob for the Renderer. The two R2 files must exactly match either the originally shipped R2 files or the corrected R2R1 payload, allowing LF/CRLF differences. Unrelated changes stop the operation. The original sources are backed up under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r2r1_<timestamp>\`. If a focused test fails, the corrected R2 files are restored; the original R2 installer separately restores the Renderer.

## Windows PowerShell

Run from the EHP Proof Tracer repository root after extracting the ZIP:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase172_R2R1_TYPED_GENERATOR_CORRECTION.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r2r1_typed_generator_correction\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r2r1_typed_generator_correction\run.ps1" -RunFocusedTests
git status -sb
git diff --stat
```

The regular run uses the five existing R2 focused pytest groups; the first contains six tests after this correction. It does **not** execute the full test suite. It also supports a repeated run when the exact corrected Renderer is already present.

The complete corrected functions, imports, tests, and installer are included in `CODE_FULL_JA.md`. The original R2 dry run still outputs the complete final Renderer function and file outside the repository. This correction does not alter project-wide documentation or any mathematical source, database, registry, or Proof Tree.
