# Phase 169 R10EB — Typed Stable-Composition Power Display

This package adds a *presentation-only* rule that renders a typed composition of two or more consecutively composable members of one registered family as a power, for example `\nu_{30}^{3}` and `\sigma_{11}^{4}`.

The rule obtains the family ID, positive stem, minimum dimension, and TeX name exclusively through the existing `HyoujiGen.csv` typed-family registry. Every individual factor must satisfy the existing canonical metadata check. It never treats database rows as mathematical assertions. Noncanonical, mixed-family, and degree-incompatible expressions retain their previous rendering behavior.

## Scope

The only production functions modified are `element_tex()` in `phase168_r3_27_typed_statement_projection.py` and `render_toda_expression_latex()` in `toda_human_readable_renderer.py`. Both call the shared new helper `typed_stable_composition_power_latex()` in `phase169_r10eb_typed_composition_power/display.py`. Existing eta/sigma/nu-square fallback rendering remains to protect compatibility. No proof, citation, search, registry, or verification rules change.

`patch.py` checks the exact reviewed Git blob for both production files before preparing either edit. It handles LF and CRLF, rejects mixed newlines, applies complete-function replacements, checks Python AST postconditions, and writes full modified functions and source files to `output/`. `run.ps1` additionally checks the `develop` branch and reviewed ancestor, invokes focused pytest and a public-proof replay audit, and restores tracked sources and output files if execution fails.

## Run on Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10eb_typed_composition_power.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10eb_typed_composition_power\run.ps1"
```

The complete pytest suite is deliberately not run. The next phase concerns presentation of long stable image chains and repeated eta-image prose; this package does not compress proof sequences.
