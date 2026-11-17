# EHP Proof Tracer — Phase 175 R3R10R1

This package makes the previously verified generator-zero inference visible in the **shared, model-backed public narrative**. In particular, the typed `GeneratorImage` already derived from Toda Lemma 5.7 can be shown as the equation `E(η₂∘ν′)=0` before the zero-map conclusion for `E: π₆² → π₇³`.

## R3R10R1 correction

On Windows, `Path.write_text()` can already create CRLF line endings. The original `test_crlf_file_preserves_line_endings()` then replaced all LF bytes with CRLF, accidentally constructing CRCRLF and failing the installer baseline check. R3R10R1 changes only this test, first normalizing CRLF to LF and then converting once to CRLF. The production patch, proof search, original citations, and Web rendering requirements are unchanged. The prior run correctly rolled back the production file after 17 tests passed and one fixture test failed.

## Scope

Only one existing function changes: `typed_sentence()` in `phase168_r3_27_typed_statement_projection.py`. Its entire replacement is shipped in `full_functions/typed_sentence_FULL.py`, together with the complete reviewed original function. A small guarded installer performs a function-level replacement, preserving the rest of the file and its line endings. No inference rules, source data, search providers, registered GIVENs, or Web completion criteria are changed.

The patch is general: it renders a **proved typed** `GeneratorImage` with a `Zero` codomain generator, not a special case keyed to a particular group, citation number or theorem name. The existing model renderer determines the position and source tags from the verified proof tree. Unsupported source generators remain undisplayed.

## Requirements

Run in the repository root, on the `develop` branch, with the completed Phase 175 R3R9 code installed. The reviewed Git `HEAD` blob for the affected file is `9ce32b5db34a3981649b9b9f2c5ff897eb8de831`. The installer fails closed if the current function differs from the reviewed source, or if the target already has an unreviewed local change. Python, pytest and PowerShell are required for the Windows workflow.

## Windows commands

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\R3R10R1.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r10_generator_zero_narrative\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File $script
git diff --check
git diff --stat
git status -sb
```

Run the normal command only after the dry-run gate passes. The normal command installs the change, runs focused pytest and validates actual Group query and Web output. On failure, it restores the original production file when safe. Reports and backup data are stored outside the repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3r10_generator_zero_narrative\`.

## Success gate

`PASS_R3R10_LEMMA57_ZERO_GENERATOR_NARRATIVE_VISIBLE`

This means the local guarded run passed, not merely that the patch archive was generated. Full-suite pytest remains reserved for the end of Phase 175. Proof search for `π₉⁵` and `π₁₀⁶` is out of scope.
