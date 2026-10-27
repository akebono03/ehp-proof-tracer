# Phase 169 R10EB-R1 — Reviewed Git Blob Guard Fix

This package corrects a source-integrity guard in the R10EB display-only installer. The reviewed `phase168_r3_27_typed_statement_projection.py` and `toda_human_readable_renderer.py` Git blobs contain CRLF line endings. The original installer normalized the bytes to LF **before** computing the Git blob ID and consequently rejected the genuine reviewed files.

This repair does not introduce or modify any proof rule, database, registry entry, search behavior, citation, or trust-boundary mechanism. It uses the original R10EB display transformation for both Renderer functions.

## Requirements

- The repository `akebono03/ehp-proof-tracer`, branch `develop`.
- The original extracted `phase169_r10eb_typed_composition_power` directory at the repository root.
- The existing R10E8 and R10E9 production changes.
- Python, pytest, Windows PowerShell, and Git available in the working environment.

The runner checks that the current HEAD descends from the reviewed commit and verifies six unchanged tracked Git blobs. Both renderer files must also be unmodified locally. No hardcoded current HEAD is required if later commits do not change the reviewed files.

## Usage

From the repository root in Windows PowerShell:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r10ebr1_git_blob_guard_fix.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r10ebr1_git_blob_guard_fix\run.ps1"
```

The R1 adapter verifies each file against the reviewed Git blob digest using the exact bytes, normalized LF bytes, or reconstructed CRLF bytes. Existing safe checkout checks must also pass. Both replacements are prepared before either production file is written; errors in the focused pytest, trust-boundary audit, or integrity checks trigger byte-exact restoration of production files and previously known audit outputs.

## Changed or added functions

All code in this R1 package is new. `patch.py` includes the full source for `prepare_patch()` and `main()`. The targeted original functions are unchanged by R1 itself: the original R10EB display transform still updates only `element_tex()` and `render_toda_expression_latex()` and writes their complete post-patch source and function text into `phase169_r10eb_typed_composition_power/output/`.

`tests/test_r10ebr1_git_blob_guard.py` contains the full focused tests and required imports. The original R10EB tests and the existing sigma, registered generator, composite image, eta alias, and narrative audit tests are included in the Windows runner.

**Full pytest is not run until the end of Phase 169.**
