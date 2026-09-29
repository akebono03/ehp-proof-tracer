$ErrorActionPreference = "Stop"

$root = (Get-Location).Path
$rendererPath = Join-Path $root "toda_human_readable_renderer.py"
$testPath = Join-Path $root "tests\test_phase143_72a_negative_scalar_product_latex.py"

if (-not (Test-Path $rendererPath)) {
  throw "toda_human_readable_renderer.py not found. Run this script from the repository root."
}

$source = Get-Content -Raw -Encoding UTF8 $rendererPath

$old = @'
    if (
      isinstance(
        value.right,
        int,
      )
      and not isinstance(
        value.right,
        bool,
      )
      and value.right < 0
    ):
      return (
        _render_scalar_latex(
          value.left
        )
        + " - "
        + _render_scalar_latex(
          -value.right
        )
      )

    return (
'@

$new = @'
    if (
      isinstance(
        value.right,
        int,
      )
      and not isinstance(
        value.right,
        bool,
      )
      and value.right < 0
    ):
      return (
        _render_scalar_latex(
          value.left
        )
        + " - "
        + _render_scalar_latex(
          -value.right
        )
      )

    if (
      isinstance(
        value.right,
        ScalarProduct,
      )
      and value.right.left == -1
    ):
      return (
        _render_scalar_latex(
          value.left
        )
        + " - "
        + _render_scalar_latex(
          value.right.right
        )
      )

    return (
'@

if (-not $source.Contains($old)) {
  throw "Expected Phase 143-58A ScalarSum block was not found. No files were changed."
}

$updated = $source.Replace($old, $new)

Copy-Item $rendererPath "$rendererPath.phase143_72a.bak" -Force
Set-Content -Path $rendererPath -Value $updated -Encoding UTF8

$testContent = @'
from expression import (
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)


def test_phase143_72a_renders_negative_constant_product_in_scalar_sum_as_subtraction():
  n = ScalarSymbol(
    "n"
  )

  expression = IteratedSuspension(
    expression=HomotopyElement(
      name="η",
      dimension=4,
    ),
    exponent=ScalarSum(
      left=n,
      right=ScalarProduct(
        left=-1,
        right=4,
      ),
    ),
  )

  assert (
    render_toda_expression_latex(
      expression
    )
    == r"E^{n - 4}\eta"
  )


def test_phase143_72a_renders_negative_symbolic_product_in_scalar_sum_as_subtraction():
  m = ScalarSymbol(
    "m"
  )
  n = ScalarSymbol(
    "n"
  )

  expression = IteratedSuspension(
    expression=HomotopyElement(
      name="η",
      dimension=4,
    ),
    exponent=ScalarSum(
      left=m,
      right=ScalarProduct(
        left=-1,
        right=n,
      ),
    ),
  )

  assert (
    render_toda_expression_latex(
      expression
    )
    == r"E^{m - n}\eta"
  )


def test_phase143_72a_preserves_negative_integer_scalar_sum_rendering():
  n = ScalarSymbol(
    "n"
  )

  expression = IteratedSuspension(
    expression=HomotopyElement(
      name="η",
      dimension=4,
    ),
    exponent=ScalarSum(
      left=n,
      right=-4,
    ),
  )

  assert (
    render_toda_expression_latex(
      expression
    )
    == r"E^{n - 4}\eta"
  )
'@

Set-Content -Path $testPath -Value $testContent -Encoding UTF8

Write-Host "Phase 143-72A patch applied."
Write-Host "Changed: toda_human_readable_renderer.py"
Write-Host "Added:   tests\test_phase143_72a_negative_scalar_product_latex.py"
