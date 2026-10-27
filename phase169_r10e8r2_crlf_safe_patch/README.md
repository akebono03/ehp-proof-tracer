# Phase 169 R10E8-R2: CRLF-Safe Patch Adapter

This package fixes a Windows working-tree line-ending mismatch in R10E8 without modifying proof rules, Chapter VI citations, data, or search logic. It contains the unchanged R10E8 package to make extraction self-contained.

## Source review

Reviewed baseline: GitHub `develop` commit `940d1d1cc2e9943e9d2955c7204a4392984d65e9`. `run.ps1` also allows descendant HEADs only when every intervening changed path is under the already-reviewed R10E8-R1 or R10E8-R2 package directories. It checks exact Git blob SHA values for both production targets, the existing R10E8 patch and tests, the CSV, Toda Chapter VI text, and the shared family registry.

## Apply on Windows PowerShell

Run from the repository root:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10e8r2_crlf_safe_patch.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e8r2_crlf_safe_patch\run.ps1"
```

The wrapper uses the exact original R10E8 `transformed_sources()` and its AST/source guards. It converts CRLF to LF **only in memory**, then writes each tracked source back in its original uniform newline convention (LF or CRLF). Mixed CRLF/LF, bare CR, a BOM or invalid UTF-8 fail closed. Original source bytes are restored after patch or test failure.

## Files

- `newline_support.py`: strict, reversible LF/CRLF byte conversion.
- `patch.py`: applies the *unchanged* R10E8 transform using this byte conversion; emits full replaced files, import block and complete changed functions into the existing R10E8 `output` folder.
- `tests/test_r10e8r2_newlines.py`: nine focused tests for round trips, real patch adaptation and malformed input rejection.
- `run.ps1`: reviewed source guards, patch, only focused pytest, group-search audit and rollback.
- `DESIGN_JA.md`: design and phase boundary in Japanese.

`run.ps1` runs limited tests for R10E8-R2, R10E8, R10D2, R10E5 and R10E4. It does not run the full pytest suite. A proof remains partial if open goals remain after the R10E8 audit.
