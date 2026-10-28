# Phase 169 R10EO-R3: Reviewed Definition Bridge

This package adds an explicitly reviewed, source-backed Definition record to the existing typed proof bridge without introducing a generator-specific mathematical rule. The record is an attestation of the adopted Toda Chapter VI transcription, not a claim that the original printed edition was independently checked.

The common inference implementation is unchanged: a source-linked `GIVEN` Definition yields typed instances by the existing rule; the existing `GeneratorImage` inference requires those instances. `HyoujiGen.csv` remains identity/type metadata only. The attestation must match a complete SHA-256 fingerprint, paragraph, line, and unique formula occurrence, or registration fails.

## Requirements

Use the repository `akebono03/ehp-proof-tracer`, branch `develop`, at verified commit `3b58b2392aa0fd4ec0247f89410a85613c8b8585`. Have Python and pytest installed.

Unpack the ZIP at the repository root and run from PowerShell:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10eo_r3_reviewed_definition_bridge.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10eo_r3_reviewed_definition_bridge\run.ps1"
git status -sb
```

The runner makes backups before changing two production files; restores the original bytes after any test, audit, integrity, or patch failure; and disables pytest cache writes. The script does not run the full pytest suite. It prints the real status of $\pi_{41}^{30}$ without assuming that connecting the Definition alone completes the proof.

Full replacement function bodies are in `full_functions/`, and output copies are emitted after patching. New module and tests are complete, with no elisions.
