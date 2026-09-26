Phase 143-72A
=============

Purpose
-------
Normalize only the LaTeX rendering of:

  ScalarSum(left=a, right=ScalarProduct(left=-1, right=b))

to:

  a - b

This package does not add scalar evaluation, AST rewriting, bootstrap changes,
or Narrative-specific string replacement.

Apply
-----
From the ehp-proof-tracer repository root:

  Expand-Archive `
    -Path "$HOME\Downloads\phase143_72a.zip" `
    -DestinationPath "." `
    -Force

  powershell -ExecutionPolicy Bypass `
    -File ".\phase143_72a\apply_phase143_72a.ps1"

Test
----
  $env:PYTHONPATH = (Get-Location).Path

  pytest -q `
    ".\tests\test_phase143_72a_negative_scalar_product_latex.py"

  Remove-Item Env:PYTHONPATH

Do not run the full pytest suite yet. Phase policy reserves the full suite
for the end of the phase.

Then rerun the existing six-case Narrative audit used in Phase 143-71A/72
and verify that forms such as:

  E^{n + -1\,4}

no longer appear and render as:

  E^{n - 4}
